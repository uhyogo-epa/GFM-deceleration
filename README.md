# GFM deceleration

Implementation accompanying **Fault-induced Decelerating Loss of Synchronism in Multi-Grid-Forming Inverter Systems**.

A common eight-bus model compares fault recovery and negative internal-angle rotation under Droop and virtual synchronous machine (VSM) control. The model retains LCL-filter and inner-controller dynamics, a current-command limiter, and network switching.

This repository is being aligned with the manuscript. The existing calculations and saved results are retained; the model explanation and manuscript-to-code correspondence are being organized. The documentation identifies the current scope and remaining verification.

## Start here

- [Model and assumptions](docs/model.md): what is simulated and where the equations are implemented.
- [Reproduce the results](docs/reproduction.md): environment, commands, and output locations.
- [Paper-to-code map](docs/paper-map.md): manuscript figures, inputs, saved data, and commands.

## Repository layout

| Location | Contents |
|---|---|
| [src](src/) | Shared model, integration, analysis, and plotting implementation |
| [studies/paper](studies/paper/) | Paper study: settings, executable scripts, saved results, and figures |
| [docs](docs/) | Model explanation, numerical verification, and reproducibility guidance |

New calculations and plots go into `outputs/` (ignored by Git); saved study data remain read-only.

## Quick start

From the repository root, with Python 3.11+ and Julia 1.12.5 installed:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python studies/paper/scripts/plot.py --only time
```

This redraws saved time responses into `outputs/figures/paper/`; it does not run a simulation.

To instantiate Julia dependencies and compute case C:

```bash
julia +1.12.5 --project=. -e 'using Pkg; Pkg.instantiate()'
OPENBLAS_NUM_THREADS=1 julia +1.12.5 --project=. studies/paper/scripts/run.jl cases.csv C
```

See the [reproduction guide](docs/reproduction.md) for phase-plane calculations and validation. Citation metadata are in [CITATION.cff](CITATION.cff). Third-party component scope and license notices are in [third-party components](docs/third-party.md).
