# app.py
# Executive Presence Simulator — Student Dashboard + Three Scenarios
# -----------------------------------------------------------------
# Hardened navigation (no errors on click), three simulations only,
# full end-to-end journeys for each scenario with pre-filled charts.

import io
import math
from typing import List, Dict

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# -------------------------
# Page Setup
# -------------------------
st.set_page_config(
    page_title="Executive Presence Simulator",
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
      .status-dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Demo Data / Session State
# -------------------------
SCENARIOS: Dict[str, Dict] = {
    "Negotiation": {
        "title": "High‑Stakes Client Negotiation",
        "chips": ["Board‑level Dialogue","Objection Handling","Gravitas & Composure","ROI Storytelling","Executive Q&A"],
        "overview": "Experience a realistic boardroom renewal conversation with a C‑suite client. Practice persuasive framing under pressure and build the executive presence required to land the deal with confidence.",
        "brief": {
            "objective": "Renewal at target terms + upsell entry",
            "stakeholder": "CFO (risk‑averse, data‑driven, concise)",
            "timebox": "8 minutes main exchange, 4 minutes Q&A",
            "assessment": "Opening clarity, confidence under pressure, objection handling, ROI framing, executive brevity",
            "prompt1": "We have two competing offers with better pricing. Convince me why we should renew at current terms.",
        },
        "attempt_radar": [
            [5.0, 5.5, 6.0, 5.0, 4.8],
            [7.6, 7.2, 7.9, 6.8, 7.3],
            [8.4, 8.1, 8.6, 7.9, 8.2],
        ],
        "attempt_bars": [
            [6.0, 5.2, 4.6],
            [7.6, 7.2, 6.9],
            [8.5, 8.0, 7.7],
        ],
    },
    "BoardUpdate": {
        "title": "Boardroom Strategic Update",
        "chips": ["Executive Framing","Data‑to‑Insight","Stakeholder Control","Crisp Storyline","Q&A Handling"],
        "overview": "Deliver a concise quarterly update to the Board, defend strategic pivots, and secure alignment on next‑quarter bets.",
        "brief": {
            "objective": "Land 3 strategic priorities with Board consensus",
            "stakeholder": "Board (diverse viewpoints; time‑boxed)",
            "timebox": "6 minutes update, 6 minutes Q&A",
            "assessment": "Narrative arc, signal‑to‑noise, evidence quality, handling interruptions",
            "prompt1": "You have 3 minutes left. Prioritize what matters most for next quarter.",
        },
        "attempt_radar": [
            [5.2, 5.8, 5.9, 5.1, 5.0],
            [7.0, 7.4, 7.6, 6.7, 6.9],
            [8.1, 8.0, 8.3, 7.6, 7.8],
        ],
        "attempt_bars": [
            [6.2, 5.4, 5.0],
            [7.4, 7.1, 6.8],
            [8.3, 8.0, 7.6],
        ],
    },
    "CrisisComms": {
        "title": "Crisis Communication Briefing",
        "chips": ["Calm Authority","Message Control","Empathy","Fact‑based Clarity","Media Handling"],
        "overview": "Run a controlled briefing after a reputational incident. Maintain composure, deliver clear facts, and protect trust.",
        "brief": {
            "objective": "Stabilize sentiment; outline corrective actions",
            "stakeholder": "Employees + media (high scrutiny)",
            "timebox": "5 minutes statement, 7 minutes Q&A",
            "assessment": "Gravitas, transparency, bridge statements, empathy without liability",
            "prompt1": "Can you guarantee this won’t happen again?",
        },
        "attempt_radar": [
            [5.4, 5.2, 6.2, 5.3, 5.1],
            [7.1, 6.9, 7.8, 6.7, 6.8],
            [8.2, 7.9, 8.5, 7.8, 7.7],
        ],
        "attempt_bars": [
            [5.8, 5.6, 5.1],
            [7.3, 7.2, 6.9],
            [8.2, 8.1, 7.5],
        ],
    },
}

DEFAULT_RADAR_LABELS = ["Gravitas","Persuasion","Vocal","Gestures","Brevity"]
DEFAULT_BAR_CATS = ["Opening", "Objections", "Close"]
WEEKS = ["Week 1","W2","W3","W4","W5","W6"]

if "view" not in st.session_state:
    st.session_state.view = "dashboard"  # or "scenario"
if "scenario_key" not in st.session_state:
    st.session_state.scenario_key = None
if "scenario_page" not in st.session_state:
    st.session_state.scenario_page = "Overview"

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


def line_growth(weeks: List[str], series_dict: Dict[str, List[float]]):
    x = np.arange(len(weeks))
    fig, ax = plt.subplots(figsize=(7.2,3.8))
    for name, vals in series_dict.items():
        ax.plot(x, vals, marker='o', label=name)
        ax.fill_between(x, vals, step='pre', alpha=0.12)
    ax.set_xticks(x, weeks)
    ax.set_ylabel('Composite EP Score')
    ax.set_ylim(0, 10)
    ax.legend()
    st.pyplot(fig, use_container_width=False)

# -------------------------
# Layout Helpers
# -------------------------

def scenario_header(skey: str):
    s = SCENARIOS[skey]
    st.title(s["title"])
    st.write(s["overview"]) 
    chips = ''.join([f'<span class="chip">{c}</span>' for c in s["chips"]])
    st.markdown(chips, unsafe_allow_html=True)

    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown('<div class="metric"><div class="kpi-title">Session Length</div><h3>12–15 min</h3></div>', unsafe_allow_html=True)
    with k2:
        st.markdown('<div class="metric"><div class="kpi-title">Scenario Difficulty</div><h3>Progressive</h3></div>', unsafe_allow_html=True)
    with k3:
        st.markdown('<div class="metric"><div class="kpi-title">Focus Areas</div><h3>Gravitas • Persuasion • Control</h3></div>', unsafe_allow_html=True)


def scenario_brief(skey: str):
    b = SCENARIOS[skey]["brief"]
    st.header("Scenario Brief")
    st.markdown(f"- **Objective:** {b['objective']}\n- **Stakeholder:** {b['stakeholder']}\n- **Timebox:** {b['timebox']}")
    st.subheader("What You'll Be Assessed On")
    st.write(b["assessment"])


def scenario_baseline(skey: str):
    b = SCENARIOS[skey]["brief"]
    st.header("Baseline Simulation")
    st.write("Hold a live conversation with the avatar. Expect pushback and time pressure. Maintain composure, lead with outcomes, and secure agreement on value before price.")
    c1, c2 = st.columns([1,1])
    with c1:
        st.image(render_mock_avatar(300).getvalue(), caption="Avatar")
    with c2:
        st.markdown(f'<div class="callout">Client: “{b["prompt1"]}”</div>', unsafe_allow_html=True)
        st.success("This is a demo build. Live capture will be configured here.")


def scenario_coaching():
    st.header("Live Coaching Prompts")
    st.write("Non‑intrusive nudges appear when pacing, framing, or presence drifts. You stay in flow while receiving timely cues.")
    st.warning("Breathe. Shorten your sentence. Lead with impact → ROI in 90 days.")
    st.markdown("**Example Prompts**")
    st.markdown("- Slow down 10% — let the point land.\n- Anchor on outcomes before price.\n- Use a brief silence — regain control.\n- Translate features → CFO metrics.")


def scenario_feedback(skey: str):
    st.header("Feedback & Scorecard — Pre‑filled Attempts")
    radar_chart(
        DEFAULT_RADAR_LABELS,
        SCENARIOS[skey]["attempt_radar"],
        ["Attempt 1","Attempt 2","Attempt 3"],
    )
    st.divider()
    grouped_bar(
        DEFAULT_BAR_CATS,
        SCENARIOS[skey]["attempt_bars"],
        ["Attempt 1","Attempt 2","Attempt 3"],
    )
    st.info("Charts are pre‑filled with representative scores across three attempts. Live scoring will appear here.")


def scenario_learning():
    st.header("Targeted Learning Modules")
    st.write("After feedback, complete short modules that strengthen specific behaviors observed in your session.")
    with st.expander("ROI Story in 60s"):
        st.write("Craft a concise value narrative that anchors the discussion on outcomes.")
        st.button("Practice", type="primary", disabled=True)
        st.button("View Example", disabled=True)
    with st.expander("Handling Price Pushback"):
        st.write("Reframe discounts to risk‑adjusted ROI with confident wording.")
        st.button("Practice", type="primary", disabled=True)
        st.button("Drill", disabled=True)
    with st.expander("Composed Delivery"):
        st.write("Use pacing, pauses, and controlled gestures to project calm authority.")
        st.button("Practice", type="primary", disabled=True)
        st.button("Breathe", disabled=True)


def scenario_resim(skey: str):
    st.header("Re‑Simulation")
    st.write("Face the same persona with varied objection order. Demonstrate improved framing, calm under pressure, and a disciplined close.")
    st.image(render_mock_avatar(260).getvalue(), caption="Avatar")
    st.info("Demo build: re‑simulation logic will be configured here.")
    st.markdown("**What Good Looks Like**: Outcome anchor → risk plan → confident price defense → crisp close with agreed next step.")


def scenario_growth(skey: str):
    st.header("Your Journey Over Time")
    # derive composite means per attempt to simulate growth curve
    attempts = SCENARIOS[skey]["attempt_radar"]
    a1 = float(np.mean(attempts[0])); a2 = float(np.mean(attempts[1])); a3 = float(np.mean(attempts[2]))
    baseline = list(np.linspace(a1-3, a1+1, len(WEEKS)))
    actual = list(np.linspace(a1, a3, len(WEEKS)))
    line_growth(WEEKS, {"Baseline Path": baseline, "Actual With Learning": actual})
    st.subheader("Export Portfolio")
    st.write("Download a concise report with highlights, before/after clips, and mastered behaviors.")
    st.button("Download Report", disabled=True)


# -------------------------
# Sidebar Navigation
# -------------------------
if st.session_state.view == "dashboard":
    st.sidebar.header("Navigate")
    st.sidebar.radio("", ["Student Dashboard"], index=0, label_visibility="collapsed")
else:
    skey = st.session_state.scenario_key
    st.sidebar.header("Scenario")
    st.sidebar.write(f"**{SCENARIOS[skey]['title']}**")
    page = st.sidebar.radio("Navigate", [
        "Overview","Scenario Brief","Baseline Simulation","Live Coaching",
        "Feedback","Learning Modules","Re‑Simulation","Growth Dashboard"
    ], index=["Overview","Scenario Brief","Baseline Simulation","Live Coaching","Feedback","Learning Modules","Re‑Simulation","Growth Dashboard"].index(st.session_state.scenario_page))
    st.session_state.scenario_page = page
    if st.sidebar.button("← Back to Dashboard"):
        st.session_state.view = "dashboard"
        st.session_state.scenario_key = None
        st.session_state.scenario_page = "Overview"
        st.experimental_rerun()

# -------------------------
# Main Views
# -------------------------
if st.session_state.view == "dashboard":
    st.title("Your Executive Presence Simulations")
    st.write("Select a simulation to begin. All pages are configured with placeholders where live features will appear.")

    # Only three simulations
    sims = [
        {"key":"Negotiation","status":"In Progress"},
        {"key":"BoardUpdate","status":"Assigned"},
        {"key":"CrisisComms","status":"Assigned"},
    ]

    cols = st.columns(3)
    for i, sim in enumerate(sims):
        skey = sim["key"]; meta = SCENARIOS[skey]
        with cols[i]:
            st.subheader(meta["title"])
            status_color = "#34d399" if sim["status"]=="In Progress" else "#60a5fa"
            st.markdown(f"<span class='status-dot' style='background:{status_color}'></span>**{sim['status']}**", unsafe_allow_html=True)
            score = round(float(np.mean(meta["attempt_radar"][2])), 1)
            st.metric("Latest Composite Score", score)
            btn_label = "Resume" if sim["status"]=="In Progress" else "Start"
            if st.button(btn_label, key=f"btn_{skey}"):
                st.session_state.view = "scenario"
                st.session_state.scenario_key = skey
                st.session_state.scenario_page = "Overview"
                st.experimental_rerun()

    st.divider()
    st.caption("Note: If a control is not yet live, the page will display a clear placeholder instead of an error.")

else:
    # Scenario view
    skey = st.session_state.scenario_key
    page = st.session_state.scenario_page

    # Defensive guards
    if skey not in SCENARIOS:
        st.error("Scenario not found. Use the sidebar to go back to the dashboard.")
    else:
        if page == "Overview":
            scenario_header(skey)
        elif page == "Scenario Brief":
            scenario_brief(skey)
        elif page == "Baseline Simulation":
            scenario_baseline(skey)
        elif page == "Live Coaching":
            scenario_coaching()
        elif page == "Feedback":
            scenario_feedback(skey)
        elif page == "Learning Modules":
            scenario_learning()
        elif page == "Re‑Simulation":
            scenario_resim(skey)
        elif page == "Growth Dashboard":
            scenario_growth(skey)
        else:
            st.info("This section will be configured. Please select another tab.")

st.markdown("---")
st.caption("This simulation is designed to help you build presence, persuasion, and composure in high‑stakes conversations. Complete the learning modules between attempts for best results.")

# requirements.txt
# streamlit
# matplotlib
# numpy
