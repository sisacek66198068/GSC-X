import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from multiprocessing import Pool, cpu_count

DT = 0.001
T = 180.0
N_STEPS = int(T / DT)
SEEDS = 300

A_CRIT = 0.60
A_COLLAPSE = 1.55

SENSOR_DELAY = 0.015
ACTUATOR_LAG = 0.020
NOISE_SIGMA = 0.045

DELAY_STEPS = max(1, int(SENSOR_DELAY / DT))
LAG_ALPHA = DT / (ACTUATOR_LAG + DT)

def burst_profile(t):
    bursts = [
        (8.0, 9.0, 2.2),
        (18.0, 19.5, 2.6),
        (31.0, 32.2, 3.0),
        (44.0, 45.0, 2.8),
        (53.0, 54.0, 3.2),
    ]
    return sum(amp for a, b, amp in bursts if a <= t <= b)

def simulate(controller, seed):
    rng = np.random.default_rng(seed)

    # Plasma-like state
    A = 0.02          # MHD instability amplitude
    Temp = 1.00      # normalized core temperature
    dens = 1.00      # normalized density
    u_applied = 0.0

    integral = 0.0
    raw_hist = [A] * (DELAY_STEPS + 2)

    ema = A
    ema_prev = A
    persistence = 0.0
    memory = 0.0

    peak_A = abs(A)
    min_temp = Temp
    max_dens = dens
    unsafe_time = 0.0
    control_energy = 0.0
    fusion_yield = 0.0
    collapsed = False
    collapse_time = np.nan

    for i in range(N_STEPS):
        t = i * DT
        burst = burst_profile(t)

        # Sensor
        raw_hist.append(A)
        delayed_A = raw_hist[-DELAY_STEPS]
        A_raw = delayed_A + rng.normal(0.0, NOISE_SIGMA)
        d_raw = (A_raw - raw_hist[-DELAY_STEPS - 1]) / DT

        if controller == "PID":
            Kp, Ki, Kd = 7.5, 0.22, 1.6
            integral = np.clip(integral + A_raw * DT, -1.0, 1.0)
            u_cmd = -Kp * A_raw - Ki * integral - Kd * d_raw
            u_cmd = np.clip(u_cmd, -5.0, 5.0)

        elif controller == "GSCX_V7":
            Gamma, alpha_nl, Ki = 5.4, 2.8, 0.035
            integral = np.clip(integral + A_raw * DT, -0.8, 0.8)
            risk = abs(A_raw) + 0.15 * max(0.0, d_raw)

            mode_gain = 1.0
            if risk > 0.40:
                mode_gain = 1.35
            if risk > 0.55:
                mode_gain = 1.75
            if risk > 0.75:
                mode_gain = 2.25

            u_cmd = -mode_gain * Gamma * A_raw * (1.0 + alpha_nl * A_raw * A_raw) - Ki * integral
            u_cmd = np.clip(u_cmd, -7.0, 7.0)

        elif controller == "GSCX_V91":
            d_ema_probe = (ema - ema_prev) / DT
            alpha_ema = 0.035 + 0.12 * min(1.0, abs(d_ema_probe) / 8.0)
            alpha_ema = np.clip(alpha_ema, 0.025, 0.18)

            ema_prev = ema
            ema = alpha_ema * A_raw + (1.0 - alpha_ema) * ema
            d_ema = (ema - ema_prev) / DT

            A_pred = ema + 0.012 * d_ema

            if abs(A_pred) > 0.42:
                persistence += DT
            else:
                persistence = max(0.0, persistence - 2.0 * DT)

            memory = 0.995 * memory + 0.005 * max(0.0, abs(A_pred) - 0.35)

            raw_emergency = abs(A_raw) > 0.95
            risk = abs(A_pred) + 0.10 * max(0.0, d_ema) + 0.38 * persistence + 0.20 * memory

            mode_gain = 0.95
            if risk > 0.45:
                mode_gain = 1.25
            if risk > 0.65:
                mode_gain = 1.60
            if risk > 0.85:
                mode_gain = 2.05
            if raw_emergency:
                mode_gain = 1.95

            Gamma, alpha_nl, Ki = 5.15, 2.45, 0.030
            integral = np.clip(integral + ema * DT, -0.7, 0.7)
            u_cmd = -mode_gain * Gamma * A_pred * (1.0 + alpha_nl * A_pred * A_pred) - Ki * integral
            u_cmd = np.clip(u_cmd, -6.5, 6.5)

        else:
            raise ValueError(controller)

        # actuator lag
        u_applied += LAG_ALPHA * (u_cmd - u_applied)

        # Plasma core dynamics
        gamma_mhd = 1.10 + burst + 0.20 * max(0.0, dens - 1.0) - 0.15 * max(0.0, Temp - 1.0)
        eta = 1.0

        dA = gamma_mhd * A - eta * A**3 + u_applied
        A += DT * dA

        # Control cools and disturbs the plasma slightly; instability degrades temperature
        Temp += DT * (0.018 * (1.0 - Temp) - 0.040 * abs(A) - 0.006 * abs(u_applied))
        dens += DT * (0.012 * burst + 0.030 * abs(A) - 0.018 * (dens - 1.0) - 0.004 * abs(u_applied))

        Temp = max(0.0, Temp)
        dens = max(0.0, dens)

        # Fusion yield proxy: wants high temperature and density, penalizes instability
        yield_rate = max(0.0, Temp)**2 * max(0.0, dens) * np.exp(-2.2 * abs(A))
        fusion_yield += yield_rate * DT

        peak_A = max(peak_A, abs(A))
        min_temp = min(min_temp, Temp)
        max_dens = max(max_dens, dens)

        if abs(A) > A_CRIT or Temp < 0.72 or dens > 1.45:
            unsafe_time += DT

        control_energy += u_applied * u_applied * DT

        if abs(A) > A_COLLAPSE or Temp < 0.35 or dens > 2.2 or not np.isfinite(A):
            collapsed = True
            collapse_time = t
            break

    return {
        "controller": controller,
        "seed": seed,
        "survived": int(not collapsed),
        "collapse_time": collapse_time,
        "peak_A": peak_A,
        "min_temp": min_temp,
        "max_density": max_dens,
        "unsafe_time": unsafe_time,
        "control_energy": control_energy,
        "fusion_yield": fusion_yield,
        "yield_per_energy": fusion_yield / (control_energy + 1e-9),
    }

def run_one(args):
    return simulate(*args)

def main():
    controllers = ["PID", "GSCX_V7", "GSCX_V91"]
    jobs = [(c, s) for c in controllers for s in range(SEEDS)]
    workers = min(cpu_count(), 8)

    print(f"Running {len(jobs)} fusion-core simulations on {workers} workers...")

    with Pool(workers) as pool:
        rows = pool.map(run_one, jobs)

    df = pd.DataFrame(rows)
    df.to_csv("fusion_core_gscx_v91_endurance_endurance_results.csv", index=False)

    summary = df.groupby("controller").agg(
        survival_rate=("survived", "mean"),
        mean_peak_A=("peak_A", "mean"),
        mean_min_temp=("min_temp", "mean"),
        mean_max_density=("max_density", "mean"),
        mean_unsafe_time=("unsafe_time", "mean"),
        mean_control_energy=("control_energy", "mean"),
        mean_fusion_yield=("fusion_yield", "mean"),
        mean_yield_per_energy=("yield_per_energy", "mean"),
    ).reset_index()

    summary.to_csv("fusion_core_gscx_v91_endurance_endurance_summary.csv", index=False)
    print(summary.to_string(index=False))

    for metric in [
        "survival_rate",
        "mean_peak_A",
        "mean_min_temp",
        "mean_max_density",
        "mean_unsafe_time",
        "mean_control_energy",
        "mean_fusion_yield",
        "mean_yield_per_energy",
    ]:
        plt.figure(figsize=(8, 5))
        plt.bar(summary["controller"], summary[metric])
        plt.title(metric.replace("_", " ").title())
        plt.tight_layout()
        plt.savefig(f"fusion_core_gscx_v91_endurance_{metric}.png", dpi=180)
        plt.close()

    print("\nSAVED:")
    print("  fusion_core_gscx_v91_endurance_endurance_results.csv")
    print("  fusion_core_gscx_v91_endurance_endurance_summary.csv")
    print("  fusion_core_gscx_v91_endurance_*.png")

if __name__ == "__main__":
    main()
