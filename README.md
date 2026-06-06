## Interactive Public Sandboxes

Industrial Sandbox:  
https://sandbox.gds-gsc-x.com

Fusion Sandbox:  
https://fusion.gds-gsc-x.com

Research Website:  
https://gds-gsc-x.com

Publication (Zenodo DOI):  
https://doi.org/10.5281/zenodo.20156104

## Aerospace Validation (TRUE N10000 Confirmed)

The first aerospace validation branch of GSC-X has been completed and independently confirmed using large-scale TRUE N10000 validation runs.

### Validation Scope

* Flight Stabilization
* Damage Recovery
* Guidance HARD
* Waypoint Navigation
* Rocket Guidance
* Gymnasium LunarLander

### Key Results

| Benchmark                       | Result                                                                |
| ------------------------------- | --------------------------------------------------------------------- |
| Guidance HARD TRUE N10000       | 18.18× lower median guidance error than PID                           |
| Waypoint Navigation TRUE N10000 | 3.57× lower median final error than PID                               |
| Rocket TRUE Validation          | 4.34× lower median final error and 9.43× higher productivity than PID |
| LunarLander Smoke Validation    | Crash rate reduced from 51.5% to 7.1%                                 |

### Validation Artifacts

Report:

`reports/aerospace_v1/AEROSPACE_VALIDATION_V1.md`

Summary:

`reports/aerospace_v1/RESULTS_SUMMARY.csv`

### Interpretation

The aerospace validation campaign indicates that the Guidance Layer transformed GSC-X from a stabilization-oriented controller into a trajectory-capable controller.

The strongest confirmed results were obtained in delayed and disturbed guidance tasks, waypoint navigation, and rocket ascent control.

These results represent offline simulation validation and form the basis for the next phase:

* JSBSim aircraft validation
* UAV/F16 scenarios
* NASA open-source simulation environments
* Hardware-in-the-loop validation

## GSC-X v9.1 Endurance Benchmark

A 900-run fusion-core endurance benchmark was completed for GSC-X v9.1 against GSC-X v7 and PID.

| Controller | Survival Rate | Mean Peak A | Unsafe Time | Control Energy | Fusion Yield | Yield / Energy |
|---|---:|---:|---:|---:|---:|---:|
| GSC-X v9.1 | 1.000 | 0.02736 | 0.00000 | 0.51175 | 180.723 | 353.303 |
| GSC-X v7 | 1.000 | 0.03150 | 0.00000 | 0.78932 | 173.363 | 219.689 |
| PID | 0.000 | 1.55067 | 4.33259 | 5.55964 | 3.225 | 0.586 |

### Key Result

GSC-X v9.1 achieved 100% survival, zero unsafe operational time, lower control energy than v7, higher fusion yield than v7, and approximately 600× higher productivity per unit energy than PID.

Benchmark artifacts are stored in:

`frozen/v91_endurance/`

