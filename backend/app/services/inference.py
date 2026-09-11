import os
import numpy as np
import onnxruntime as ort
from app.config import settings

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "ai", "models")

_modulations = ["AM", "FM", "BPSK", "QPSK", "16QAM", "64QAM", "WBFM", "AM-SSB", "AM-DSB"]

_classifier_session: ort.InferenceSession | None = None
_regressor_session: ort.InferenceSession | None = None


def _get_classifier():
    global _classifier_session
    if _classifier_session is None:
        path = os.path.join(MODEL_PATH, "classifier.onnx")
        if os.path.exists(path):
            _classifier_session = ort.InferenceSession(path)
    return _classifier_session


def _get_regressor():
    global _regressor_session
    if _regressor_session is None:
        path = os.path.join(MODEL_PATH, "regressor.onnx")
        if os.path.exists(path):
            _regressor_session = ort.InferenceSession(path)
    return _regressor_session


def run_inference(iq_data: np.ndarray) -> dict:
    classifier = _get_classifier()
    regressor = _get_regressor()

    if classifier is not None:
        input_name = classifier.get_inputs()[0].name
        features = _extract_features(iq_data)
        outputs = classifier.run(None, {input_name: features[np.newaxis, ...]})
        pred = np.argmax(outputs[0], axis=1)[0]
        probs = np.softmax(outputs[0], axis=1)[0]
        modulation = _modulations[pred]
        confidence = float(probs[pred]) * 100
    else:
        modulation = "Unknown"
        confidence = 0.0

    if regressor is not None:
        input_name = regressor.get_inputs()[0].name
        features = _extract_features(iq_data)
        outputs = regressor.run(None, {input_name: features[np.newaxis, ...]})
        snr = float(outputs[0][0])
    else:
        snr = _estimate_snr(iq_data)

    return {
        "modulation": modulation,
        "confidence": round(confidence, 2),
        "snr": round(snr, 2),
        "symbol_rate": None,
        "freq_offset": None,
    }


def _extract_features(iq_data: np.ndarray, target_size: tuple = (64, 64)) -> np.ndarray:
    n = min(len(iq_data), 1024)
    fft_vals = np.fft.fftshift(np.fft.fft(iq_data[:n]))
    power = 20 * np.log10(np.abs(fft_vals) + 1e-10)
    from scipy.signal import spectrogram
    f, t, Sxx = spectrogram(iq_data[:n], nperseg=64, noverlap=32)
    from scipy.ndimage import zoom
    Sxx_db = 10 * np.log10(Sxx + 1e-10)
    zoom_factors = (target_size[0] / Sxx_db.shape[0], target_size[1] / Sxx_db.shape[1])
    resized = zoom(Sxx_db, zoom_factors)
    return resized.astype(np.float32)


def _estimate_snr(iq_data: np.ndarray) -> float:
    signal_power = np.mean(np.abs(iq_data) ** 2)
    noise_power = np.var(iq_data - np.mean(iq_data))
    if noise_power > 0:
        return float(10 * np.log10(signal_power / noise_power))
    return 0.0
