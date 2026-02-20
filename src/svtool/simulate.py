import numpy as np

def generate_signal(mode="sine", freq=50, duration=1.0, fs=10000):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)

    if mode == "sine":
        signal = np.sin(2 * np.pi * freq * t)
    elif mode == "square":
        signal = np.sign(np.sin(2 * np.pi * freq * t))
    else:
        raise ValueError("Unsupported mode")

    return t, signal, fs


def add_noise(signal, noise_std=0.1, seed=None):
    if seed is not None:
        np.random.seed(seed)

    noise = np.random.normal(0, noise_std, len(signal))
    noisy_signal = signal + noise
    return noisy_signal, noise