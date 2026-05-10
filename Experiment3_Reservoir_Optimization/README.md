# Experiment 3: Reservoir Optimization

Optimal daily water release scheduling for a reservoir to maximize hydropower revenue.

## Overview

- **Mathematical formulation** (`formulation.md`): 7 decision variables (Q[t]), revenue maximization objective, storage/release constraints, mass balance

- **Main optimization** (`reservoir_optimize.py`):
  - SLSQP solver with native inequality constraints
  - L-BFGS-B solver with penalty method (comparison)
  - Parameters: V₀=500k m³, V_min=100k, V_max=1M, Q_eco=10 m³/s, Q_max=100 m³/s
  - Inflow: [15,12,10,8,12,15,18] m³/s, prices: [$0.08–0.12]/kWh

- **Multi-objective analysis** (Pareto frontier): revenue vs ecological deficit trade-off → `tradeoff_analysis.png`

- **Uncertainty analysis**: Monte Carlo (50 scenarios, 15% inflow noise)

- **Validation report** (`validation_report.txt`): constraint checks, algorithm comparison, MC statistics

- **Release schedule** (`optimal_schedule.csv`): daily plan

## Files

| File | Purpose |
|------|---------|
| `reservoir_optimize.py` | Main optimization script |
| `formulation.md` | Mathematical problem formulation |
| `optimal_schedule.csv` | Optimal release schedule |
| `validation_report.txt` | Validation report |
| `tradeoff_analysis.png` | Pareto frontier plot |
| `Experiment3_Reservoir_Optimization.docx` | Experiment description |
| `prompt_log.md` | AI interaction log |
