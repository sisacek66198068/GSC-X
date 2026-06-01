import numpy as np
import pandas as pd
import os

SEED=int(os.environ.get("GSC_SEED","0"))
rng=np.random.default_rng(SEED)

dt=0.05
T=180
steps=int(T/dt)

TARGET=0.0
UNSAFE=1.2

def clamp(x,lo=-1,hi=1):
    return max(lo,min(hi,x))

def run(ctrl):
    x=rng.uniform(0.55,0.85)
    v=rng.uniform(-0.08,0.08)
    prev=0.0
    integ=0.0
    memory=0.0
    motor_heat=0.0
    delay=[0.0]*rng.integers(5,12)
    rows=[]

    P1=rng.uniform(0,6.28)
    P2=rng.uniform(0,6.28)

    for k in range(steps):
        t=k*dt

        disturbance=(
            rng.uniform(0.07,0.13)*np.sin(t/5+P1)
            +rng.uniform(0.03,0.08)*np.sin(t/1.7+P2)
        )

        if 50<t<80:
            disturbance+=rng.uniform(0.25,0.55)*np.sin(t*1.2+P1)

        if 115<t<145:
            disturbance-=rng.uniform(0.20,0.45)*np.sin(t*1.5+P2)

        meas=x+rng.normal(0,rng.uniform(0.008,0.018))

        err=TARGET-meas
        derr=(err-prev)/dt
        prev=err
        integ+=err*dt

        if ctrl=="PID":
            u_raw=1.8*err+0.32*derr+0.02*integ
        else:
            risk=1.2*abs(x)+0.8*abs(v)+0.9*motor_heat
            memory=0.97*memory+0.03*risk
            guardian=(risk+memory)>0.85

            if guardian:
                u_raw=(
                    1.45*err
                    +0.34*derr
                    -0.35*np.tanh(v)
                    -0.30*np.tanh(motor_heat)
                    +0.10*np.tanh(memory)
                )
            else:
                u_raw=(
                    1.25*err
                    +0.24*derr
                    -0.12*np.tanh(v)
                )

        delay.append(clamp(u_raw))
        u=delay.pop(0)

        motor_heat=0.995*motor_heat+0.035*abs(u)

        authority=max(
            0.35,
            1-rng.uniform(0.20,0.45)*motor_heat
        )

        a=authority*u+disturbance-0.08*v
        v+=a*dt
        x+=v*dt

        unsafe=abs(x)>UNSAFE

        rows.append({
            "x":x,
            "v":v,
            "u":u,
            "motor_heat":motor_heat,
            "unsafe":unsafe
        })

    return pd.DataFrame(rows)

pid=run("PID")
gsc=run("GSCX")

summary=[]
for name,df in [("PID",pid),("GSCX",gsc)]:
    unsafe=df.unsafe.mean()
    energy=np.mean(np.abs(df.u))
    pos_error=np.mean(np.abs(df.x-TARGET))
    heat=np.mean(df.motor_heat)
    overshoot=np.max(np.abs(df.x))

    prod=1/(1+unsafe+1.1*pos_error+0.45*energy+0.35*heat+0.12*overshoot)

    summary.append({
        "controller":name,
        "unsafe_time":unsafe,
        "control_energy":energy,
        "position_error":pos_error,
        "motor_heat":heat,
        "max_abs_position":overshoot,
        "productivity":prod
    })

summary=pd.DataFrame(summary)

print(f"\n=== ROBOTICS V3 RANDOM seed={SEED} ===")
print(summary.to_string(index=False))

summary.to_csv("robotics_v3_random_summary.csv",index=False)
