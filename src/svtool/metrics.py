import numpy as np

def rms(x: np.ndarray) -> float:
    return float(np.sqrt(np.mean(x**2)))

def snr_db(clean: np.ndarray, noisy: np.ndarray) -> float:
    noise = noisy - clean
    signal_power = np.mean(clean**2)
    noise_power = np.mean(noise**2)
    if noise_power == 0:
        return float("inf")
    return float(10 * np.log10(signal_power / noise_power))

def fft_peak(noisy: np.ndarray, fs: float) -> tuple[float, float]:
    # Returns (peak_freq_hz, peak_mag)
    n = len(noisy)
    fft_vals = np.fft.rfft(noisy)
    mags = np.abs(fft_vals)
    freqs = np.fft.rfftfreq(n, d=1/fs)

    # ignore DC bin at index 0 so we don’t “peak” at 0 Hz
    peak_idx = int(np.argmax(mags[1:]) + 1)
    return float(freqs[peak_idx]), float(mags[peak_idx])

def basic_stats(x: np.ndarray) -> dict:
    return {
        "mean": float(np.mean(x)),
        "std": float(np.std(x)),
        "min": float(np.min(x)),
        "max": float(np.max(x)),
        "rms": rms(x),
    }