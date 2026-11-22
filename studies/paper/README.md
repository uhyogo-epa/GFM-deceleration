# Paper study

Run all commands from the repository root. [Reproduction guide](../../docs/reproduction.md) · [Paper-to-code map](../../docs/paper-map.md).

| Location | Purpose |
|---|---|
| `inputs/` | Physical parameters, cases A/B/C, numerical settings, and prescribed initial-state sections |
| `scripts/` | Simulation, plotting, and verification entry points |
| `results/` | Saved states, observables, classifications, roots, and validation results |
| `figures/` | Saved paper and supplementary figures; `catalog.toml` maps them to source datasets |
| `provenance/` | Numerical identity catalogs, source fixtures, and technical audits |

These directories form one study. They are retained together while the manuscript correspondence is reviewed; supplementary and historical checks are not presented as additional paper cases. New results go to the repository's `outputs/` directory.
