# Internet — Public Validation Results

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

## internet_results_summary.csv

**Records / Záznamy:** 3

**Dataset:** [CSV](results/internet_results_summary.csv)

**Columns / Sloupce:**

`domain`, `scenario`, `validation_class`, `metric_family`, `status`, `implementation_public`

### Recorded metrics / Zaznamenané metriky

| domain | scenario | validation_class | metric_family | status | implementation_public |
| --- | --- | --- | --- | --- | --- |
| internet | viral_event | TRUE_N10000 | availability_latency_energy_dropped_requests | validated | no |
| internet | datacenter_failure | TRUE_N10000 | availability_latency_energy_dropped_requests | validated | no |
| internet | compound_crisis | TRUE_N10000 | availability_latency_energy_dropped_requests | validated | no |

**Interpretation / Interpretace:**

Metric definitions, experimental conditions and
comparative baselines must be considered before
drawing scientific conclusions.

Při interpretaci je nutné zohlednit definice metrik,
experimentální podmínky a referenční metody.
