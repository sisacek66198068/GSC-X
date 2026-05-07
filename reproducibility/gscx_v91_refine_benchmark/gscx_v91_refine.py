import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from multiprocessing import Pool, cpu_count

DT = 0.001
T = 60.0
N_STEPS = int(T / DT)
A_CRIT = 0.60
A_HARD = 0.95

# Dirty hardware reality
SENSOR_DELAY = 0.015
ACTUATOR_LAG = 0.020
NOISE_SIGMA = 0.045

DELAY_STEPS = max(1, int(SENSOR_DELAY / DT))
LAG_ALPHA = DT / (ACTUATOR_LAG + DT)

SEEDS = 1000

def burst_profile(t):
    bursts = [
        (8.0, 9.0, 2.2),
        (18.0, 19.5, 2.6),
        (31.0, 32.2, 3.0),
        (44.0, 45.0, 2.8),
        (53.0, 54.0, 3.2),
    ]
    s = 0.0
    for a, b, amp in bursts:
        if a <= t <= b:
            s += amp
    return s

def simulate(controller, seed):
    rng = np.random.default_rng(seed)

    A = 0.02
    u_applied = 0.0
    integral = 0.0

    raw_hist = [A] * (DELAY_STEPS + 2)
    ema = A
    ema_prev = A
    persistence = 0.0
    memory = 0.0
    recovery = 0.0

    peak = abs(A)
    unsafe_time = 0.0
    energy = 0.0
    productivity = 0.0
    collapsed = False
    collapse_time = np.nan

    for i in range(N_STEPS):
        t = i * DT

        # true system forcing
        shock = burst_profile(t)
        gamma_mhd = 1.15 + shock
        eta = 1.0

        # delayed noisy sensor
        raw_hist.append(A)
        delayed_true = raw_hist[-DELAY_STEPS]
        A_raw = delayed_true + rng.normal(0.0, NOISE_SIGMA)

        d_raw = (A_raw - raw_hist[-DELAY_STEPS-1]) / DT if len(raw_hist) > DELAY_STEPS + 2 else 0.0

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

        elif controller == "GSCX_V9":
            # Chief Core: EMA + adaptive alpha + raw emergency channel + predictive observer
            d_ema_probe = (ema - ema_prev) / DT
            alpha_ema = 0.035 + 0.12 * min(1.0, abs(d_ema_probe) / 8.0)
            alpha_ema = np.clip(alpha_ema, 0.025, 0.18)

            ema_prev = ema
            ema = alpha_ema * A_raw + (1.0 - alpha_ema) * ema
            d_ema = (ema - ema_prev) / DT

            A_pred = ema + 0.012 * d_ema

            # persistence gate
            if abs(A_pred) > 0.42:
                persistence += DT
            else:
                persistence = max(0.0, persistence - 2.0 * DT)

            # instability memory
            memory = 0.995 * memory + 0.005 * max(0.0, abs(A_pred) - 0.35)

            raw_emergency = abs(A_raw) > A_HARD
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

            # recovery relaxation prevents snap-back overreaction
            recovery = max(recovery * 0.997, 0.0)
            if risk > 0.65:
                recovery = 1.0

            u_cmd = -mode_gain * Gamma * A_pred * (1.0 + alpha_nl * A_pred * A_pred) - Ki * integral
            u_cmd *= (1.0 - 0.10 * recovery)
            u_cmd = np.clip(u_cmd, -6.5, 6.5)

        else:
            raise ValueError(controller)

        # actuator lag
        u_applied += LAG_ALPHA * (u_cmd - u_applied)

        # plant dynamics
        dA = gamma_mhd * A - eta * A**3 + u_applied
        A = A + DT * dA

        peak = max(peak, abs(A))
        if abs(A) > A_CRIT:
            unsafe_time += DT
        energy += u_applied * u_applied * DT
        productivity += max(0.0, 1.0 - abs(A)) * DT

        if abs(A) > 1.50 or not np.isfinite(A):
            collapsed = True
            collapse_time = t
            break

    return {
        "controller": controller,
        "seed": seed,
        "survived": int(not collapsed),
        "collapse_time": collapse_time,
        "peak": peak,
        "unsafe_time": unsafe_time,
        "energy": energy,
        "productivity": productivity,
        "prod_per_energy": productivity / (energy + 1e-9),
    }

def run_one(args):
    return simulate(*args)

def main():
    controllers = ["PID", "GSCX_V7", "GSCX_V9"]
    jobs = [(c, s) for c in controllers for s in range(SEEDS)]

    workers = min(cpu_count(), 8)
    print(f"Running {len(jobs)} simulations on {workers} workers...")

    with Pool(workers) as pool:
        rows = pool.map(run_one, jobs)

    df = pd.DataFrame(rows)
    df.to_csv("gscx_v91_refine_results.csv", index=False)

    summary = df.groupby("controller").agg(
        survival_rate=("survived", "mean"),
        mean_peak=("peak", "mean"),
        median_peak=("peak", "median"),
        mean_unsafe_time=("unsafe_time", "mean"),
        mean_energy=("energy", "mean"),
        mean_productivity=("productivity", "mean"),
        mean_prod_per_energy=("prod_per_energy", "mean"),
    ).reset_index()

    summary.to_csv("gscx_v91_refine_summary.csv", index=False)
    print(summary.to_string(index=False))

    for metric in ["survival_rate", "mean_peak", "mean_unsafe_time", "mean_energy", "mean_prod_per_energy"]:
        plt.figure(figsize=(8, 5))
        plt.bar(summary["controller"], summary[metric])
        plt.title(metric.replace("_", " ").title())
        plt.tight_layout()
        plt.savefig(f"gscx_v91_{metric}.png", dpi=180)
        plt.close()

    print("\nSAVED:")
    print("  gscx_v91_refine_results.csv")
    print("  gscx_v91_refine_summary.csv")
    print("  gscx_v91_*.png")

if __name__ == "__main__":
    main()
