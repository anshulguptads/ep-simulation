import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# Session state initialization
# ---------------------------
if "attempt1_scores" not in st.session_state:
    st.session_state.attempt1_scores = [6, 6, 6, 6, 6]
if "attempt2_scores" not in st.session_state:
    st.session_state.attempt2_scores = [8, 8, 8, 8, 8]
if "bar_attempt1" not in st.session_state:
    st.session_state.bar_attempt1 = [6, 6, 6]
if "bar_attempt2" not in st.session_state:
    st.session_state.bar_attempt2 = [8, 8, 8]
if "reset" not in st.session_state:
    st.session_state.reset = False

# ---------------------------
# Helper functions for charts
# ---------------------------
def radar_chart(labels, attempt1, attempt2):
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    attempt1 += attempt1[:1]
    attempt2 += attempt2[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, attempt1, "o-", linewidth=2, label="Attempt 1")
    ax.fill(angles, attempt1, alpha=0.25)
    ax.plot(angles, attempt2, "o-", linewidth=2, label="Attempt 2")
    ax.fill(angles, attempt2, alpha=0.25)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_ylim(0, 10)
    ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))
    return fig

def bar_chart(categories, attempt1, attempt2):
    x = np.arange(len(categories))
    width = 0.35
    fig, ax = plt.subplots()
    ax.bar(x - width/2, attempt1, width, label="Attempt 1")
    ax.bar(x + width/2, attempt2, width, label="Attempt 2")
    ax.set_ylabel("Score")
    ax.set_title("Component-wise Performance")
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylim(0, 10)
    ax.legend()
    return fig

def line_chart(attempt1_avg, attempt2_avg):
    weeks = np.arange(1, 7)
    # simple interpolation for mock data
    scores1 = np.linspace(attempt1_avg, attempt1_avg + 0.5, 6)
    scores2 = np.linspace(attempt2_avg, attempt2_avg + 0.5, 6)
    fig, ax = plt.subplots()
    ax.plot(weeks, scores1, marker="o", label="Attempt 1 Trajectory")
    ax.plot(weeks, scores2, marker="o", label="Attempt 2 Trajectory")
    ax.set_xlabel("Week")
    ax.set_ylabel("Score")
    ax.set_title("Week-over-Week Growth")
    ax.set_ylim(0, 10)
    ax.legend()
    return fig

# ---------------------------
# Sidebar Navigation
# ---------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Home",
    "Scenario Brief",
    "Baseline Simulation",
    "Live Coaching",
    "Feedback",
    "Skill-Building",
    "Re-Simulation",
    "Growth Dashboard"
])

if st.sidebar.button("Reset Demo Data"):
    st.session_state.attempt1_scores = [6, 6, 6, 6, 6]
    st.session_state.attempt2_scores = [8, 8, 8, 8, 8]
    st.session_state.bar_attempt1 = [6, 6, 6]
    st.session_state.bar_attempt2 = [8, 8, 8]
    st.session_state.reset = True

# ---------------------------
# Pages
# ---------------------------
if page == "Home":
    st.title("Executive Presence Simulator")
    st.subheader("High-Stakes Client Negotiation (EMBA)")
    st.markdown("""
    Welcome to the Executive Presence (EP) simulation — a safe, AI-driven environment 
    for practicing complex, high-pressure scenarios. This journey focuses on 
    **renewing a multi-million-dollar global account** with a C-suite client while facing 
    competitive offers. You will experience:
    
    - A realistic boardroom negotiation with adaptive challenges.
    - Live micro-coaching during the conversation.
    - Detailed performance feedback across EP dimensions.
    - Guided skill-building modules.
    - A re-simulation to measure growth.
    """)
    st.image("https://via.placeholder.com/800x400.png?text=Mock+Avatar+Scene", caption="Your virtual client awaits...")

elif page == "Scenario Brief":
    st.header("Scenario Brief")
    st.markdown("""
    **Background:**  
    You are representing your company in a renewal negotiation for a high-value global account. 
    The client, a Fortune 500 CFO, is entertaining offers from competitors and questioning 
    ROI from the current partnership.

    **Objective:**  
    - Renewal at target terms  
    - Upsell entry into an additional service line

    **Stakeholder Profile:**  
    - Risk-averse, ROI-driven  
    - Expects confident, concise, data-backed communication
    """)

elif page == "Baseline Simulation":
    st.header("Baseline Simulation")
    st.markdown("""
    In this first attempt, you will engage in a simulated negotiation with the virtual client.
    They will raise objections, challenge pricing, and test your ability to maintain control.
    
    Speak naturally, as you would in a real meeting.
    """)
    st.image("https://via.placeholder.com/800x400.png?text=Video+Call+with+Client", caption="Live simulation feed")

elif page == "Live Coaching":
    st.header("Live Coaching Cues")
    st.markdown("""
    During the simulation, you will receive discreet on-screen cues such as:
    - *\"Slow your pace — client appears unconvinced.\"*
    - *\"Reframe value in ROI terms.\"*
    - *\"Pause for impact after key points.\"*
    """)
    st.image("https://via.placeholder.com/600x300.png?text=On-screen+Coaching+Prompts", caption="Example coaching overlay")

elif page == "Feedback":
    st.header("Feedback & Scorecard")
    st.markdown("""
    Adjust your Attempt 1 and Attempt 2 scores below to simulate performance outcomes.
    **EP Dimensions:** Gravitas, Persuasion, Vocal, Gestures, Brevity
    """)
    labels = ["Gravitas", "Persuasion", "Vocal", "Gestures", "Brevity"]

    st.subheader("Attempt 1 Scores")
    att1 = [st.slider(f"{label} (Attempt 1)", 0, 10, st.session_state.attempt1_scores[i]) for i, label in enumerate(labels)]
    if st.button("Save Attempt 1"):
        st.session_state.attempt1_scores = att1

    st.subheader("Attempt 2 Scores")
    att2 = [st.slider(f"{label} (Attempt 2)", 0, 10, st.session_state.attempt2_scores[i]) for i, label in enumerate(labels)]
    if st.button("Save Attempt 2"):
        st.session_state.attempt2_scores = att2

    st.pyplot(radar_chart(labels, st.session_state.attempt1_scores[:], st.session_state.attempt2_scores[:]))

    st.markdown("### Component-wise Scores")
    categories = ["Opening", "Objections", "Close"]
    bar1 = [st.slider(f"{cat} (Attempt 1)", 0, 10, st.session_state.bar_attempt1[i]) for i, cat in enumerate(categories)]
    if st.button("Save Bars Attempt 1"):
        st.session_state.bar_attempt1 = bar1
    bar2 = [st.slider(f"{cat} (Attempt 2)", 0, 10, st.session_state.bar_attempt2[i]) for i, cat in enumerate(categories)]
    if st.button("Save Bars Attempt 2"):
        st.session_state.bar_attempt2 = bar2

    st.pyplot(bar_chart(categories, st.session_state.bar_attempt1, st.session_state.bar_attempt2))

elif page == "Skill-Building":
    st.header("Targeted Skill-Building Modules")
    st.markdown("""
    Based on your feedback, here are suggested drills:
    - **30-Second ROI Pitch** — Frame your value proposition concisely.
    - **Price Objection Handling** — Defend pricing with confidence and data.
    - **Executive Body Language** — Project control through posture and gestures.
    """)
    st.image("https://via.placeholder.com/600x300.png?text=Micro-learning+Module", caption="Sample learning module layout")

elif page == "Re-Simulation":
    st.header("Re-Simulation")
    st.markdown("""
    Now, apply your newly honed skills in a second simulated negotiation.
    Expect the client to vary their objections and negotiation tactics.
    """)
    st.image("https://via.placeholder.com/800x400.png?text=Second+Simulation+Video", caption="Live re-simulation")

elif page == "Growth Dashboard":
    st.header("Growth Dashboard")
    st.markdown("""
    **Week-over-Week Growth**  
    This chart shows your improvement trajectory between the first and second attempts across a simulated 6-week period.
    """)
    attempt1_avg = np.mean(st.session_state.attempt1_scores)
    attempt2_avg = np.mean(st.session_state.attempt2_scores)
    st.pyplot(line_chart(attempt1_avg, attempt2_avg))
