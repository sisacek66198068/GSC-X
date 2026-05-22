import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("muon_gscx_results.csv")

plt.figure(figsize=(8, 5))

for name, label in [
    ("baseline", "Baseline"),
    ("linear", "Linear"),
    ("gscx", "GDS-GSC-X"),
]:
    x = df[df["controller"] == name]["cycles"]
    plt.hist(x, bins=45, density=True, alpha=0.45, label=label)

plt.xlabel("Runaway Cycles")
plt.ylabel("Probability Density")
plt.title("Distribution of Runaway Dynamics under Adaptive Stabilization")
plt.legend()
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig("paper_figures/output/fig03_distribution_histogram.png", dpi=300)
plt.savefig("paper_figures/output/fig03_distribution_histogram.pdf")

print("SAVED:")
print("paper_figures/output/fig03_distribution_histogram.png")
print("paper_figures/output/fig03_distribution_histogram.pdf")
