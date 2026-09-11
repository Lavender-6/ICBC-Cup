import numpy as np
from scipy.signal import spectrogram, butter, filtfilt
from scipy.ndimage import zoom


def preprocess_signal(file_path: str, format: str) -> np.ndarray:
    if format == "npy":
        data = np.load(file_path)
        if data.dtype == np.complex64 or data.dtype == np.complex128:
            iq = data
        elif data.ndim == 2 and data.shape[1] == 2:
            iq = data[:, 0] + 1j * data[:, 1]
        else:
            iq = data.astype(np.complex64)
    elif format == "wav":
        from scipy.io import wavfile
        _, data = wavfile.read(file_path)
        if data.ndim == 2:
            iq = data[:, 0] + 1j * data[:, 1]
        else:
            iq = data.astype(np.complex64)
    else:
        raise ValueError(f"Unsupported format: {format}")

    iq = remove_dc(iq)
    iq = normalize(iq)
    return iq


def remove_dc(iq_data: np.ndarray) -> np.ndarray:
    return iq_data - np.mean(iq_data)


def normalize(iq_data: np.ndarray) -> np.ndarray:
    max_val = np.max(np.abs(iq_data))
    if max_val > 0:
        return iq_data / max_val
    return iq_data


def downsample(iq_data: np.ndarray, factor: int = 4) -> np.ndarray:
    return iq_data[::factor]


def bandpass_filter(iq_data: np.ndarray, low: float = 0.1, high: float = 0.4, order: int = 5) -> np.ndarray:
    b, a = butter(order, [low, high], btype="band")
    filtered = filtfilt(b, a, iq_data.real) + 1j * filtfilt(b, a, iq_data.imag)
    return filtered.astype(np.complex64)


def generate_visualization(iq_data: np.ndarray) -> dict:
    n = min(len(iq_data), 4096)
    iq = iq_data[:n]

    f, t, Sxx = spectrogram(iq, nperseg=128, noverlap=64, return_onesided=False)
    waterfall = 10 * np.log10(Sxx + 1e-10)

    target_shape = (64, 64)
    zoom_factors = (target_shape[0] / waterfall.shape[0], target_shape[1] / waterfall.shape[1])
    waterfall_resized = zoom(waterfall, zoom_factors)
    waterfall_list = np.nan_to_num(waterfall_resized, nan=-20.0).tolist()

    sample_step = max(1, len(iq) // 2000)
    constellation = []
    for i in range(0, len(iq), sample_step):
        constellation.append({"i": float(iq[i].real), "q": float(iq[i].imag)})

    return {
        "waterfall": waterfall_list,
        "constellation": constellation,
    }


def extract_features(iq_data: np.ndarray, target_size: tuple = (64, 64)) -> np.ndarray:
    n = min(len(iq_data), 1024)
    iq = iq_data[:n]

    f, t, Sxx = spectrogram(iq, nperseg=64, noverlap=32)
    Sxx_db = 10 * np.log10(Sxx + 1e-10)

    zoom_factors = (target_size[0] / Sxx_db.shape[0], target_size[1] / Sxx_db.shape[1])
    features = zoom(Sxx_db, zoom_factors)
    return np.nan_to_num(features, nan=-20.0).astype(np.float32)
