def evaluate(metrics: dict, expected_freq: float, freq_tol_hz: float = 2.0) -> dict:
    reasons = []

    # Thresholds (tune later)
    if metrics["snr_db"] < 10.0:
        reasons.append(f"SNR too low: {metrics['snr_db']:.2f} dB (< 10 dB)")

    if abs(metrics["fft_peak_hz"] - expected_freq) > freq_tol_hz:
        reasons.append(
            f"FFT peak frequency off: {metrics['fft_peak_hz']:.2f} Hz (expected {expected_freq}±{freq_tol_hz})"
        )

    if abs(metrics["mean"]) > 0.2:
        reasons.append(f"DC offset too large: mean={metrics['mean']:.3f} (> 0.2)")

    status = "PASS" if not reasons else "FAIL"
    return {"status": status, "reasons": reasons}