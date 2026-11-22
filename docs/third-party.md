# Third-party components

The LCL filter, dq transformations, PI-controller equations and DroopOuter derive from [PowerDynamics.jl](https://github.com/JuliaEnergy/PowerDynamics.jl), version 4.4.0, registered source tree `b2c2d56c664c475b4dbb19280b8420c5b0d68f30`. The supplied model uses a recorded 60 Hz nominal-frequency adaptation.

The derived electrical and inner-control equations are implemented in [dynamics.jl](../src/dynamics.jl); their parameter definitions and coordinate conventions are in [model.jl](../src/model.jl). The shared electrical/PI path is distinct from the Droop and VSM outer-control branches in `rhs!`. Source hashes and coefficient mapping remain in the [technical audit records](../studies/paper/provenance/).

The complete upstream copyright and license notices are retained in [PowerDynamics.txt](licenses/PowerDynamics.txt). This notice does not assign a license to the repository as a whole.
