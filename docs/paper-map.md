# Manuscript-to-code correspondence

This initial map follows the current local manuscript, titled **Fault-induced Decelerating Loss of Synchronism in Multi-Grid-Forming Inverter Systems**. Figure numbers may change during revision; descriptive names and filenames identify the content. Final numerical agreement with the submission version remains to be reviewed.

All paths below refer to the [paper study](../studies/). Run commands from the repository root.

| Manuscript content | Settings / saved data | Saved figure | Reproduction entry point |
|---|---|---|---|
| Eight-bus system and contingency | `inputs/common.toml`, `inputs/study.toml` | [system.pdf](figures/system.pdf) | `python studies/scripts/figure1.py` |
| Cases A/B/C and time responses | `inputs/cases.csv`; `results/A/`, `results/B/`, `results/C/` | [time_response_ABC.pdf](../studies/figures/paper/time_response_ABC.pdf) | `python studies/scripts/plot.py --only time` |
| Case C power flow before the fault and 1 s after clearing | `results/power_flow/common_pre_equilibrium/`, `results/power_flow/C_post_1s/` | [pre-fault](../studies/figures/details/power_flow/C_pre_equilibrium.pdf), [post-fault](../studies/figures/details/power_flow/C_post_1s.pdf) | `python studies/scripts/plot_flow_comparison.py` |
| Conditional initial-state sections and actual paths | `inputs/fault_basin.toml`; `results/fault_basins/` | [A](../studies/figures/paper/basin_A.pdf), [B](../studies/figures/paper/basin_B.pdf), [C](../studies/figures/paper/basin_C.pdf) | `python studies/scripts/plot.py --only basins` |

To recompute time responses use `julia +1.12.5 --project=. studies/scripts/run.jl cases.csv A,B,C`. To recompute sections use `julia +1.12.5 --project=. studies/scripts/fault_basins.jl`. Section plots must be interpreted using the [section definitions](BASIN_VIEWS.md).

Supplementary damping comparisons, local sections, and historical source checks remain available inside the same study, with their scope described in the [detailed figure guide](DETAILS.md).
