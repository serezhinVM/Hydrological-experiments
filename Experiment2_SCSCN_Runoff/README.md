# Experiment 2: SCS-CN Runoff

Implementation of the SCS-CN (Soil Conservation Service Curve Number) method for estimating direct runoff from rainfall.

## Overview

- **Core module** (`scscn_runoff.py`):
  - `calculate_runoff(P, CN)` — main SCS-CN runoff calculation
  - `calculate_S(CN)` — potential maximum retention
  - `calculate_Ia(CN)` — initial abstraction
  - Boundary handling (P ≤ Ia → Q=0, CN out of range → ValueError)

- **Unit tests** (`test_scscn_runoff.py`):
  - 10 tests: zero rainfall, boundary values, normal case (P=50, CN=80 → Q≈13.8 mm), physical constraint Q ≤ P, CN monotonicity

- **Sensitivity analysis** (`sensitivity_analysis.py`):
  - Runoff vs CN at fixed rainfall P=50 mm
  - Rainfall-runoff curves for multiple CN values (60, 70, 80, 90, 95, 100)
  - Visualizations: `Rainfall-Runoff Relationship for Different CN Values.png`, `SCS-CN Sensitivity Analysis.png`

## Files

| File | Purpose |
|------|---------|
| `scscn_runoff.py` | Main runoff calculation module |
| `test_scscn_runoff.py` | Pytest test suite |
| `sensitivity_analysis.py` | Sensitivity analysis and plots |
| `*.png` | Result visualizations |
| `Experiment2_SCSCN_Runoff.docx` | Experiment description |
| `prompt_log.md` | AI interaction log |
