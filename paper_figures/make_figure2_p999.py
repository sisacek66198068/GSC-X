import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("paper_figures/data/figure2_p999.csv")

plt.figure(figsize=(7, 5))
plt.bar(df["architecture"], df["p999"])

plt.ylabel("p999 Runaway Cycles")
plt.xlabel("Control Architecture")
plt.title("Catastrophic Tail Suppression under GDS-GSC-X")

for i, v in enumerate(df["p999"]):
    plt.text(i, v + 5, str(v), ha="center", va="bottom", fontsize=11)

plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig("paper_figures/output/fig02_p999_tail_suppression.png", dpi=300)
plt.savefig("paper_figures/output/fig02_p999_tail_suppression.pdf")

print("SAVED:")
print("paper_figures/output/fig02_p999_tail_suppression.png")
print("paper_figures/output/fig02_p999_tail_suppression.pdf")
