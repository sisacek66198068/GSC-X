# Battery — Public Validation Results

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

## battery_synthetic_true_n3000_summary.csv

**Records / Záznamy:** 2

**Dataset:** [CSV](results/battery_synthetic_true_n3000_summary.csv)

**Columns / Sloupce:**

`controller`, `detection_rate`, `missed_events`, `false_alarm_rate`, `mean_warning_lead_percent`, `median_warning_lead_percent`, `mean_peak_temperature`, `mean_final_degradation`, `mean_unsafe_time`, `mean_energy_stress`

### Recorded metrics / Zaznamenané metriky

| controller | detection_rate | missed_events | false_alarm_rate | mean_warning_lead_percent | median_warning_lead_percent | mean_peak_temperature | mean_final_degradation | mean_unsafe_time | mean_energy_stress |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BASELINE_BMS | 1 | 0 | 0.408667 | 2.90789 | 0 | 48.228 | 0.549234 | 0.0171328 | 0.00631882 |
| GSCX_BATTERY | 1 | 0 | 0.678667 | 2.71189 | 0 | 45.4909 | 0.510326 | 0.00592444 | 0.0498889 |

**Interpretation / Interpretace:**

Metric definitions, experimental conditions and
comparative baselines must be considered before
drawing scientific conclusions.

Při interpretaci je nutné zohlednit definice metrik,
experimentální podmínky a referenční metody.
