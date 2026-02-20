import argparse
import numpy as np
from .plot import plot_snr_sweep
from datetime import datetime

from .simulate import generate_signal, add_noise
from .plot import plot_waveform
from .metrics import snr_db, fft_peak, basic_stats
from .rules import evaluate
from .report import write_report_row, write_summary


def main():
    parser = argparse.ArgumentParser(description="Signal Verification Tool")
    parser.add_argument("--mode", type=str, default="sine", help="Signal mode (sine/square)")
    parser.add_argument("--freq", type=float, default=50, help="Signal frequency (Hz)")
    parser.add_argument("--noise", type=float, default=0.1, help="Noise standard deviation")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--duration", type=float, default=1.0, help="Duration (s)")
    parser.add_argument("--fs", type=float, default=10000, help="Sample rate (Hz)")

    parser.add_argument(
    "--sweep-noise",
    nargs=3,
    type=float,
    default=None,
    metavar=("START", "END", "STEPS"),
    help="Sweep noise std from START to END with STEPS points"
    )

    args = parser.parse_args()

    run_timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    run_type = "sweep" if args.sweep_noise is not None else "single"
    run_id = f"{run_timestamp}_{run_type}"

    if args.sweep_noise is not None:
        start, end, steps = args.sweep_noise
        steps = int(steps)
        noise_vals = np.linspace(start, end, steps)

        results = []
        for nstd in noise_vals:
            t, clean_signal, fs = generate_signal(
                mode=args.mode, freq=args.freq, duration=args.duration, fs=int(args.fs)
            )
            noisy_signal, _ = add_noise(clean_signal, noise_std=float(nstd), seed=args.seed)

            stats = basic_stats(noisy_signal)
            snr = snr_db(clean_signal, noisy_signal)
            peak_hz, peak_mag = fft_peak(noisy_signal, fs)

            metrics = {**stats, "snr_db": snr, "fft_peak_hz": peak_hz, "fft_peak_mag": peak_mag}
            verdict = evaluate(metrics, expected_freq=args.freq)

            row = {
                "run_id": run_id,
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "mode": args.mode,
                "freq_hz": args.freq,
                "noise_std": float(nstd),
                "seed": args.seed,
                "snr_db": metrics["snr_db"],
                "fft_peak_hz": metrics["fft_peak_hz"],
                "mean": metrics["mean"],
                "std": metrics["std"],
                "rms": metrics["rms"],
                "status": verdict["status"],
                "reasons": "; ".join(verdict["reasons"]),
                "fft_peak_hz": metrics["fft_peak_hz"],
                "fft_peak_mag": metrics["fft_peak_mag"],
            }
            write_report_row(row)
            results.append((float(nstd), metrics["snr_db"], verdict["status"]))

        sweep_plot = plot_snr_sweep(results, output_dir="outputs/plots")
        write_summary({
            "last_run": datetime.now().isoformat(timespec="seconds"),
            "mode": "sweep",
            "points": len(results),
            "best_snr_db": max(r[1] for r in results),
            "worst_snr_db": min(r[1] for r in results),
            "sweep_plot": sweep_plot
        })

        print(f"Sweep complete. Plot saved to: {sweep_plot}")
        return

    print("Running Signal Verification Tool...")
    t, clean_signal, fs = generate_signal(mode=args.mode, freq=args.freq, duration=args.duration, fs=int(args.fs))
    noisy_signal, _ = add_noise(clean_signal, noise_std=args.noise, seed=args.seed)

    # Plot
    plot_path = plot_waveform(t, clean_signal, noisy_signal)

    # Metrics
    stats = basic_stats(noisy_signal)
    snr = snr_db(clean_signal, noisy_signal)
    peak_hz, peak_mag = fft_peak(noisy_signal, fs)

    metrics = {
        **stats,
        "snr_db": snr,
        "fft_peak_hz": peak_hz,
        "fft_peak_mag": peak_mag,
    }

    # Rules
    verdict = evaluate(metrics, expected_freq=args.freq)

    # Output row
    row = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "mode": args.mode,
        "freq_hz": args.freq,
        "noise_std": args.noise,
        "seed": args.seed,
        "snr_db": metrics["snr_db"],
        "fft_peak_hz": metrics["fft_peak_hz"],
        "mean": metrics["mean"],
        "std": metrics["std"],
        "rms": metrics["rms"],
        "status": verdict["status"],
        "reasons": "; ".join(verdict["reasons"]),
        "plot": plot_path,
    }

    report_path = write_report_row(row)
    summary_path = write_summary(
        {
            "last_run": row["timestamp"],
            "status": verdict["status"],
            "snr_db": metrics["snr_db"],
            "fft_peak_hz": metrics["fft_peak_hz"],
            "reasons": verdict["reasons"],
        }
    )

    print(f"Status: {verdict['status']}")
    if verdict["reasons"]:
        print("Reasons:")
        for r in verdict["reasons"]:
            print(f"  - {r}")

    print(f"Saved plot: {plot_path}")
    print(f"Updated report: {report_path}")
    print(f"Updated summary: {summary_path}")
    print("Done.")


if __name__ == "__main__":
    main()