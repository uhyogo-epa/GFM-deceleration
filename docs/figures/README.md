# Drawing scripts

Diagrams that need no simulation results. Each script is named after the files it writes, and writes them next to itself by default (`--output <dir>` for a preview elsewhere). Run from the repository root.

| Script | Output | Content |
|---|---|---|
| [`system.py`](system.py) | `system.pdf`, `system.svg`, `system.png` | Manuscript Fig. 1: pre-fault eight-bus network and the common GFM model ([guide](../figure1.md)) |
| [`control_diagrams.py`](control_diagrams.py) | `control_diagrams/*.png` | Detailed Droop, VSM and shared inner-control block diagrams |

`system.py` reads only the branch list in `studies/inputs/study.toml`, to check that the drawn topology matches the study. `control_diagrams.py` reads no files.
