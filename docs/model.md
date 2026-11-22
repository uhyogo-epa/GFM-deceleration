# Model and implementation

The balanced averaged model describes four grid-forming inverters at buses 1, 2, 3, and 7 of an eight-bus network. Bus 6 is a fixed 60 Hz slack. Bus 5 contains a constant-impedance load and a parallel capacitor. PWM and DC-source dynamics are outside the model.

## Equation-to-code map

| Model element | Implementation | Supporting description |
|---|---|---|
| Parameters, units, native states, and coordinates | [model.jl](../src/model.jl) | [Parameter and state definitions](PARAMETERS.md) |
| Network admittance and algebraic-voltage elimination | [network.jl](../src/network.jl) | [Numerical validation](VALIDATION.md) |
| LCL filter, dq transformations, PI loops, and circular current-command limiter | `machine` and `rhs!` in [dynamics.jl](../src/dynamics.jl) | [Third-party components](third-party.md) |
| Droop power filter and VSM swing/washout dynamics | Control branches in [dynamics.jl](../src/dynamics.jl) | [Parameters and outer-control equations](PARAMETERS.md) |
| Equilibria, observations, Jacobian, and eigenvalues | [equilibria.jl](../src/equilibria.jl) | [Validation](VALIDATION.md) |
| Fault application, clearing, and integration | [simulation.jl](../src/simulation.jl) | [Physical and numerical settings](../studies/inputs/) |
| Section initialization and finite-time classifications | [sections.jl](../src/sections.jl), [analysis.jl](../src/analysis.jl) | [Section definitions](BASIN_VIEWS.md) |

Active power is measured at filter-capacitor voltage and grid-side filter current, `P + jQ = Vc conj(Ig)`; positive power denotes inverter injection. Internal angles are unwrapped relative to the fixed slack. The circular limiter acts on the current command, rather than imposing an instantaneous bound on physical filter currents.

## Outer-control equations

Let `nu = (omega - omega0)/omega0`, with `omega0 = 2 pi 60`. The internal angle satisfies `d(delta)/dt = omega0 nu`.

```math
\text{Droop:}\qquad \tau_p \dot P_f=P-P_f,\qquad \nu=m_p(P^*-P_f).
```

```math
\text{VSM:}\qquad 2H\dot\nu=P^*-P-(1/m_p+D_1)\nu-D_2(\nu-z),\qquad \dot z=\omega_D(\nu-z).
```

Both controls use `tau_q d(Qf)/dt = Q - Qf` and `Vref = Vset - Kq (Qf - Qset)`. With `D1 = D2 = 0`, the coordinate transformation `nu = mp (Pset - Pf)` gives the equivalence `2H = tau_p/mp`; this is an equation identity, rather than independent physical validation.

| Case | Control | Main settings |
|---|---|---|
| A | Droop | `mp = 0.05`, `tau_p = 0.02 s` |
| B | Droop | `mp = 0.05`, `tau_p = 1.00 s` |
| C | VSM | `mp = 0.05`, `H = 2.5 s`, `D1 = 0`, `D2 = 100`, `omega_D = 50 s^-1` |

The common fault is applied at Bus 4 at absolute time 1.00 s and cleared at 1.15 s, when line 4–5 opens. Canonical values are in [common.toml](../studies/inputs/common.toml), [cases.csv](../studies/inputs/cases.csv), and [study.toml](../studies/inputs/study.toml).

## What still needs to be documented

This is the initial documentation structure. Subsequent model documentation will connect each circuit and controller equation to its derivation or source, per-unit conventions, code variables, and a numerical consistency check. The existing parameter and validation documents remain the detailed reference during this work.

Conditional phase-plane classifications describe specified initial-state sections over 1000 s. Their projections do not establish a full attraction boundary or asymptotic stability of rotation.
