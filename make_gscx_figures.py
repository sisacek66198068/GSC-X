import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs("figs_gscx", exist_ok=True)

metrics = {
    "Survival Rate": (0.000, 0.924),
    "Mean Peak Instability": (1.301772, 0.623390),
    "Mean Minimum Core Stability": (0.000088, 0.826780),
    "Mean Unsafe Time": (75.381753, 0.088132),
    "Mean Control Energy": (640.067811, 34.206901),
    "Mean Fusion Yield": (7.448265, 82.950407),
    "Yield per Energy": (0.011641, 2.624227),
}

def bar_plot(filename, title, ylabel, pid, gsc):
    fig, ax = plt.subplots(figsize=(6,4))
    ax.bar(["PID", "GSC-X"], [pid, gsc])
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", alpha=0.3)
    for i, v in enumerate([pid, gsc]):
        ax.text(i, v, f"{v:.4g}", ha="center", va="bottom")
    plt.tight_layout()
    plt.savefig(f"figs_gscx/{filename}", dpi=220)
    plt.close()

bar_plot("fig01_survival_rate.png", "Final Boss v4: Survival Rate", "Survival rate", *metrics["Survival Rate"])
bar_plot("fig02_unsafe_time.png", "Final Boss v4: Unsafe Operational Time", "Unsafe time", *metrics["Mean Unsafe Time"])
bar_plot("fig03_control_energy.png", "Final Boss v4: Control Energy", "Control energy", *metrics["Mean Control Energy"])
bar_plot("fig04_fusion_yield.png", "Final Boss v4: Fusion Yield", "Fusion yield", *metrics["Mean Fusion Yield"])
bar_plot("fig05_yield_per_energy.png", "Final Boss v4: Productivity per Energy", "Yield per energy", *metrics["Yield per Energy"])
bar_plot("fig06_peak_instability.png", "Final Boss v4: Peak Instability", "Peak instability", *metrics["Mean Peak Instability"])
bar_plot("fig07_core_stability.png", "Final Boss v4: Minimum Core Stability", "Minimum core stability", *metrics["Mean Minimum Core Stability"])

print("DONE: figures saved in /home/taka/GSC-X/figs_gscx/")
