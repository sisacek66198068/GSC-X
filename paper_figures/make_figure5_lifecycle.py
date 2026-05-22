import matplotlib.pyplot as plt

steps = ["SCAN", "DECIDE", "STABILIZE", "RECOVER", "ADAPT"]

fig, ax = plt.subplots(figsize=(10, 2.8))
ax.axis("off")

x_positions = range(len(steps))

for i, step in enumerate(steps):
    ax.text(
        i, 0.5, step,
        ha="center", va="center",
        fontsize=15,
        bbox=dict(boxstyle="round,pad=0.45", linewidth=1.4, facecolor="white")
    )

    if i < len(steps) - 1:
        ax.annotate(
            "",
            xy=(i + 0.72, 0.5),
            xytext=(i + 0.28, 0.5),
            arrowprops=dict(arrowstyle="->", linewidth=1.6)
        )

ax.set_xlim(-0.6, len(steps) - 0.4)
ax.set_ylim(0, 1)

plt.title("GDS-GSC-X Executive Stabilization Lifecycle", fontsize=16)
plt.tight_layout()

plt.savefig("paper_figures/output/fig05_lifecycle_architecture.png", dpi=300)
plt.savefig("paper_figures/output/fig05_lifecycle_architecture.pdf")

print("SAVED:")
print("paper_figures/output/fig05_lifecycle_architecture.png")
print("paper_figures/output/fig05_lifecycle_architecture.pdf")
