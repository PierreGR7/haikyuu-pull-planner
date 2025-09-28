import streamlit as st
import json
from datetime import datetime
from calculator import calculate_pulls, is_goal_reached
from parameters import daily_income, weekly_income, monthly_income, gems_per_pull, banner_tickets

# config
st.set_page_config(page_title="Haikyuu Pull Planner", page_icon="🏐", layout="centered")

# css
st.markdown(
    """
    <style>
    .stApp {
        background-color: #fdf6f0; /* light background */
        color: #222;
    }
    .result-box {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0px 0px 5px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# explanation
with st.expander("ℹ️ See how calculations are done"):
    st.markdown(
        """
        **Calculator Parameters**
        
        - **UR ticket = 150 gems**
        - **Daily income = 200 gems**  
          (60 daily missions + 85 training + 30 free time + 15 summit challenge + 10 PVP)
        - **Weekly income = 800 gems**  
          (100 weekly missions + 150 chill games + 50 club + 120 weekend bonus + 380 specialty test)
        - **Monthly income = 1830 gems**  
          (350 PvP ranking + 2×640 match streak + 150 update compensation + 50 calendar)
        - **Banner tickets = 15 per banner**  
          (login bonuses + event shop)
        """
    )

# Load banners
with open("DATA/incoming_banner.json", "r") as f:
    banners = json.load(f)

st.title("🏐 Haikyuu Pull Planner")
st.markdown("Plan your pulls and check if you will reach pity before the banner ends!")

today = datetime.today().date()
upcoming_banners = [
    (b["character"], datetime.fromisoformat(b["start_date"]).date(), datetime.fromisoformat(b["end_date"]).date(), b["is_rerun"])
    for b in banners
    if datetime.fromisoformat(b["end_date"]).date() >= today
]

# Banner selector
banner_options = [f"{char}{' (Rerun)' if rerun else ''} — {start} → {end}" for char, start, end, rerun in upcoming_banners]
choice = st.selectbox("Select the banner you are aiming for:", banner_options)

selected_index = banner_options.index(choice)
target_char, start_date, end_date, _ = upcoming_banners[selected_index]
days_until_banner = (end_date - today).days
banner_count = selected_index + 1
total_banner_tickets = banner_count * banner_tickets

st.write(f"🎯 **Selected Banner:** {target_char}")
st.write(f"⏳ Ends on **{end_date}** — in **{days_until_banner} days**")
st.write(f"🎟️ Total banner tickets expected: **{total_banner_tickets}**")

# User inputs
current_gems = st.number_input("💎 Current gems:", min_value=0, step=10)
current_tickets = st.number_input("🎟️ Current UR tickets:", min_value=0, step=1)
pity_remaining = st.number_input("📊 Pity remaining (pulls needed for guarantee):", min_value=0, max_value=140, step=1)

if st.button("Calculate"):
    result = calculate_pulls(current_gems, current_tickets, pity_remaining, days_until_banner)
    result["pulls_from_banner"] = total_banner_tickets
    result["total_pulls"] = result["pulls_from_gems"] + result["pulls_from_tickets"] + result["pulls_from_banner"]

    goal_reached, remaining_pulls = is_goal_reached(result["total_pulls"], result["pity_needed"])

    st.markdown("### 📊 Results")
    st.markdown(
        f"""
        <div class="result-box">
        <b>Total predicted gems:</b> {result['total_gems']}<br>
        <b>Pulls from gems:</b> {result['pulls_from_gems']}<br>
        <b>Current UR tickets:</b> {result['pulls_from_tickets']}<br>
        <b>Banner tickets:</b> {result['pulls_from_banner']}<br>
        <b>Total available pulls:</b> {result['total_pulls']}<br>
        <b>Pulls needed for pity:</b> {result['pity_needed']}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if goal_reached:
        st.success(f"✅ Goal reached! Surplus: {abs(remaining_pulls)} pulls")
    else:
        st.error(f"❌ Not enough... you still need {abs(remaining_pulls)} pulls")

# Bas de page

st.markdown(
    """
    <div style="
        margin-top: 2rem;
        padding: 0.8rem;
        background-color: #f1f1f1;
        border-radius: 8px;
        text-align: center;
        font-size: 0.9rem;
    ">
        Made by <b>Pierre Graef</b> — Data Engineer<br>
        🌐 <a href="https://www.pierregraef.com" target="_blank" style="text-decoration:none; color:#FF6600;">pierregraef.com</a>
    </div>
    """,
    unsafe_allow_html=True,
)