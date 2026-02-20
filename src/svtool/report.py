import os
import json
import csv
import pandas as pd


def write_report_row(row: dict, output_dir: str = "outputs"):
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "report.csv")

    # Clean optional fields (no NaNs)
    row["reasons"] = row.get("reasons") or ""
    row["plot"] = row.get("plot") or ""

    # Lock column order so every row matches the same schema
    columns = [
        "run_id",
        "timestamp",
        "mode",
        "freq_hz",
        "noise_std",
        "seed",
        "snr_db",
        "fft_peak_hz",
        "fft_peak_mag",
        "mean",
        "std",
        "rms",
        "status",
        "reasons",
        "plot",
    ]

    df = pd.DataFrame([row], columns=columns)

    # If file doesn't exist, write header. Otherwise append.
    write_header = not os.path.exists(path)

    df.to_csv(
        path,
        mode="a",
        header=write_header,
        index=False,
        quoting=csv.QUOTE_MINIMAL,   # quotes fields when needed (commas, etc.)
    )

    return path


def write_summary(summary: dict, output_dir: str = "outputs"):
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "summary.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    return path