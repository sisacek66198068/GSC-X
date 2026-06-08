# GSC-X Fusion Štěpánů Trio TRUE N1,000,000 Validation

This folder contains the million-run validation of the Fusion PTM / Štěpánů Trio branch.

## Validation ladder

- N = 3,000
- N = 10,000
- N = 100,000
- N = 1,000,000

Across all validation scales, the ordering remained stable:

1. TREND_ONLY
2. MEMORY_TREND
3. TRIO_ELI_HEAVY

## TRUE N1,000,000 Results

| Variant | Survival Rate | Unsafe Time | Control Energy | Yield/Energy | Persistence Proxy |
|---|---:|---:|---:|---:|---:|
| TREND_ONLY | 1.0 | 0.331781 | 3.570420 | 101.170398 | 3.014038 |
| MEMORY_TREND | 1.0 | 0.332312 | 3.730337 | 96.954611 | 3.009218 |
| TRIO_ELI_HEAVY | 1.0 | 0.333476 | 3.606404 | 100.205002 | 2.998714 |

## PTM Findings

Fusion PTM V1 revealed a recurring cycle:

Build-up → Detection → Recovery → Persistence → Release

Key PTM metrics:

- Predictive Lead Median: 22 steps
- Predictive Lead Mean: 27.6 steps
- Recovery Median: 0 steps
- Persistence Median: 2 steps
- Longest Persistence Event: 44 steps
- Longest Trigger Event: 58 steps

## Interpretation

The Fusion Sandbox branch demonstrates robust predictive stability behavior in a nonlinear plasma-like simulation environment.  
This does not represent a physical reactor validation, but it provides a statistically strong simulation-level validation of the GSC-X Fusion PTM architecture.

## Author

Martin Štěpánů  
Independent Researcher  
ORCID: 0009-0007-0409-6037  
https://gds-gsc-x.com  
