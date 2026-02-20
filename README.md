# Signal Verification & Characterization Tool

A Python-based signal verification framework that simulates noisy transmission environments and performs automated characterization.

The tool computes SNR (dB), FFT peak frequency, and statistical metrics, applies pass/fail validation rules, and generates structured CSV/JSON test reports.

---

## Features

- Signal generation (sine, square)
- Gaussian noise injection with deterministic seed support
- SNR (dB), RMS, mean, and standard deviation computation
- FFT peak frequency detection
- Automated pass/fail rule engine with failure reasons
- Parameter sweep mode (noise vs SNR)
- Structured CSV logging with run IDs
- JSON summary export

---

## Example Outputs

### Time-Domain Waveform

![Waveform Example](outputs/plots/waveform_example.png)

### SNR vs Noise Sweep

![SNR Sweep](outputs/plots/snr_vs_noise.png)

---

## Usage

### Single Run

```bash
python -m src.svtool.cli --mode sine --freq 50 --noise 0.3 --seed 1
```

### Noise Sweep Mode

```bash
python -m src.svtool.cli --mode sine --freq 50 --seed 1 --sweep-noise 0.01 1.0 10
```

---

## Output Artifacts

After execution, the tool generates:

- `report.csv` — structured per-test logging
- `summary.json` — summary of most recent run
- `waveform_example.png` — time-domain visualization
- `snr_vs_noise.png` — sweep characterization plot

---

## Technologies

- Python
- NumPy
- Pandas
- Matplotlib
- Modular CLI architecture

---

## Motivation

This project was built to emulate structured verification workflows used in hardware and signal validation environments, emphasizing automation, robustness characterization, and failure analysis.