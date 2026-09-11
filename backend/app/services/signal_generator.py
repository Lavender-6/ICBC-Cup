import numpy as np


def generate_bpsk(num_samples: int = 4096, sample_rate: int = 1000, freq: float = 100, snr_db: float = 20) -> np.ndarray:
    t = np.arange(num_samples) / sample_rate
    bits = np.random.randint(0, 2, num_samples)
    symbols = 2 * bits - 1
    signal = symbols * np.exp(1j * 2 * np.pi * freq * t)
    return _add_noise(signal, snr_db)


def generate_qpsk(num_samples: int = 4096, sample_rate: int = 1000, freq: float = 100, snr_db: float = 20) -> np.ndarray:
    t = np.arange(num_samples) / sample_rate
    bits = np.random.randint(0, 4, num_samples)
    phases = bits * np.pi / 2 + np.pi / 4
    signal = np.exp(1j * phases) * np.exp(1j * 2 * np.pi * freq * t)
    return _add_noise(signal, snr_db)


def generate_16qam(num_samples: int = 4096, sample_rate: int = 1000, freq: float = 100, snr_db: float = 20) -> np.ndarray:
    t = np.arange(num_samples) / sample_rate
    levels = np.array([-3, -1, 1, 3])
    i_bits = np.random.choice(levels, num_samples)
    q_bits = np.random.choice(levels, num_samples)
    symbols = (i_bits + 1j * q_bits) / np.sqrt(10)
    signal = symbols * np.exp(1j * 2 * np.pi * freq * t)
    return _add_noise(signal, snr_db)


def generate_64qam(num_samples: int = 4096, sample_rate: int = 1000, freq: float = 100, snr_db: float = 20) -> np.ndarray:
    t = np.arange(num_samples) / sample_rate
    levels = np.array([-7, -5, -3, -1, 1, 3, 5, 7])
    i_bits = np.random.choice(levels, num_samples)
    q_bits = np.random.choice(levels, num_samples)
    symbols = (i_bits + 1j * q_bits) / np.sqrt(42)
    signal = symbols * np.exp(1j * 2 * np.pi * freq * t)
    return _add_noise(signal, snr_db)


def generate_am(num_samples: int = 4096, sample_rate: int = 1000, freq: float = 100, snr_db: float = 20) -> np.ndarray:
    t = np.arange(num_samples) / sample_rate
    modulation = 0.5 * np.sin(2 * np.pi * 10 * t)
    signal = (1 + modulation) * np.exp(1j * 2 * np.pi * freq * t)
    return _add_noise(signal, snr_db)


def generate_fm(num_samples: int = 4096, sample_rate: int = 1000, freq: float = 100, snr_db: float = 20) -> np.ndarray:
    t = np.arange(num_samples) / sample_rate
    modulation = np.sin(2 * np.pi * 10 * t)
    signal = np.exp(1j * (2 * np.pi * freq * t + 5 * modulation))
    return _add_noise(signal, snr_db)


BUILTIN_SIGNALS = {
    "bpsk-test": {"name": "BPSK 测试信号", "modulation": "BPSK", "generator": generate_bpsk},
    "qpsk-test": {"name": "QPSK 测试信号", "modulation": "QPSK", "generator": generate_qpsk},
    "16qam-test": {"name": "16QAM 测试信号", "modulation": "16QAM", "generator": generate_16qam},
    "64qam-test": {"name": "64QAM 测试信号", "modulation": "64QAM", "generator": generate_64qam},
    "am-test": {"name": "AM 测试信号", "modulation": "AM", "generator": generate_am},
    "fm-test": {"name": "FM 测试信号", "modulation": "FM", "generator": generate_fm},
}


def generate_builtin_signal(signal_type: str) -> tuple[np.ndarray, str]:
    if signal_type not in BUILTIN_SIGNALS:
        raise ValueError(f"Unknown signal type: {signal_type}")
    info = BUILTIN_SIGNALS[signal_type]
    iq_data = info["generator"]()
    return iq_data, info["modulation"]


def _add_noise(signal: np.ndarray, snr_db: float) -> np.ndarray:
    signal_power = np.mean(np.abs(signal) ** 2)
    noise_power = signal_power / (10 ** (snr_db / 10))
    noise = np.sqrt(noise_power / 2) * (np.random.randn(len(signal)) + 1j * np.random.randn(len(signal)))
    return (signal + noise).astype(np.complex64)
