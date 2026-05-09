# GSC-X v9.1 TRUE N3000 Endurance Confirmation Benchmark

## Run size

9000 total simulations:

- 3000 seeds
- 3 controllers
- 8 workers

## Result summary

| Controller | Survival Rate | Mean Peak A | Mean Unsafe Time | Mean Control Energy | Mean Fusion Yield | Mean Yield / Energy |
|---|---:|---:|---:|---:|---:|---:|
| GSCX_V7 | 1.0 | 0.031473 | 0.000000 | 0.790055 | 173.355159 | 219.479964 |
| GSCX_V91 | 1.0 | 0.027072 | 0.000000 | 0.512124 | 180.712423 | 353.021120 |
| PID | 0.0 | 1.550688 | 4.433643 | 5.629628 | 3.182115 | 0.572013 |

## Interpretation

GSCX_V91 achieved full survival, zero unsafe time, lower peak instability, lower control energy, and approximately 617x higher yield per energy than PID in the TRUE N3000 endurance confirmation benchmark.

