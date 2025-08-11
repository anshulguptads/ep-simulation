# app.py
# Executive Presence Simulation – High‑Stakes Client Negotiation (Student‑facing)
# -----------------------------------------------------------------------------
# Streamlit single‑file app with:
# - Student Dashboard (multi‑scenario launcher)
# - Pre‑filled charts for multiple attempts (A1, A2, A3)
# - End‑to‑end journey pages for the Negotiation scenario
# To run:  pip install -r requirements.txt  &&  streamlit run app.py

import io
import math
from typing import List

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

st.markdown(
    """
    <style>
      .chip {display:inline-block;padding:4px 10px;margin:4px;border-radius:999px;border:1px solid #21486b;background:#0b2238;color:#cbe6ff;font-size:12px}
      .callout {border:1px solid #1e3a5f;background:#0f1f37;color:#dbeafe;padding:12px 14px;border-radius:12px}
      .metric {background:#0f172a;border:1px solid #1f2937;border-radius:16px;padding:14px;color:#e5e7eb}
      .kpi-title {color:#cbd5e1;font-size:13px;margin-bottom:6px}
      .avatar-frame {border:1px solid #18314f;border-radius:16px;padding:10px;background:linear-gradient(180deg,#0b1b33,#0a1020)}
      .card {border:1px solid #1f2937;border-radius:16px;padding:16px;background:#0f172a}
      footer {color:#94a3b8}
      .status-dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Demo Data / Session State
# -------------------------
DEFAULT_RADAR_LABELS = ["Gravitas","Persuasion","Vocal","Gestures","Brevity"]
DEFAULT_BAR_CATS = ["Opening", "Objections", "Close"]
WEEKS = ["Week 1","W2","W3","W4","W5","W6"]

if "nav" not in st.session_state:
    st.session_state.nav = "Student Dashboard"

if "current_scenario" not in st.session_state:
    st.session_state.current_scenario = None  # e.g., "Negotiation"

# Pre‑filled scores (three attempts)
if "attempt1_radar" not in st.session_state:
    st.session_state.attempt1_radar = [5.0, 5.5, 6.0, 5.0, 4.8]
if "attempt2_radar" not in st.session_state:
    st.session_state.attempt2_radar = [7.6, 7.2, 7.9, 6.8, 7.3]
if "attempt3_radar" not in st.session_state:
    st.session_state.attempt3_radar = [8.4, 8.1, 8.6, 7.9, 8.2]

if "attempt1_bars" not in st.session_state:
    st.session_state.attempt1_bars = [6.0, 5.2, 4.6]
if "attempt2_bars" not in st.session_state:
    st.session_state.attempt2_bars = [7.6, 7.2, 6.9]
if "attempt3_bars" not in st.session_state:
    st.session_state.attempt3_bars = [8.5, 8.0, 7.7]

# Baseline vs actual trajectory (derived from attempts 1→3)
if "weekly_baseline" not in st.session_state:
    st.session_state.weekly_baseline = [2.0, 3.0, 3.8, 4.8, 5.8, 6.5]
if "weekly_actual" not in st.session_state:
    a1 = float(np.mean(st.session_state.attempt1_radar))
    a3 = float(np.mean(st.session_state.attempt3_radar))
    st.session_state.weekly_actual = list(np.linspace(a1, a3, len(WEEKS)))

# -------------------------
# Utilities
# -------------------------

def render_mock_avatar(size: int = 280) -> io.BytesIO:
    fig, ax = plt.subplots(figsize=(size/100, size/100), dpi=100)
    ax.set_aspect('equal')
    ax.axis('off')

    # Background
    circle_bg = plt.Circle((0.5, 0.55), 0.45)
    ax.add_artist(circle_bg)

    # Face
    face = plt.Circle((0.5, 0.62), 0.22)
    ax.add_artist(face)
    # Eyes
    ax.plot([0.44, 0.56], [0.66, 0.66], marker='o', markersize=4, linestyle='')
    # Smile
    theta = np.linspace(math.pi*0.1, math.pi*0.9, 100)
    ax.plot(0.5 + 0.12*np.cos(theta), 0.60 + 0.07*np.sin(theta))

    # Suit
    ax.add_patch(plt.Polygon([[0.18,0.10],[0.5,0.42],[0.82,0.10]], closed=True))
    ax.add_patch(plt.Polygon([[0.5,0.42],[0.65,0.10],[0.82,0.10]], closed=True))
    ax.add_patch(plt.Polygon([[0.5,0.42],[0.35,0.10],[0.18,0.10]], closed=True))
    # Tie
    ax.add_patch(plt.Polygon([[0.48,0.42],[0.52,0.42],[0.54,0.25],[0.46,0.25]], closed=True))

    buf = io.BytesIO()
    plt.tight_layout(pad=0)
    plt.savefig(buf, format='png', transparent=True)
    plt.close(fig)
    buf.seek(0)
    return buf

# Charts

def radar_chart(labels: List[str], series: List[List[float]], series_names: List[str]):
    N = len(labels)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5.2, 4.0), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_yticklabels([])
    ax.set_ylim(0, 10)

    for s in series:
        vals = np.array(s + s[:1])
        ax.plot(angles, vals, linewidth=2)
        ax.fill(angles, vals, alpha=0.12)

    ax.legend(series_names, loc='upper right', bbox_to_anchor=(1.25, 1.10))
    st.pyplot(fig, use_container_width=False)


def grouped_bar(categories: List[str], series: List[List[float]], series_names: List[str]):
    x = np.arange(len(categories))
    m = len(series)
    width = 0.9 / m
    fig, ax = plt.subplots(figsize=(6.2,3.8))
    for i, s in enumerate(series):
        ax.bar(x - 0.45 + i*width + width/2, s, width)
    ax.set_xticks(x, categories)
    ax.set_ylabel('Score')
    ax.set_ylim(0, 10)
    ax.legend(series_names)
    st.pyplot(fig, use_container_width=False)


def line_growth(weeks: List[str], baseline: List[float], actual: List[float]):
    x = np.arange(len(weeks))
    fig, ax = plt.subplots(figsize=(7.2,3.8))
    ax.plot(x, baseline, marker='o')
    ax.fill_between(x, baseline, step='pre', alpha=0.10)
    ax.plot(x, actual, marker='o')
    ax.fill_between(x, actual, step='pre', alpha=0.18)
    ax.set_xticks(x, weeks)
    ax.set_ylabel('Composite EP Score')
    ax.set_ylim(0, 10)
    ax.legend(["Baseline Path","Actual With Learning"])
    st.pyplot(fig, use_container_width=False)

# -------------------------
# Sidebar Navigation
# -------------------------
sections = [
    "Student Dashboard",
    "Home",
    "Scenario Brief",
    "Baseline Simulation",
    "Live Coaching",
    "Feedback",
    "Learning Modules",
    "Re‑Simulation",
    "Growth Dashboard",
]
choice = st.sidebar.radio("Navigate", sections, index=sections.index(st.session_state.nav), key="nav")

# -------------------------
# Student Dashboard (multi‑scenario launcher)
# -------------------------
if choice == "Student Dashboard":
    st.title("Your Executive Presence Simulations")
    st.write("Select a simulation to begin. Your latest scores are pre‑filled in charts for quick review.")

    # Demo allocations
    sims = [
        {"key":"Negotiation","title":"High‑Stakes Client Negotiation","status":"In Progress","score":round(np.mean(st.session_state.attempt3_radar),1)},
        {"key":"BoardUpdate","title":"Boardroom Strategic Update","status":"Assigned","score":None},
        {"key":"CrisisComms","title":"Crisis Communication Briefing","status":"Assigned","score":None},
        {"key":"InvestorPitch","title":"Investor Pitch for Funding","status":"Assigned","score":None},
    ]

    cols = st.columns(2)
    for i, sim in enumerate(sims):
        with cols[i%2]:
            with st.container(border=True):
                st.subheader(sim["title"])
                status_color = "#34d399" if sim["status"]=="In Progress" else "#60a5fa"
                st.markdown(f"<span class='status-dot' style='background:{status_color}'></span>**{sim['status']}**", unsafe_allow_html=True)
                if sim["score"] is not None:
                    st.metric("Latest Composite Score", sim["score"])
                else:
                    st.caption("Score available after first attempt.")
                btn_label = "Resume" if sim["key"]=="Negotiation" else "Start"
                if st.button(f"{btn_label}", key=f"btn_{sim['key']}"):
                    st.session_state.current_scenario = sim["key"]
                    # Navigate into the journey; Negotiation is fully wired
                    st.session_state.nav = "Home" if sim["key"]=="Negotiation" else "Scenario Brief"
                    st.experimental_rerun()

    st.divider()
    st.caption("Tip: Begin with the Negotiation simulation. Additional simulations will unlock progressively.")

# -------------------------
# Journey: Negotiation (fully wired)
# -------------------------
elif choice == "Home":
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

elif choice == "Live Coaching":
    st.header("Live Coaching Prompts")
    st.write("Non‑intrusive nudges appear when your pacing, framing, or presence drifts. You stay in flow while receiving timely, actionable cues.")
    st.warning("Breathe. Shorten your sentence. Lead with impact → ROI in 90 days.")
    st.markdown("**Example Prompts**")
    st.markdown("- Slow down 10% — let the point land.\n- Anchor on outcomes before price.\n- Use a brief silence — regain control.\n- Translate features → CFO metrics.")

elif choice == "Feedback":
    st.header("Feedback & Scorecard — Pre‑filled Attempts")

    st.subheader("Executive‑Presence Footprint (Radar)")
    radar_chart(
        DEFAULT_RADAR_LABELS,
        [
            st.session_state.attempt1_radar,
            st.session_state.attempt2_radar,
            st.session_state.attempt3_radar,
        ],
        ["Attempt 1","Attempt 2","Attempt 3"],
    )

    st.divider()
    st.subheader("Attempt Comparison (Opening • Objections • Close)")
    grouped_bar(
        DEFAULT_BAR_CATS,
        [
            st.session_state.attempt1_bars,
            st.session_state.attempt2_bars,
            st.session_state.attempt3_bars,
        ],
        ["Attempt 1","Attempt 2","Attempt 3"],
    )

    st.info("Charts are pre‑filled with representative scores across three attempts. Use them as exemplars in your leadership demo.")

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

elif choice == "Re‑Simulation":
    st.header("Re‑Simulation")
    st.write("Face the same client persona with varied objection order. Demonstrate improved framing, calm under pressure, and a disciplined close.")
    st.image(render_mock_avatar(260).getvalue(), caption="Client Avatar")
    st.info("Acknowledge risk. Give a concrete plan. Then secure a micro‑agreement.")
    st.markdown("**What Good Looks Like**: Clear outcome anchor → risk plan → confident price defense → crisp close with agreed next step.")

elif choice == "Growth Dashboard":
    st.header("Your Journey Over Time")

    # Update trajectory to reflect Attempts 1 → 3
    a1 = float(np.mean(st.session_state.attempt1_radar))
    a3 = float(np.mean(st.session_state.attempt3_radar))
    st.session_state.weekly_actual = list(np.linspace(a1, a3, len(WEEKS)))

    line_growth(WEEKS, st.session_state.weekly_baseline, st.session_state.weekly_actual)

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
