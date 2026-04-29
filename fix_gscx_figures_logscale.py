import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs("figs_gscx_fixed", exist_ok=True)

metrics = {
    "Unsafe Time": (75.381753, 0.088132),
    "Control Energy": (640.067811, 34.206901),
    "Fusion Yield": (7.448265, 82.950407),
    "Yield per Energy": (0.011641, 2.624227),
}

for name, (pid, gsc) in metrics.items():
    fig, ax = plt.subplots(figsize=(7,4))

    values = [max(pid, 1e-6), max(gsc, 1e-6)]

    ax.bar(["PID", "GSC-X"], values)
    ax.set_yscale("log")
    ax.set_title(f"{name} Comparison (Log Scale)")
    ax.set_ylabel(name)
    ax.grid(axis="y", alpha=0.3)

    for i, v in enumerate(values):
        ax.text(i, v, f"{v:.4g}", ha="center", va="bottom")

    plt.tight_layout()
    filename = name.lower().replace(" ", "_")
    plt.savefig(f"figs_gscx_fixed/{filename}_log.png", dpi=220)
    plt.close()

print("DONE: fixed log-scale figures saved in figs_gscx_fixed/")
