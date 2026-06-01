import subprocess, os, pandas as pd

rows=[]

for seed in range(3000):
    print(f"\n=== SEED {seed} ===")

    env=os.environ.copy()
    env["GSC_SEED"]=str(seed)

    subprocess.run(
        ["python3","benchmark_robotics_v3_random.py"],
        env=env,
        check=True
    )

    df=pd.read_csv("robotics_v3_random_summary.csv")

    for _,r in df.iterrows():
        rr=dict(r)
        rr["seed"]=seed
        rows.append(rr)

all_df=pd.DataFrame(rows)

print("\n=== ROBOTICS TRUE N3000 MEAN ===")
print(
    all_df.groupby("controller")[[
        "unsafe_time",
        "control_energy",
        "position_error",
        "motor_heat",
        "max_abs_position",
        "productivity"
    ]].mean().to_string()
)

wide=all_df.pivot(
    index="seed",
    columns="controller",
    values="productivity"
)

print("\nGSCX wins:",
      int((wide["GSCX"]>wide["PID"]).sum()),
      "/3000")

all_df.to_csv("robotics_TRUE_N3000.csv",index=False)
