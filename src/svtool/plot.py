import matplotlib.pyplot as plt
import os


def plot_waveform(t, clean_signal, noisy_signal, output_dir="outputs/plots"):
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(10, 4))
    plt.plot(t, clean_signal, label="Clean Signal")
    plt.plot(t, noisy_signal, label="Noisy Signal", alpha=0.7)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Signal Verification - Time Domain")
    plt.legend()
    plt.tight_layout()

    filepath = os.path.join(output_dir, "waveform_example.png")
    plt.savefig(filepath)
    plt.close()

    return filepath

def plot_snr_sweep(results, output_dir="outputs/plots"):
    """
    results: list of (noise_std, snr_db, status)
    """
    os.makedirs(output_dir, exist_ok=True)

    noise = [r[0] for r in results]
    snr = [r[1] for r in results]

    plt.figure(figsize=(8, 4))
    plt.plot(noise, snr, marker="o")
    plt.xlabel("Noise STD")
    plt.ylabel("SNR (dB)")
    plt.title("SNR vs Noise Sweep")
    plt.tight_layout()

    filepath = os.path.join(output_dir, "snr_vs_noise.png")
    plt.savefig(filepath)
    plt.close()
    return filepath