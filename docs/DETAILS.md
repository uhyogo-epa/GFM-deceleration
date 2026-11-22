# Detailed figures and data

These figures are retained for repository inspection; the paper candidates are in [studies/paper/figures/paper](../studies/paper/figures/paper/). Every listed figure has a PDF and PNG. All time responses use fixed Bus6 internal angles, seconds from clearing, the same machine colors and unprocessed individual-machine samples.

## Paper candidates and shared sources

| Figure | Data | PDF | Drawing command |
|---|---|---|---|
| Individual-machine A/B/C time responses | [A](../studies/paper/results/A/), [B](../studies/paper/results/B/), [C](../studies/paper/results/C/) | [PDF](../studies/paper/figures/paper/time_response_ABC.pdf) | `python studies/paper/scripts/plot.py --only time` |
| Conditional section A | [Point states, labels, paths](../studies/paper/results/fault_basins/A/) | [PDF](../studies/paper/figures/paper/basin_A.pdf) | `python studies/paper/scripts/plot.py --only basins` |
| Conditional section B | [Point states, labels, paths](../studies/paper/results/fault_basins/B/) | [PDF](../studies/paper/figures/paper/basin_B.pdf) | same |
| Conditional section C | [Point states, labels, paths](../studies/paper/results/fault_basins/C/) | [PDF](../studies/paper/figures/paper/basin_C.pdf) | same |
| System/scenario diagram | [Shared post-fault network](../studies/paper/results/power_flow/common_post_equilibrium/) | [PDF](../studies/paper/figures/paper/system.pdf) | `python studies/paper/scripts/power_flow.py` |

Inputs are [case rows](../studies/paper/inputs/cases.csv), [physical values](../studies/paper/inputs/common.toml), [main section](../studies/paper/inputs/fault_basin.toml), [local section](../studies/paper/inputs/local_basin.toml) and [presentation](../studies/paper/inputs/figures.toml). [Saved figure identities](../studies/paper/figures/catalog.toml) link every figure to its data. These commands draw into `outputs/figures/` and do not rewrite numeric results or validation baselines. [Full workflow guide](RUNNING.md).

## Main and additional responses

### A

![A responses](../studies/paper/figures/details/A_responses.png)

[PDF](../studies/paper/figures/details/A_responses.pdf) · [Observations](../studies/paper/results/A/observations.csv.gz) · [Native full states](../studies/paper/results/A/states.csv.gz) · [Input](../studies/paper/inputs/cases.csv) · [Plot code](../studies/paper/scripts/plot.py)

### B

![B responses](../studies/paper/figures/details/B_responses.png)

[PDF](../studies/paper/figures/details/B_responses.pdf) · [Observations](../studies/paper/results/B/observations.csv.gz) · [Native full states](../studies/paper/results/B/states.csv.gz) · [Input](../studies/paper/inputs/cases.csv) · [Plot code](../studies/paper/scripts/plot.py)

### C

![C responses](../studies/paper/figures/details/C_responses.png)

[PDF](../studies/paper/figures/details/C_responses.pdf) · [Observations](../studies/paper/results/C/observations.csv.gz) · [Native full states](../studies/paper/results/C/states.csv.gz) · [Input](../studies/paper/inputs/cases.csv) · [Plot code](../studies/paper/scripts/plot.py)

### C_D1_10

![C_D1_10 responses](../studies/paper/figures/details/C_D1_10_responses.png)

[PDF](../studies/paper/figures/details/C_D1_10_responses.pdf) · [Observations](../studies/paper/results/C_D1_10/observations.csv.gz) · [Native full states](../studies/paper/results/C_D1_10/states.csv.gz) · [Input](../studies/paper/inputs/cases.csv) · [Plot code](../studies/paper/scripts/plot.py)

![D1 comparison](../studies/paper/figures/details/C_D1_comparison.png)

[D₁ comparison PDF](../studies/paper/figures/details/C_D1_comparison.pdf): C versus C_D1_10, with only D₁ changed from 0 to 10. Red/blue distinguish the cases; line styles distinguish machines. This changes effective steady droop to 3.333…% as well as damping.

[Long 1000 s comparison PNG](../studies/paper/figures/details/time_response_ABC_long.png) · [PDF](../studies/paper/figures/details/time_response_ABC_long.pdf).

Recreate the above with `python studies/paper/scripts/plot.py --only time`.

## Phase-plane details

The main figures start at the actual pre-fault state and include the fault-on and post-fault paths. Wide views use a common −150 to 0 rad range to show the full first 30 s: A recovers, B/C continue negatively. Frequency limits, markers, stage colors and background match the main views.

| Case | First-30-s wide view | Separate local section diagnostic |
|---|---|---|
| A | [PNG](../studies/paper/figures/details/basin_A_wide.png) · [PDF](../studies/paper/figures/details/basin_A_wide.pdf) | [PNG](../studies/paper/figures/details/basin_local_A.png) · [PDF](../studies/paper/figures/details/basin_local_A.pdf) |
| B | [PNG](../studies/paper/figures/details/basin_B_wide.png) · [PDF](../studies/paper/figures/details/basin_B_wide.pdf) | [PNG](../studies/paper/figures/details/basin_local_B.png) · [PDF](../studies/paper/figures/details/basin_local_B.pdf) |
| C | [PNG](../studies/paper/figures/details/basin_C_wide.png) · [PDF](../studies/paper/figures/details/basin_C_wide.pdf) | [PNG](../studies/paper/figures/details/basin_local_C.png) · [PDF](../studies/paper/figures/details/basin_local_C.pdf) |

The 49-point local diagnostic uses rotated initial Vc/If/Ig, small coordinate ranges and section-launched curves. It is **not a magnification of the revised background**; its results are unchanged. [Definitions and differences](BASIN_VIEWS.md). Replot main/wide views with `python studies/paper/scripts/plot.py --only basins`, local diagnostics with `--only local-basins`. [Main input](../studies/paper/inputs/fault_basin.toml), [main data](../studies/paper/results/fault_basins/), [local data](../studies/paper/results/basins/).

## Equilibrium and matched-time dynamic power flow

The common pre/post equilibria are shared positions of the different controllers at ν=0; their local stability is checked separately for each controller. Dynamic diagrams show saved states, not equilibrium solutions. Every bus label includes terminal-voltage magnitude [pu] and principal phase [rad]. Every active branch lists signed P/Q from each end into the branch [pu]. Blue/green arrows denote P/Q.

| Case | Snapshot | PNG | PDF | Audited data |
|---|---|---|---|---|
| common | common_pre_equilibrium | [PNG](../studies/paper/figures/details/power_flow/common_pre_equilibrium.png) | [PDF](../studies/paper/figures/details/power_flow/common_pre_equilibrium.pdf) | [Data](../studies/paper/results/power_flow/common_pre_equilibrium/) |
| common | common_post_equilibrium | [PNG](../studies/paper/figures/details/power_flow/common_post_equilibrium.png) | [PDF](../studies/paper/figures/details/power_flow/common_post_equilibrium.pdf) | [Data](../studies/paper/results/power_flow/common_post_equilibrium/) |
| A | A_pre_equilibrium | [PNG](../studies/paper/figures/details/power_flow/A_pre_equilibrium.png) | [PDF](../studies/paper/figures/details/power_flow/A_pre_equilibrium.pdf) | [Shared data](../studies/paper/results/power_flow/common_pre_equilibrium/) |
| B | B_pre_equilibrium | [PNG](../studies/paper/figures/details/power_flow/B_pre_equilibrium.png) | [PDF](../studies/paper/figures/details/power_flow/B_pre_equilibrium.pdf) | [Shared data](../studies/paper/results/power_flow/common_pre_equilibrium/) |
| C | C_pre_equilibrium | [PNG](../studies/paper/figures/details/power_flow/C_pre_equilibrium.png) | [PDF](../studies/paper/figures/details/power_flow/C_pre_equilibrium.pdf) | [Shared data](../studies/paper/results/power_flow/common_pre_equilibrium/) |
| A | A_post_0s | [PNG](../studies/paper/figures/details/power_flow/A_post_0s.png) | [PDF](../studies/paper/figures/details/power_flow/A_post_0s.pdf) | [Data](../studies/paper/results/power_flow/A_post_0s/) |
| A | A_post_1s | [PNG](../studies/paper/figures/details/power_flow/A_post_1s.png) | [PDF](../studies/paper/figures/details/power_flow/A_post_1s.pdf) | [Data](../studies/paper/results/power_flow/A_post_1s/) |
| A | A_post_5s | [PNG](../studies/paper/figures/details/power_flow/A_post_5s.png) | [PDF](../studies/paper/figures/details/power_flow/A_post_5s.pdf) | [Data](../studies/paper/results/power_flow/A_post_5s/) |
| B | B_post_0s | [PNG](../studies/paper/figures/details/power_flow/B_post_0s.png) | [PDF](../studies/paper/figures/details/power_flow/B_post_0s.pdf) | [Data](../studies/paper/results/power_flow/B_post_0s/) |
| B | B_post_1s | [PNG](../studies/paper/figures/details/power_flow/B_post_1s.png) | [PDF](../studies/paper/figures/details/power_flow/B_post_1s.pdf) | [Data](../studies/paper/results/power_flow/B_post_1s/) |
| B | B_post_5s | [PNG](../studies/paper/figures/details/power_flow/B_post_5s.png) | [PDF](../studies/paper/figures/details/power_flow/B_post_5s.pdf) | [Data](../studies/paper/results/power_flow/B_post_5s/) |
| C | C_post_0s | [PNG](../studies/paper/figures/details/power_flow/C_post_0s.png) | [PDF](../studies/paper/figures/details/power_flow/C_post_0s.pdf) | [Data](../studies/paper/results/power_flow/C_post_0s/) |
| C | C_post_1s | [PNG](../studies/paper/figures/details/power_flow/C_post_1s.png) | [PDF](../studies/paper/figures/details/power_flow/C_post_1s.pdf) | [Data](../studies/paper/results/power_flow/C_post_1s/) |
| C | C_post_5s | [PNG](../studies/paper/figures/details/power_flow/C_post_5s.png) | [PDF](../studies/paper/figures/details/power_flow/C_post_5s.pdf) | [Data](../studies/paper/results/power_flow/C_post_5s/) |

The [paper-to-code map](paper-map.md) pairs each case's pre-fault view with its clearing+1 s snapshot. Pre-fault views share the canonical dataset and are checked against the saved observations of A/B/C separately. [Six-view index](../studies/paper/results/power_flow/comparison.csv), [validation](../studies/paper/results/validation/power_flow_comparison.json). Redraw only these six with `python studies/paper/scripts/plot_flow_comparison.py`.

Redraw all saved flows with `python studies/paper/scripts/power_flow.py`; run `python studies/paper/scripts/check_flows.py` for a new validation report; [flow processing](../src/flows.py), [single-line renderer](../src/network_plot.py), [network inputs](../studies/paper/inputs/common.toml). The plots distinguish equilibrium and dynamic time in their headers. Each data folder contains bus/line powers and `audit.json`, including current KCL, nodal complex-power and whole-network P/Q balance errors.
