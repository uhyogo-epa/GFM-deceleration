# Reproduction

Run commands from the repository root. Julia dependencies are pinned by `Project.toml` and `Manifest.toml`; the recorded Julia version is 1.12.5. Python 3.11+ and the packages in `requirements.txt` are needed for plotting and saved-data checks. Julia workflows also use the `gzip` executable.

## Environment

See [Environment setup](../README.md#environment-setup) for prerequisites and the roles of the Julia and Python environment files. With Juliaup installed, the complete setup is:

```bash
juliaup add 1.12.5
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
julia +1.12.5 --project=. -e 'using Pkg; Pkg.instantiate()'
```

## Independent tasks

| Task | Command | Output |
|---|---|---|
| Redraw time responses | `python studies/scripts/plot.py --only time` | `studies/outputs/figures/` |
| Redraw main sections | `python studies/scripts/plot.py --only basins` | `studies/outputs/figures/` |
| Redraw system and power-flow views | `python studies/scripts/power_flow.py` | `studies/outputs/figures/` |
| Recompute case C | `julia +1.12.5 --project=. studies/scripts/run.jl cases.csv C` | `studies/outputs/runs/C/` |
| Recompute main sections | `julia +1.12.5 --project=. studies/scripts/fault_basins.jl` | `studies/outputs/fault_basins/` |
| Check saved-data identities, links, and import safety | `python studies/scripts/check_repository.py` | `studies/outputs/checks/` |
| Compare saved waveforms with source fixtures | `python studies/scripts/validate.py` | `studies/outputs/checks/` |
| Check RHS, network voltages, and saved classifications | `julia +1.12.5 --project=. studies/scripts/check_refactor.jl` | `studies/outputs/checks/` |
| Check equations and physical-event integration | `julia +1.12.5 --project=. studies/scripts/check_equations.jl` | `studies/outputs/checks/` |

For Julia calculations set `OPENBLAS_NUM_THREADS=1`; section calculations can use `JULIA_NUM_THREADS=8`. Replotting saved data does not require Julia. Use `--output` to choose a new destination when an existing run would conflict.

[Detailed command options and run identities](RUNNING.md) · [Numerical checks](VALIDATION.md) · [Code responsibilities](REPRODUCIBILITY.md).

## Initial layout verification

The [layout verification record](../studies/provenance/layout_validation.toml) records unchanged numerical input values, byte-identical saved data and figures, and 36 bitwise-equal before/after RHS and network-voltage evaluations. The 230 saved-waveform comparisons and equation checks pass. Case C was also executed through pre-fault, fault-on, and a short post-fault interval as an execution check; this does not replace the 1000 s classification runs.

In this environment, `check_refactor.jl` fails its exact-zero fixture assertion on both the tagged baseline and the reorganized code. Maximum deviations from the stored fixtures are approximately `4.26e-12` for the RHS and `3.34e-16` for voltage. The original assertion is retained; the direct baseline comparison establishes that the layout change introduces no difference at these states.
