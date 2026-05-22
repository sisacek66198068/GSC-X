import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("muon_corridor_sweep_results.csv")

pivot = df.pivot_table(
    values="p999",
    index="cooldown",
    columns="quarantine",
    aggfunc="mean"
)

plt.figure(figsize=(7, 6))

im = plt.imshow(
    pivot,
    origin="lower",
    aspect="auto"
)

plt.colorbar(im, label="p999 Runaway Cycles")

plt.xticks(
    range(len(pivot.columns)),
    [f"{x:.2f}" for x in pivot.columns]
)

plt.yticks(
    range(len(pivot.index)),
    [f"{y:.2f}" for y in pivot.index]
)

plt.xlabel("Quarantine Parameter")
plt.ylabel("Cooldown Parameter")

plt.title(
    "Emergent Metastability Corridors under GDS-GSC-X"
)

plt.tight_layout()

plt.savefig(
    "paper_figures/output/fig04_corridor_heatmap.png",
    dpi=300
)

plt.savefig(
    "paper_figures/output/fig04_corridor_heatmap.pdf"
)

print("SAVED:")
print("paper_figures/output/fig04_corridor_heatmap.png")
print("paper_figures/output/fig04_corridor_heatmap.pdf")
