# Nuclear — Public Validation Results

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

## nuclear_transmutation_v3_summary.csv

**Records / Záznamy:** 8

**Dataset:** [CSV](results/nuclear_transmutation_v3_summary.csv)

**Columns / Sloupce:**

`mode`, `runs`, `mean_toxicity_reduction`, `median_toxicity_reduction`, `mean_remaining_fraction`, `mean_converted_mass_proxy`, `mean_energy`, `mean_yield_per_energy`, `mean_unsafe_time`, `mean_interventions`, `score`

### Recorded metrics / Zaznamenané metriky

| mode | runs | mean_toxicity_reduction | median_toxicity_reduction | mean_remaining_fraction | mean_converted_mass_proxy | mean_energy | mean_yield_per_energy | mean_unsafe_time | mean_interventions | score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FAST_HYBRID | 10000 | 0.341591 | 0.341647 | 0.658409 | 1.71014 | 116.924 | 0.0146339 | 0 | 40.1309 | 4.64545 |
| ADS_HYBRID | 10000 | 0.323956 | 0.323979 | 0.676044 | 1.62275 | 113.962 | 0.014246 | 0 | 53.8262 | 4.43624 |
| ADS | 10000 | 0.365451 | 0.365469 | 0.634549 | 1.82929 | 181.771 | 0.0100702 | 0.0003 | 260 | 4.29797 |
| GSCX_MSR_HYBRID | 10000 | 0.236769 | 0.236836 | 0.763231 | 1.18796 | 60.8179 | 0.0195467 | 0 | 28.9763 | 4.20072 |
| GSCX_CM_ELI | 10000 | 0.259757 | 0.259966 | 0.740243 | 1.30312 | 78.7882 | 0.0165683 | 0 | 54.4181 | 4.09683 |
| MSR | 10000 | 0.241591 | 0.241848 | 0.758409 | 1.21249 | 68.9507 | 0.0175964 | 0 | 0 | 4.03765 |
| BASE | 10000 | 0.231141 | 0.231094 | 0.768859 | 1.1601 | 72.5784 | 0.015999 | 0 | 0 | 3.76615 |
| FAST | 10000 | 0.396142 | 0.396272 | 0.603858 | 1.98258 | 329.131 | 0.00603035 | 116.664 | 260 | -1.92702 |

**Interpretation / Interpretace:**

Metric definitions, experimental conditions and
comparative baselines must be considered before
drawing scientific conclusions.

Při interpretaci je nutné zohlednit definice metrik,
experimentální podmínky a referenční metody.
