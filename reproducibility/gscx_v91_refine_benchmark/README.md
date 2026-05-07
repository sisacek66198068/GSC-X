# GSC-X v9.1 Refined Cloud Benchmark

Cloud-scale refinement benchmark of the GSC-X nonlinear executive stabilization framework.

## Benchmark conditions

- delayed sensor feedback
- actuator lag
- stochastic noise
- nonlinear burst forcing
- multi-seed execution
- cloud parallel processing

## Simulation count

3000 simulations total

- PID baseline
- GSC-X v7
- GSC-X v9.1 refined EMA hardened architecture

## Key results

| Controller | Survival Rate | Mean Peak | Mean Unsafe Time | Mean Energy | Mean Productivity / Energy |
|---|---:|---:|---:|---:|---:|
| PID | 0% | 1.500719 | 4.599672 | 5.538983 | 0.699842 |
| GSC-X v7 | 100% | 0.031619 | 0.000000 | 0.292560 | 202.205323 |
| GSC-X v9.1 | 100% | 0.030251 | 0.000000 | 0.156543 | 381.358585 |

## Interpretation

GSC-X v9.1 improves over GSC-X v7 in this benchmark by combining EMA-based sensor filtering, predictive observer logic, reduced overreaction, and efficient nonlinear stabilization.

Cloud execution environment:

- Google Cloud Compute Engine
- Ubuntu 24.04
- 8 vCPU / 32 GB RAM
