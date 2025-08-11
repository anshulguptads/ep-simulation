# app.py
# Executive Presence Simulation – High‑Stakes Client Negotiation (Student‑facing)
# --------------------------------------------------------------
# Streamlit single‑file app with sidebar navigation. No external assets required.
# To run locally:  pip install -r requirements.txt  &&  streamlit run app.py

import io
import math
import base64
from typing import List, Tuple

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# -------------------------
# Page Setup
# -------------------------
st.set_page_config(
    page_title="Executive Presence Simulator — High‑Stakes Client Negotiation",
    page_icon="💼",
    layout="wide",
)

# Minimal theming via markdown (kept subtle for Streamlit Cloud)
st.markdown(
    """
    <style>
      .chip {display:inline-block;padding:4px 10px;margin:4px;border-radius:999px;border:1px solid #21486b;background:#0b2238;color:#cbe6ff;font-size:12px}
      .callout {border:1px solid #1e3a5f;background:#0f1f37;color:#dbeafe;padding:12px 14px;border-radius:12px}
      .metric {background:#0f172a;border:1px solid #1f2937;border-radius:16px;padding:14px;color:#e5e7eb}
      .kpi-title {color:#cbd5e1;font-size:13px;margin-bottom:6px}
      .avatar-frame {border:1px solid #18314f;border-radius:16px;padding:10px;background:linear-gradient(180deg,#0b1b33,#0a1020)}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Utility: Mock Avatar (Matplotlib drawing)
# -------------------------

def render_mock_avatar(size: int = 280) -> io.BytesIO:
    fig, ax = plt.subplots(figsize=(size/100, size/100), dpi=100)
    ax.set_aspect('equal')
    ax.axis('off')

    # Background glow
    circle_bg = plt.Circle((0.5, 0.55), 0.45, color=(0.10, 0.16, 0.28), zorder=0)
    ax.add_artist(circle_bg)

    # Face
    face = plt.Circle((0.5, 0.62), 0.22, color=(1.0, 0.85, 0.70), zorder=1)
    ax.add_artist(face)
    # Eyes
    ax.plot([0.44, 0.56], [0.66, 0.66], marker='o', color='black', markersize=4, linestyle='')
    # Smile
    theta = np.linspace(math.pi*0.1, math.pi*0.9, 100)
    ax.plot(0.5 + 0.12*np.cos(theta), 0.60 + 0.07*np.sin(theta), color='#222')

    # Suit (simple V‑shape)
    ax.add_patch(plt.Polygon([[0.18,0.10],[0.5,0.42],[0.82,0.10]], closed=True, color='#0f172a'))
    ax.add_patch(plt.Polygon([[0.5,0.42],[0.65,0.10],[0.82,0.10]], closed=True, color='#111a2b'))
    ax.add_patch(plt.Polygon([[0.5,0.42],[0.35,0.10],[0.18,0.10]], closed=True, color='#111a2b'))
    # Tie
    ax.add_patch(plt.Polygon([[0.48,0.42],[0.52,0.42],[0.54,0.25],[0.46,0.25]], closed=True, color='#1f6feb'))

    buf = io.BytesIO()
    plt.tight_layout(pad=0)
    plt.savefig(buf, format='png', transparent=True)
    plt.close(fig)
    buf.seek(0)
    return buf

# -------------------------
# Charts
# -------------------------

def radar_chart(labels: List[str], baseline: List[float], improved: List[float]):
    N = len(labels)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    baseline = np.array(baseline + baseline[:1])
    improved = np.array(improved + improved[:1])
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(4.6, 3.6), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_yticklabels([])
    ax.set_ylim(0, 10)

    ax.plot(angles, baseline, linewidth=2)
    ax.fill(angles, baseline, alpha=0.1)
    ax.plot(angles, improved, linewidth=2)
    ax.fill(angles, improved, alpha=0.15)

    st.pyplot(fig, use_container_width=False)


def grouped_bar(categories: List[str], first: List[float], second: List[float]):
    x = np.arange(len(categories))
    width = 0.34
    fig, ax = plt.subplots(figsize=(5.8,3.6))
    ax.bar(x - width/2, first, width)
    ax.bar(x + width/2, second, width)
    ax.set_xticks(x, categories)
    ax.set_ylabel('Score')
    st.pyplot(fig, use_container_width=False)


def line_growth(weeks: List[str], baseline: List[float], actual: List[float]):
    x = np.arange(len(weeks))
    fig, ax = plt.subplots(figsize=(7,3.6))
    ax.plot(x, baseline, marker='o')
    ax.plot(x, actual, marker='o')
    ax.set_xticks(x, weeks)
    ax.set_ylabel('Composite EP Score')
    st.pyplot(fig, use_container_width=False)

# -------------------------
# Sidebar Navigation
# -------------------------
sections = [
    "Home",
    "Scenario Brief",
    "Baseline Simulation",
    "Live Coaching",
    "Feedback",
    "Learning Modules",
    "Re‑Simulation",
    "Growth Dashboard",
]
choice = st.sidebar.radio("Navigate", sections, index=0)

# -------------------------
# Home
# -------------------------
if choice == "Home":
    st.title("High‑Stakes Client Negotiation")
    st.write(
        """
        Experience a realistic boardroom renewal conversation with a C‑suite client. Practice persuasive framing under pressure and
        build the executive presence required to land the deal with confidence.
        """
    )
    c1, c2, c3 = st.columns([1.2, 0.05, 1])
    with c1:
        st.markdown('<span class="chip">Board‑level Dialogue</span>'
                    '<span class="chip">Objection Handling</span>'
                    '<span class="chip">Gravitas & Composure</span>'
                    '<span class="chip">ROI Storytelling</span>'
                    '<span class="chip">Executive Q&A</span>', unsafe_allow_html=True)
        st.markdown("\n")
        k1, k2, k3 = st.columns(3)
        with k1:
            st.markdown('<div class="metric"><div class="kpi-title">Session Length</div><h3>12–15 min</h3></div>', unsafe_allow_html=True)
        with k2:
            st.markdown('<div class="metric"><div class="kpi-title">Scenario Difficulty</div><h3>Progressive</h3></div>', unsafe_allow_html=True)
        with k3:
            st.markdown('<div class="metric"><div class="kpi-title">Focus Areas</div><h3>Gravitas • Persuasion • Control</h3></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="avatar-frame">', unsafe_allow_html=True)
        st.image(render_mock_avatar().getvalue(), caption="Client (CFO)")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="callout">“We have two competing offers with better pricing. Convince me why we should renew with you at current terms.”</div>', unsafe_allow_html=True)
        st.info("Tip: Lead with outcomes. Quantify impact before discussing price.")

# -------------------------
# Scenario Brief
# -------------------------
elif choice == "Scenario Brief":
    st.header("Scenario Brief")
    st.write(
        """
        You are renewing a global account with a C‑suite client. Two rivals are undercutting your price.
        Your objective is to secure renewal at target terms and position a value‑based upsell. You will navigate pricing
        pressure, risk concerns, and ROI scrutiny.
        """
    )
    st.subheader("Objectives & Parameters")
    st.markdown("- **Objective:** Renewal at target terms + upsell entry\n- **Stakeholder:** CFO (risk‑averse, data‑driven, concise)\n- **Timebox:** 8 minutes main exchange, 4 minutes Q&A")

    st.subheader("What You'll Be Assessed On")
    st.markdown("Clarity of opening, confidence under pressure, objection handling, ROI framing, and executive‑level brevity.")

# -------------------------
# Baseline Simulation
# -------------------------
elif choice == "Baseline Simulation":
    st.header("Baseline Simulation")
    st.write(
        "Hold a live conversation with the client avatar. Expect price pushback, timeline compression, and competitive references.\n"
        "Maintain composure, lead with outcomes, and secure agreement on value before discount.")
    c1, c2 = st.columns([1,1])
    with c1:
        st.image(render_mock_avatar(300).getvalue(), caption="Client Avatar")
    with c2:
        st.markdown('<div class="callout">Client: “If we match your terms, what guarantees do we have on time‑to‑value within this quarter?”</div>', unsafe_allow_html=True)
        st.success("Hold a calm pause. Reframe to business outcomes, then address risk.")

    st.markdown("**Journey Stages**")
    st.markdown("1. Baseline → 2. Feedback → 3. Learn → 4. Re‑Sim → 5. Growth")

# -------------------------
# Live Coaching
# -------------------------
elif choice == "Live Coaching":
    st.header("Live Coaching Prompts")
    st.write("Non‑intrusive nudges appear when your pacing, framing, or presence drifts. You stay in flow while receiving timely, actionable cues.")
    st.warning("Breathe. Shorten your sentence. Lead with impact → ROI in 90 days.")
    st.markdown("**Example Prompts**")
    st.markdown("- Slow down 10% — let the point land.\n- Anchor on outcomes before price.\n- Use a brief silence — regain control.\n- Translate features → CFO metrics.")

# -------------------------
# Feedback (Charts)
# -------------------------
elif choice == "Feedback":
    st.header("Feedback & Scorecard")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Executive‑Presence Footprint")
        radar_chart(
            labels=["Gravitas","Persuasion","Vocal","Gestures","Brevity"],
            baseline=[5.0, 5.5, 6.0, 5.0, 4.8],
            improved=[8.0, 7.5, 8.2, 7.1, 7.8],
        )
        st.caption("Your footprint expands after targeted practice.")
    with c2:
        st.subheader("Attempt Comparison")
        grouped_bar(
            categories=["Opening", "Objections", "Close"],
            first=[6.0, 5.2, 4.6],
            second=[8.3, 7.9, 7.2],
        )
        st.caption("Notable gains in opening, objection handling, and closing discipline.")

# -------------------------
# Learning Modules
# -------------------------
elif choice == "Learning Modules":
    st.header("Targeted Learning Modules")
    st.write("After feedback, complete short modules that strengthen specific behaviors observed in your session.")

    with st.expander("ROI Story in 60s"):
        st.write("Craft a concise value narrative that anchors the discussion on outcomes.")
        st.button("Practice", type="primary", disabled=True)
        st.button("View Example", disabled=True)

    with st.expander("Handling Price Pushback"):
        st.write("Reframe discounts to risk‑adjusted ROI with confident, executive wording.")
        st.button("Practice", type="primary", disabled=True)
        st.button("Drill", disabled=True)

    with st.expander("Composed Delivery"):
        st.write("Use pacing, intentional pauses, and controlled gestures to project calm authority.")
        st.button("Practice", type="primary", disabled=True)
        st.button("Breathe", disabled=True)

# -------------------------
# Re‑Simulation
# -------------------------
elif choice == "Re‑Simulation":
    st.header("Re‑Simulation")
    st.write("Face the same client persona with varied objection order. Demonstrate improved framing, calm under pressure, and a disciplined close.")
    st.image(render_mock_avatar(260).getvalue(), caption="Client Avatar")
    st.info("Acknowledge risk. Give a concrete plan. Then secure a micro‑agreement.")
    st.markdown("**What Good Looks Like**: Clear outcome anchor → risk plan → confident price defense → crisp close with agreed next step.")

# -------------------------
# Growth Dashboard
# -------------------------
elif choice == "Growth Dashboard":
    st.header("Your Journey Over Time")
    weeks = ["Week 1","W2","W3","W4","W5","W6"]
    baseline = [2.0, 3.0, 3.8, 4.8, 5.8, 6.5]
    actual = [2.0, 3.5, 4.6, 6.0, 7.2, 8.0]
    line_growth(weeks, baseline, actual)

    st.subheader("Export Portfolio")
    st.write("Download a concise report with highlights, before/after clips, and mastered behaviors.")
    st.button("Download Report", disabled=True)

# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.caption("This simulation is designed to help you build presence, persuasion, and composure in high‑stakes conversations. Complete the learning modules between attempts for best results.")

# -------------------------
# requirements.txt (include this in your repo)
# -------------------------
# streamlit
# matplotlib
# numpy
