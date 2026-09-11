import numpy as np
import onnxruntime as ort
from scipy.signal import spectrogram
from scipy.ndimage import zoom

MODULATIONS = ["AM", "FM", "BPSK", "QPSK", "16QAM", "64QAM", "WBFM", "AM-SSB", "AM-DSB"]


def extract_features(iq_data: np.ndarray, target_size: tuple = (64, 64)) -> np.ndarray:
    n = min(len(iq_data), 1024)
    f, t, Sxx = spectrogram(iq_data[:n], nperseg=64, noverlap=32)
    Sxx_db = 10 * np.log10(Sxx + 1e-10)
    zoom_factors = (target_size[0] / Sxx_db.shape[0], target_size[1] / Sxx_db.shape[1])
    return zoom(Sxx_db, zoom_factors).astype(np.float32)


def predict_modulation(iq_data: np.ndarray, model_path: str = "models/classifier.onnx") -> dict:
    session = ort.InferenceSession(model_path)
    features = extract_features(iq_data)
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: features[np.newaxis, ...]})
    pred = np.argmax(outputs[0], axis=1)[0]
    probs = np.exp(outputs[0][0]) / np.sum(np.exp(outputs[0][0]))
    return {"modulation": MODULATIONS[pred], "confidence": float(probs[pred]) * 100}


def predict_snr(iq_data: np.ndarray, model_path: str = "models/regressor.onnx") -> float:
    session = ort.InferenceSession(model_path)
    features = extract_features(iq_data)
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: features[np.newaxis, ...]})
    return float(outputs[0][0])


if __name__ == "__main__":
    dummy_iq = np.random.randn(1024) + 1j * np.random.randn(1024)
    dummy_iq = dummy_iq.astype(np.complex64)

    try:
        result = predict_modulation(dummy_iq)
        print(f"Modulation: {result['modulation']}, Confidence: {result['confidence']:.2f}%")
    except Exception as e:
        print(f"Classifier not available: {e}")

    try:
        snr = predict_snr(dummy_iq)
        print(f"Estimated SNR: {snr:.2f} dB")
    except Exception as e:
        print(f"Regressor not available: {e}")
