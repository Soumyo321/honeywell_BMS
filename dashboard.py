# dashboard.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from simulator import BuildingSimulator
from database import init_db, get_recent_decisions, get_energy_history
from control_loop import run_single_cycle, simulator
from config import BUILDING_CONFIG
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(
    page_title="Smart Building AI — Honeywell",
    page_icon="🏢",
    layout="wide"
)

init_db()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Header
st.title("🏢 Smart Building AI — Autonomous Optimization System")
st.caption("Powered by Llama 3.3-70B via Groq | MCP Tool Calling | Real-time Closed Loop Control | ASHRAE 90.1 Energy Standards")

# Scenario buttons
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("▶️ Run Cycle", use_container_width=True):
        with st.spinner("AI reasoning..."):
            result = run_single_cycle()
        st.rerun()
with col2:
    if st.button("🔥 Heatwave", use_container_width=True):
        simulator.apply_scenario("heatwave")
        with st.spinner("AI responding to heatwave..."):
            result = run_single_cycle()
        st.rerun()
with col3:
    if st.button("👥 Surge", use_container_width=True):
        simulator.apply_scenario("occupancy_surge")
        with st.spinner("AI responding to surge..."):
            result = run_single_cycle()
        st.rerun()
with col4:
    if st.button("⚡ Power Save", use_container_width=True):
        simulator.apply_scenario("power_saving")
        with st.spinner("Activating power save..."):
            result = run_single_cycle()
        st.rerun()
with col5:
    if st.button("🔄 Reset", use_container_width=True):
        simulator.apply_scenario("normal")
        with st.spinner("Resetting..."):
            result = run_single_cycle()
        st.rerun()

st.divider()

# Metrics
energy_history = get_energy_history(50)
if energy_history:
    latest = energy_history[0]
    total_energy = latest[1]
    baseline = latest[2]
    saved = latest[3]
    comfort = latest[4]
else:
    total_energy = simulator.get_total_energy()
    baseline = BUILDING_CONFIG["baseline_energy_per_hour"]
    saved = baseline - total_energy
    comfort = 100.0

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("⚡ Energy Now", f"{total_energy} kWh", f"-{round((saved/baseline)*100, 1)}% vs baseline")
with m2:
    st.metric("💰 Energy Saved", f"{round(saved, 2)} kWh", "vs 50kWh baseline")
with m3:
    st.metric("😊 Comfort Score", f"{comfort}%", "occupied rooms")
with m4:
    st.metric("🌿 Carbon Avoided", f"{round(saved * 0.233, 2)} kg CO₂", "India grid factor")

st.divider()

# Outdoor temp
rooms_data = simulator.get_all_rooms_data()
if rooms_data:
    st.info(f"🌤️ Real outdoor temperature (Bhopal): {simulator.outdoor_temp}°C")

# Room cards
st.subheader("🏠 Live Room Status")
cols = st.columns(4)
for i, room in enumerate(rooms_data):
    with cols[i]:
        temp_ok = 21 <= room["temperature"] <= 24
        co2_ok = room["co2"] <= 1000
        temp_icon = "✅" if temp_ok else "⚠️"
        co2_icon = "✅" if co2_ok else "❌"
        occupied = room["occupancy"] > 0

        st.markdown(f"### {room['name']}")
        st.markdown(f"{'🟢 Occupied' if occupied else '⚫ Empty'}")
        st.metric("🌡️ Temperature", f"{room['temperature']}°C")
        st.markdown(f"{temp_icon} Setpoint: **{room['ac_setpoint']}°C**")
        st.metric("💨 CO₂", f"{room['co2']} ppm")
        st.markdown(f"{co2_icon} Limit: 1000ppm")
        st.metric("👥 Occupancy", f"{room['occupancy']} people")
        st.progress(float(room["lighting_level"]), text=f"💡 Lighting: {int(room['lighting_level']*100)}%")
        st.progress(float(room["ventilation_level"]), text=f"🌬️ Ventilation: {int(room['ventilation_level']*100)}%")
        st.metric("⚡ Energy", f"{room['energy_consumption']} kWh")

st.divider()

# Energy chart
st.subheader("📊 Energy Consumption vs Baseline")
if energy_history:
    df = pd.DataFrame(energy_history, columns=["timestamp", "total_energy", "baseline_energy", "energy_saved", "comfort_score"])
    df = df.iloc[::-1].reset_index(drop=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["timestamp"], y=df["baseline_energy"],
        name="Baseline (No AI)", line=dict(color="red", dash="dash")
    ))
    fig.add_trace(go.Scatter(
        x=df["timestamp"], y=df["total_energy"],
        name="Actual (With AI)", line=dict(color="green"),
        fill="tonexty", fillcolor="rgba(0,255,0,0.1)"
    ))
    fig.update_layout(xaxis_title="Time", yaxis_title="Energy (kWh)", height=350, margin=dict(l=0,r=0,t=30,b=0))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Click Run Cycle to start collecting data")

st.divider()

# Decisions + Chat
left, right = st.columns([1, 1])

with left:
    st.subheader("🤖 AI Decision Log")
    decisions = get_recent_decisions(15)
    if decisions:
        for d in decisions:
            timestamp, room_id, action, reason, e_before, e_after = d
            time_str = timestamp[11:19]
            with st.expander(f"[{time_str}] {action[:50]}..."):
                st.write(f"**Room:** {room_id}")
                st.write(f"**Action:** {action}")
                st.write(f"**Reason:** {reason}")
                st.write(f"**Energy:** {e_before} → {e_after} kWh")
    else:
        st.info("No decisions yet. Click Run Cycle.")

with right:
    st.subheader("💬 Chat with Building AI")
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask the building AI anything...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        rooms_summary = "\n".join([
            f"{r['name']}: Temp={r['temperature']}°C, CO2={r['co2']}ppm, Occupancy={r['occupancy']}, Energy={r['energy_consumption']}kWh"
            for r in rooms_data
        ])

        system_prompt = f"""You are an intelligent Building Management System AI.
Current status:
{rooms_summary}
Outdoor Temp: {simulator.outdoor_temp}°C (real weather data from Bhopal)
Total Energy: {total_energy} kWh | Baseline: {baseline} kWh | Saved: {round(saved,2)} kWh
Comfort Score: {comfort}%
Answer questions about the building concisely and helpfully."""

        messages = [{"role": "system", "content": system_prompt}]
        for msg in st.session_state.chat_history[-6:]:
            messages.append(msg)

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            max_tokens=500
        )

        reply = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

st.divider()
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Real weather: Bhopal, India | Carbon factor: 0.233 kg CO₂/kWh (CEA 2023)")