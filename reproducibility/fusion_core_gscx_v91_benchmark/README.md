# Fusion-Core GSC-X v9.1 Cloud Benchmark

Cloud-scale fusion-core proxy benchmark comparing PID, GSC-X v7, and GSC-X v9.1.

## Benchmark conditions

- delayed sensor feedback
- actuator lag
- stochastic noise
- nonlinear burst forcing
- plasma-like instability amplitude
- normalized core temperature
- normalized density dynamics
- fusion yield proxy
- multi-seed cloud execution

## Simulation count

3000 simulations total

- PID baseline
- GSC-X v7
- GSC-X v9.1 refined EMA hardened architecture

## Key results

| Controller | Survival Rate | Mean Peak A | Mean Min Temp | Mean Max Density | Mean Unsafe Time | Mean Control Energy | Mean Fusion Yield | Mean Yield / Energy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| PID | 0% | 1.550682 | 0.788711 | 1.128878 | 4.420085 | 5.592485 | 3.176829 | 0.575233 |
| GSC-X v7 | 100% | 0.031458 | 0.966654 | 1.139358 | 0.000000 | 0.290297 | 59.624070 | 205.546797 |
| GSC-X v9.1 | 100% | 0.027041 | 0.980345 | 1.133183 | 0.000000 | 0.182335 | 61.445366 | 337.548384 |

## Interpretation

GSC-X v9.1 outperformed both PID and GSC-X v7 in this fusion-core proxy benchmark.

Compared with GSC-X v7, v9.1 achieved:

- lower instability peak
- higher retained core temperature
- lower control energy
- higher fusion yield
- substantially higher yield per unit energy

Cloud execution environment:

- Google Cloud Compute Engine
- Ubuntu 24.04
- 8 vCPU / 32 GB RAM
