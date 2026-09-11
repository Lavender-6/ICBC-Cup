import numpy as np
from scipy.signal import spectrogram


def compute_fft(iq_data: np.ndarray) -> np.ndarray:
    return np.fft.fftshift(np.fft.fft(iq_data))


def compute_spectrogram(iq_data: np.ndarray, nperseg: int = 128, noverlap: int = 64):
    f, t, Sxx = spectrogram(iq_data, nperseg=nperseg, noverlap=noverlap)
    return f, t, 10 * np.log10(Sxx + 1e-10)


def estimate_snr(iq_data: np.ndarray) -> float:
    signal_power = np.mean(np.abs(iq_data) ** 2)
    noise_power = np.var(iq_data - np.mean(iq_data))
    if noise_power > 0:
        return float(10 * np.log10(signal_power / noise_power))
    return 0.0


def estimate_carrier_freq(iq_data: np.ndarray, sample_rate: float = 1.0) -> float:
    fft_vals = np.fft.fftshift(np.fft.fft(iq_data))
    freqs = np.fft.fftshift(np.fft.fftfreq(len(iq_data), 1 / sample_rate))
    peak_idx = np.argmax(np.abs(fft_vals))
    return float(freqs[peak_idx])


def downsample(iq_data: np.ndarray, factor: int = 4) -> np.ndarray:
    return iq_data[::factor]
