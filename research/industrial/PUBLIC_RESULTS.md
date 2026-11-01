# Industrial — Public Validation Results

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

## hard_delay_factory_v1_summary.csv

**Records / Záznamy:** 8

**Dataset:** [CSV](results/hard_delay_factory_v1_summary.csv)

**Columns / Sloupce:**

`delay_case`, `controller`, `survival`, `unsafe`, `energy`, `productivity`, `max_state`

### Recorded metrics / Zaznamenané metriky

| delay_case | controller | survival | unsafe | energy | productivity | max_state |
| --- | --- | --- | --- | --- | --- | --- |
| BRUTAL_300ms | GSCX_V91 | 1 | 24.5091 | 56.3721 | 1.26904 | 2.12503 |
| BRUTAL_300ms | PID | 0.8802 | 35.3447 | 87.1467 | 0.488874 | 2.89226 |
| EASY_10ms | GSCX_V91 | 1 | 0 | 9.51734 | 12.0876 | 1.11868 |
| EASY_10ms | PID | 1 | 0 | 11.7952 | 10.003 | 1.10059 |
| HARD_150ms | GSCX_V91 | 1 | 0 | 9.86846 | 11.6479 | 1.13137 |
| HARD_150ms | PID | 1 | 1.04323 | 43.0414 | 2.42389 | 1.56354 |
| MEDIUM_50ms | GSCX_V91 | 1 | 0 | 9.55958 | 12.0326 | 1.12148 |
| MEDIUM_50ms | PID | 1 | 0 | 11.9178 | 9.89174 | 1.10544 |

**Interpretation / Interpretace:**

Metric definitions, experimental conditions and
comparative baselines must be considered before
drawing scientific conclusions.

Při interpretaci je nutné zohlednit definice metrik,
experimentální podmínky a referenční metody.

## industrial_productivity_v1_summary.csv

**Records / Záznamy:** 3

**Dataset:** [CSV](results/industrial_productivity_v1_summary.csv)

**Columns / Sloupce:**

`controller`, `survival`, `unsafe`, `energy`, `productivity`, `max_state`

### Recorded metrics / Zaznamenané metriky

| controller | survival | unsafe | energy | productivity | max_state |
| --- | --- | --- | --- | --- | --- |
| GSCX_PROD | 1 | 26.0124 | 77.0695 | 1.5965 | 1.90949 |
| GSCX_V91 | 1 | 18.2565 | 67.543 | 2.09477 | 1.8208 |
| PID | 1 | 57.0709 | 145.386 | 0.42467 | 2.5351 |

**Interpretation / Interpretace:**

Metric definitions, experimental conditions and
comparative baselines must be considered before
drawing scientific conclusions.

Při interpretaci je nutné zohlednit definice metrik,
experimentální podmínky a referenční metody.
