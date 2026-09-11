import numpy as np
from scipy.signal import spectrogram
from scipy.ndimage import zoom


def preprocess_signal(file_path: str, format: str) -> np.ndarray:
    if format == "npy":
        data = np.load(file_path)
        if data.dtype == np.complex64 or data.dtype == np.complex128:
            return data
        if data.ndim == 2 and data.shape[1] == 2:
            return data[:, 0] + 1j * data[:, 1]
        return data.astype(np.complex64)
    elif format == "wav":
        from scipy.io import wavfile
        _, data = wavfile.read(file_path)
        if data.ndim == 2:
            return data[:, 0] + 1j * data[:, 1]
        return data.astype(np.complex64)
    else:
        raise ValueError(f"Unsupported format: {format}")


def generate_visualization(iq_data: np.ndarray) -> dict:
    n = min(len(iq_data), 4096)
    iq = iq_data[:n]

    f, t, Sxx = spectrogram(iq, nperseg=128, noverlap=64)
    waterfall = 10 * np.log10(Sxx + 1e-10)
    waterfall_resized = zoom(waterfall, (64 / waterfall.shape[0], 64 / waterfall.shape[1]))
    waterfall_list = waterfall_resized.tolist()

    sample_step = max(1, len(iq) // 2000)
    constellation = [
        {"i": float(iq[i].real), "q": float(iq[i].imag)}
        for i in range(0, len(iq), sample_step)
    ]

    return {
        "waterfall": waterfall_list,
        "constellation": constellation,
    }
