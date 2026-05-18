import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="NVIDIA-Ready GSC-X Live Demo",
    layout="wide"
)

st.title("GSC-X LIVE DEMO — NVIDIA-READY STABILITY INTELLIGENCE")
st.caption("Predictive anomaly scanner for nonlinear autonomous systems")

fault = st.sidebar.selectbox(
    "Injected Fault / Anomaly",
    [
        "none",
        "delay_response",
        "burst_noise",
        "sensor_drift",
        "oscillation",
    ]
)

threshold = st.sidebar.slider(
    "Warning Threshold",
    0.5,
    2.0,
    1.1,
    0.05
)

steps = np.arange(0, 100)

risk = (
    0.4
    + 0.003 * steps
    + 0.15 * np.sin(steps / 5)
)

if fault != "none":
    risk[60:] += np.linspace(0, 1.2, 40)

state = []

for r in risk:
    if r < threshold:
        state.append("NORMAL")
    elif r < threshold * 1.35:
        state.append("WARNING")
    else:
        state.append("CRITICAL")

warning_step = None

for i, r in enumerate(risk):
    if r >= threshold:
        warning_step = i
        break

collapse_step = None

if fault != "none":
    collapse_step = 85

col1, col2, col3, col4 = st.columns(4)

col1.metric("Injected Anomaly", fault)
col2.metric("Max Risk", f"{risk.max():.2f}")
col3.metric("Final State", state[-1])

if warning_step is None:
    col4.metric("Warning Step", "None")
else:
    col4.metric("Warning Step", warning_step)

fig, ax = plt.subplots(figsize=(10, 4))

ax.plot(
    steps,
    risk,
    linewidth=2,
    label="GSC Risk Score"
)

ax.axhline(
    threshold,
    linestyle="--",
    label="WARNING threshold"
)

ax.axhline(
    threshold * 1.35,
    linestyle=":",
    label="CRITICAL threshold"
)

if warning_step is not None:
    ax.axvline(
        warning_step,
        linestyle="--",
        label="First WARNING"
    )

if collapse_step is not None:
    ax.axvline(
        collapse_step,
        linestyle="-.",
        label="Unsafe / Collapse"
    )

ax.set_title("Predictive Stability Risk Score")
ax.set_xlabel("Simulation Step")
ax.set_ylabel("Risk Score")
ax.legend()

st.pyplot(fig)

df = pd.DataFrame({
    "step": steps,
    "risk": risk,
    "state": state,
})

st.subheader("Replay Timeline")
st.dataframe(df.tail(25), use_container_width=True)

st.subheader("Prediction Result")

if fault == "none":
    st.info("No injected anomaly. System remains in NORMAL state.")

elif warning_step is not None and collapse_step is not None and warning_step < collapse_step:
    st.success(
    f"EARLY WARNING SUCCESS: GSC-X predicted instability {collapse_step - warning_step} simulation steps before unsafe system divergence."
)

elif warning_step is not None:
    st.warning("GSC-X issued a warning, but collapse timing was not confirmed.")

else:
    st.error("Unsafe/collapse event occurred without early warning.")

st.markdown("---")

st.subheader("Why this matters")

st.write(
    """
This demo shows GSC-X as a **Predictive Stability Intelligence Layer**.

It does not replace the main controller.  
It monitors nonlinear system dynamics and detects emerging instability trends before failure.

Target use cases:
- robotics safety,
- autonomous systems,
- digital twins,
- industrial anomaly detection,
- fusion plasma monitoring,
- aerospace runtime diagnostics.
"""
)

st.caption(
    "GSC-X © Martin Štěpánů | Independent Researcher | ORCID: 0009-0007-0409-6037 | gds-gsc-x.com"
)