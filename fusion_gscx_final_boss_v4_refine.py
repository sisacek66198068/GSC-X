import numpy as np
import pandas as pd

print("=== GSC-X FINAL BOSS v4 : REFINED ENDURANCE SAFE MODE ===")

dt = 0.002
T = 90.0
t = np.arange(0.0, T, dt)
N = 2000

Acrit = 0.75
Tcrit_low = 0.45
ncrit_high = 1.35

Kp = 3.4
Kd = 0.55

Gamma = 1.0
alpha = 1.5

def gsc_field(x, gain):
    return -gain * Gamma * x * (1.0 + alpha * x*x)

def scanner(A, dA, Tcore, density):
    score = 0.0
    if A > 0.16:
        score += A / Acrit
    if dA > 0.14:
        score += 1.7 * dA
    if density > 1.12:
        score += 0.55 * (density - 1.12)
    if Tcore < 0.62:
        score += 0.35 * (0.62 - Tcore)
    return score

def commander(score, memory):
    e = score + 0.30 * memory
    if e < 0.70:
        return "NORMAL"
    elif e < 1.20:
        return "WARNING"
    elif e < 1.80:
        return "CRITICAL"
    else:
        return "EMERGENCY"

def run_case(seed, mode):
    rng = np.random.default_rng(seed)

    A = 0.03
    Tcore = 1.0
    density = 1.0
    prevA = A

    peak = A
    minT = Tcore
    maxD = density
    unsafe = 0.0
    energy = 0.0
    fyield = 0.0
    failed = False

    memory = 0.0
    emergency_timer = 0.0
    recovery_mode = False

    counts = {
        "NORMAL": 0,
        "WARNING": 0,
        "CRITICAL": 0,
        "EMERGENCY": 0,
        "RECOVERY": 0
    }

    bursts = []
    for _ in range(rng.integers(8, 16)):
        s = rng.uniform(3, T - 5)
        d = rng.uniform(1.5, 4.0)
        a = rng.uniform(0.35, 1.00)
        bursts.append((s, s + d, a))

    for ti in t:
        burst = sum(a for s, e, a in bursts if s < ti < e)

        noise = rng.normal(0.0, 0.03)
        A_meas = max(0.0, A + noise)

        dA = (A_meas - prevA) / dt
        prevA = A_meas

        if mode == "pid":
            u = -Kp * A_meas - Kd * dA

        else:
            score = scanner(A_meas, dA, Tcore, density)
            cmode = commander(score, memory)

            if Tcore < 0.64:
                recovery_mode = True

            if cmode == "EMERGENCY":
                emergency_timer += dt
            else:
                emergency_timer = max(0.0, emergency_timer - 2.0 * dt)

            if emergency_timer > 2.4:
                recovery_mode = True

            if recovery_mode:
                counts["RECOVERY"] += 1
                u = -0.30 * Kp * A_meas - 0.08 * Kd * dA

                if Tcore > 0.80 and A < 0.25:
                    recovery_mode = False
                    emergency_timer = 0.0
            else:
                counts[cmode] += 1

                if cmode == "NORMAL":
                    u = -0.70 * Kp * A_meas

                elif cmode == "WARNING":
                    u = -0.55 * Kp * A_meas + 0.35 * gsc_field(A_meas, 1.0)

                elif cmode == "CRITICAL":
                    u = -0.35 * Kp * A_meas + 0.60 * gsc_field(A_meas, 2.2)

                else:
                    u = -0.20 * Kp * A_meas + 0.62 * gsc_field(A_meas, 2.8)

        u = float(np.clip(u, -3.0, 3.0))

        pressure = Tcore * density

        dA_phys = (
            0.90 * A
            - 0.82 * A**3
            + 0.28 * (pressure - 1.0)
            + 0.10 * (density - 1.0)
            + burst
            + u
            + rng.normal(0.0, 0.015)
        )

        recovery_heat = 0.015 if recovery_mode else 0.0

        dT = (
            0.035
            + recovery_heat
            - 0.022 * Tcore * (1.0 + 1.8 * A)
            - 0.014 * abs(u)
            - 0.025 * A
        )

        dn = (
            0.010
            - 0.011 * density * (1.0 + 0.5 * abs(u))
            + 0.015 * burst
        )

        A = max(0.0, A + dt * dA_phys)
        Tcore = max(0.0, Tcore + dt * dT)
        density = max(0.0, density + dt * dn)

        if A > 0.30:
            memory = min(2.0, memory + 0.015)
        else:
            memory = max(0.0, memory - 0.010)

        peak = max(peak, A)
        minT = min(minT, Tcore)
        maxD = max(maxD, density)

        fyield += max(0.0, density*density*Tcore*Tcore*(1.0 - A)) * dt
        energy += u*u*dt

        if (A >= Acrit) or (Tcore <= Tcrit_low) or (density >= ncrit_high):
            unsafe += dt
            failed = True

    return {
        "mode": mode,
        "survived": not failed,
        "peak": peak,
        "minT": minT,
        "maxD": maxD,
        "unsafe": unsafe,
        "energy": energy,
        "yield": fyield,
        "ype": fyield / (1.0 + energy),
        "RECOVERY_frac": counts["RECOVERY"]/len(t) if mode=="gscx" else np.nan
    }

rows = []

for seed in range(N):
    if seed % 100 == 0:
        print(f"running seed {seed}/{N}")

    rows.append(run_case(seed, "pid"))
    rows.append(run_case(seed, "gscx"))

df = pd.DataFrame(rows)

summary = df.groupby("mode").agg(
    survival_rate=("survived", "mean"),
    mean_peak=("peak", "mean"),
    mean_min_Tcore=("minT", "mean"),
    mean_max_density=("maxD", "mean"),
    mean_time_unsafe=("unsafe", "mean"),
    mean_energy=("energy", "mean"),
    mean_fusion_yield=("yield", "mean"),
    mean_yield_per_energy=("ype", "mean"),
).reset_index()

print()
print(summary.to_string(index=False))

g = df[df["mode"]=="gscx"]

print()
print("RECOVERY MODE FRACTION")
print(f"RECOVERY = {g['RECOVERY_frac'].mean():.3f}")

df.to_csv("fusion_gscx_final_boss_v4_refine_results.csv", index=False)
summary.to_csv("fusion_gscx_final_boss_v4_refine_summary.csv", index=False)

print()
print("SAVED:")
print(" fusion_gscx_final_boss_v4_refine_results.csv")
print(" fusion_gscx_final_boss_v4_refine_summary.csv")
