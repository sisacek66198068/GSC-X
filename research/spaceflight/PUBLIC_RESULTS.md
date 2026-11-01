# Spaceflight — Public Validation Results

## English

Selected numerical research results from the GSC-X
validation environment. Results are reported as recorded
in the original CSV files.

These datasets do not independently establish
real-world deployment performance.

## Česky

Vybrané numerické výsledky z validačního prostředí GSC-X.
Hodnoty jsou převzaty z původních CSV souborů.

Samotná data nedokazují funkčnost v reálném provozu.

## v62_kernel_N3000_FAST_summary.csv

**Records / Záznamy:** 3000

**Dataset:** [CSV](results/v62_kernel_N3000_FAST_summary.csv)

**Columns / Sloupce:**

`seed`, `nominal_MRI`, `degraded_MRI`, `failure_MRI`, `recovery_MRI`, `max_MRI`, `fragile_t`, `low_reserve_t`, `critical_t`, `authority_truth_event_t`, `fragile_lead`, `low_reserve_lead`, `critical_lead`

Full results are provided in the linked CSV.

Úplné výsledky jsou v přiloženém CSV.

**Interpretation / Interpretace:**

Metric definitions, experimental conditions and
comparative baselines must be considered before
drawing scientific conclusions.

Při interpretaci je nutné zohlednit definice metrik,
experimentální podmínky a referenční metody.

## spacefly_true_hard_v3_summary.csv

**Records / Záznamy:** 2

**Dataset:** [CSV](results/spacefly_true_hard_v3_summary.csv)

**Columns / Sloupce:**

`controller`, `unsafe_time`, `control_energy`, `mean_pointing_error_deg`, `wheel_load`, `max_angle_deg`, `productivity`

### Recorded metrics / Zaznamenané metriky

| controller | unsafe_time | control_energy | mean_pointing_error_deg | wheel_load | max_angle_deg | productivity |
| --- | --- | --- | --- | --- | --- | --- |
| PID | 0 | 0.285379 | 0.787739 | 1.45982 | 9.89458 | 0.608782 |
| GSCX | 0 | 0.228935 | 1.33537 | 1.21302 | 11.1659 | 0.584487 |

**Interpretation / Interpretace:**

Metric definitions, experimental conditions and
comparative baselines must be considered before
drawing scientific conclusions.

Při interpretaci je nutné zohlednit definice metrik,
experimentální podmínky a referenční metody.

## spacefly_failure_v53_summary.csv

**Records / Záznamy:** 2

**Dataset:** [CSV](results/spacefly_failure_v53_summary.csv)

**Columns / Sloupce:**

`controller`, `unsafe_time`, `control_energy`, `pointing_error`, `wheel_load`, `fuel_used`, `sat_fraction`, `productivity`

### Recorded metrics / Zaznamenané metriky

| controller | unsafe_time | control_energy | pointing_error | wheel_load | fuel_used | sat_fraction | productivity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PID | 0 | 0.295587 | 0.760821 | 1.28281 | 3074.11 | 0 | 0.517042 |
| GSCX | 0 | 0.268788 | 2.371 | 1.42759 | 2795.4 | 0 | 0.481108 |

**Interpretation / Interpretace:**

Metric definitions, experimental conditions and
comparative baselines must be considered before
drawing scientific conclusions.

Při interpretaci je nutné zohlednit definice metrik,
experimentální podmínky a referenční metody.

## spacefly_resource_v4_summary.csv

**Records / Záznamy:** 2

**Dataset:** [CSV](results/spacefly_resource_v4_summary.csv)

**Columns / Sloupce:**

`controller`, `unsafe_time`, `control_energy`, `mean_pointing_error_deg`, `wheel_load`, `fuel_used`, `sat_fraction`, `productivity`

### Recorded metrics / Zaznamenané metriky

| controller | unsafe_time | control_energy | mean_pointing_error_deg | wheel_load | fuel_used | sat_fraction | productivity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PID | 0 | 0.079112 | 0.728114 | 1.49163 | 664.54 | 0 | 0.701063 |
| GSCX | 0 | 0.0529902 | 0.8787 | 0.698695 | 445.118 | 0 | 0.76776 |

**Interpretation / Interpretace:**

Metric definitions, experimental conditions and
comparative baselines must be considered before
drawing scientific conclusions.

Při interpretaci je nutné zohlednit definice metrik,
experimentální podmínky a referenční metody.
