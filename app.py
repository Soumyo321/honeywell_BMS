# # # app.py
# # import streamlit as st
# # import plotly.graph_objects as go
# # import pandas as pd
# # import sqlite3
# # import subprocess

# # st.set_page_config(
# #     page_title="Smart Building AI",
# #     page_icon="🏢",
# #     layout="wide"
# # )

# # st.title("🏢 Honeywell Smart Building AI")
# # st.caption("Real EnergyPlus + Groq LLM + MCP Tool Calling + Autonomous HVAC")

# # # Sidebar
# # with st.sidebar:
# #     st.header("Control")
    
# #     run_btn = st.button("▶️ RUN SIMULATION", use_container_width=True, type="primary")
    
# #     if run_btn:
# #         with st.spinner("Running EnergyPlus + LLM... (30-60 seconds)"):
# #             result = subprocess.run(
# #                 ["python", "submission_runner.py"],
# #                 capture_output=False,
# #                 timeout=300
# #             )
# #         st.success("Done! Scroll down to see results.")
# #         st.rerun()
    
# #     st.divider()
# #     st.info("""
# # **Stack:**
# # - EnergyPlus 23.2 physics
# # - Llama 3.3-70B via Groq
# # - MCP tool calling pattern
# # - ASHRAE 55 comfort standard
# # - SQLite audit trail
# #     """)

# # # Load data
# # def load_data():
# #     try:
# #         conn = sqlite3.connect("building_data.db")
        
# #         sensors = pd.read_sql_query(
# #             "SELECT * FROM sensor_readings ORDER BY id", conn
# #         )
# #         decisions = pd.read_sql_query(
# #             "SELECT * FROM ai_decisions ORDER BY id DESC LIMIT 30", conn
# #         )
# #         energy = pd.read_sql_query(
# #             "SELECT * FROM energy_log ORDER BY id", conn
# #         )
        
# #         conn.close()
# #         return sensors, decisions, energy
# #     except:
# #         return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# # sensors, decisions, energy = load_data()

# # if sensors.empty:
# #     st.info("Click **RUN SIMULATION** in the sidebar to start.")
# #     st.stop()

# # # Metrics
# # st.subheader("Live Metrics")
# # col1, col2, col3, col4 = st.columns(4)

# # latest_temp = sensors["temperature"].iloc[-1] if not sensors.empty else 0
# # total_decisions = len(decisions)
# # latest_energy = energy["total_energy"].iloc[-1] if not energy.empty else 0
# # baseline = energy["baseline_energy"].iloc[-1] if not energy.empty else 8.0
# # saved = baseline - latest_energy
# # pct = (saved / baseline * 100) if baseline > 0 else 0

# # with col1:
# #     st.metric("Temperature", f"{latest_temp:.1f}°C",
# #               delta="Comfort OK" if 21 <= latest_temp <= 24 else "Adjusting")
# # with col2:
# #     st.metric("AI Decisions", total_decisions, delta="Autonomous")
# # with col3:
# #     st.metric("Energy Saved", f"{saved:.2f} kWh", delta=f"-{pct:.1f}%")
# # with col4:
# #     comfort = energy["comfort_score"].mean() if not energy.empty else 0
# #     st.metric("Avg Comfort", f"{comfort:.1f}%", delta="ASHRAE 55")

# # st.divider()

# # # Temperature chart
# # col_left, col_right = st.columns(2)

# # with col_left:
# #     st.subheader("Temperature Over Time")
# #     fig1 = go.Figure()
# #     fig1.add_trace(go.Scatter(
# #         x=sensors["timestamp"], y=sensors["temperature"],
# #         name="Zone Temp", line=dict(color="orange"), mode="lines"
# #     ))
# #     fig1.add_trace(go.Scatter(
# #         x=sensors["timestamp"], y=sensors["ac_setpoint"],
# #         name="Heating SP", line=dict(color="red", dash="dash"), mode="lines"
# #     ))
# #     fig1.add_hrect(y0=21, y1=24, fillcolor="green", opacity=0.1,
# #                    annotation_text="Comfort Zone")
# #     fig1.update_layout(height=350, hovermode="x unified",
# #                        yaxis_title="Temperature (C)")
# #     st.plotly_chart(fig1, use_container_width=True)

# # with col_right:
# #     st.subheader("Energy: AI vs Baseline")
# #     fig2 = go.Figure()
# #     fig2.add_trace(go.Scatter(
# #         x=energy["timestamp"], y=energy["baseline_energy"],
# #         name="Baseline (No AI)", line=dict(color="red", dash="dash"), mode="lines"
# #     ))
# #     fig2.add_trace(go.Scatter(
# #         x=energy["timestamp"], y=energy["total_energy"],
# #         name="With AI", line=dict(color="green"), fill="tonexty",
# #         fillcolor="rgba(0,200,0,0.15)", mode="lines"
# #     ))
# #     fig2.update_layout(height=350, hovermode="x unified",
# #                        yaxis_title="Energy (kWh)")
# #     st.plotly_chart(fig2, use_container_width=True)

# # st.divider()

# # # Decision log
# # st.subheader("AI Decision Log")
# # if not decisions.empty:
# #     for _, row in decisions.iterrows():
# #         with st.expander(f"[{row['timestamp'][:19]}] {row['action']}"):
# #             st.write(f"**Action:** {row['action']}")
# #             st.write(f"**Reason:** {row['reason']}")
# #             st.write(f"**Energy:** {row['energy_before']} → {row['energy_after']} kWh")
# # else:
# #     st.info("No decisions yet")

# # st.divider()
# # st.caption("Real EnergyPlus simulation | Groq Llama 3.3-70B | MCP Pattern")


# # app.py
# import streamlit as st
# import plotly.graph_objects as go
# import pandas as pd
# import sqlite3
# import subprocess
# from groq import Groq
# from config import GROQ_API_KEY, GROQ_MODEL

# st.set_page_config(
#     page_title="Smart Building AI",
#     page_icon="🏢",
#     layout="wide"
# )

# st.title("🏢 Honeywell Smart Building AI")
# st.caption("Real EnergyPlus + Groq LLM + MCP Tool Calling + Autonomous HVAC")

# # Sidebar
# with st.sidebar:
#     st.header("Control")
    
#     run_btn = st.button("▶️ RUN SIMULATION", use_container_width=True, type="primary")
    
#     if run_btn:
#         import os
#         if os.path.exists("building_data.db"):
#             os.remove("building_data.db")
        
#         with st.spinner("Running EnergyPlus + LLM... (30-60 seconds)"):
#             result = subprocess.run(
#                 ["python", "submission_runner.py"],
#                 capture_output=False,
#                 timeout=300
#             )
#         st.success("Done! Scroll down to see results.")
#         st.rerun()
    
#     st.divider()
#     st.info("""
# **Stack:**
# - EnergyPlus 23.2 physics
# - Llama 3.3-70B via Groq
# - MCP tool calling pattern
# - ASHRAE 55 comfort standard
# - SQLite audit trail
#     """)

# # Load data
# def load_data():
#     try:
#         conn = sqlite3.connect("building_data.db")
        
#         sensors = pd.read_sql_query(
#             "SELECT * FROM sensor_readings ORDER BY id", conn
#         )
#         decisions = pd.read_sql_query(
#             "SELECT * FROM ai_decisions ORDER BY id DESC LIMIT 30", conn
#         )
#         energy = pd.read_sql_query(
#             "SELECT * FROM energy_log ORDER BY id", conn
#         )
        
#         conn.close()
#         return sensors, decisions, energy
#     except:
#         return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# sensors, decisions, energy = load_data()

# if sensors.empty:
#     st.info("Click **RUN SIMULATION** in the sidebar to start.")
#     st.stop()

# # Metrics
# st.subheader("Live Metrics")
# col1, col2, col3, col4 = st.columns(4)

# latest_temp = sensors["temperature"].iloc[-1] if not sensors.empty else 0
# total_decisions = len(decisions)
# latest_energy = energy["total_energy"].iloc[-1] if not energy.empty else 0
# baseline = energy["baseline_energy"].iloc[-1] if not energy.empty else 8.0
# saved = baseline - latest_energy
# pct = (saved / baseline * 100) if baseline > 0 else 0

# with col1:
#     st.metric("Temperature", f"{latest_temp:.1f}°C",
#               delta="Comfort OK" if 21 <= latest_temp <= 24 else "Adjusting")
# with col2:
#     st.metric("AI Decisions", total_decisions, delta="Autonomous")
# with col3:
#     st.metric("Energy Saved", f"{saved:.2f} kWh", delta=f"{pct:.1f}% reduction")
# with col4:
#     comfort = energy["comfort_score"].mean() if not energy.empty else 0
#     st.metric("Avg Comfort", f"{comfort:.1f}%", delta="ASHRAE 55")

# st.divider()

# # Temperature chart
# col_left, col_right = st.columns(2)

# with col_left:
#     st.subheader("Temperature Over Time")
#     fig1 = go.Figure()
#     fig1.add_trace(go.Scatter(
#         x=sensors["timestamp"], y=sensors["temperature"],
#         name="Zone Temp", line=dict(color="orange"), mode="lines"
#     ))
#     fig1.add_trace(go.Scatter(
#         x=sensors["timestamp"], y=sensors["ac_setpoint"],
#         name="Heating SP", line=dict(color="red", dash="dash"), mode="lines"
#     ))
#     fig1.add_hrect(y0=21, y1=24, fillcolor="green", opacity=0.1,
#                    annotation_text="Comfort Zone")
#     fig1.update_layout(height=350, hovermode="x unified",
#                        yaxis_title="Temperature (C)")
#     st.plotly_chart(fig1, use_container_width=True)

# with col_right:
#     st.subheader("Energy: AI vs Baseline")
#     fig2 = go.Figure()
#     fig2.add_trace(go.Scatter(
#         x=energy["timestamp"], y=energy["baseline_energy"],
#         name="Baseline (No AI)", line=dict(color="red", dash="dash"), mode="lines"
#     ))
#     fig2.add_trace(go.Scatter(
#         x=energy["timestamp"], y=energy["total_energy"],
#         name="With AI", line=dict(color="green"), fill="tonexty",
#         fillcolor="rgba(0,200,0,0.15)", mode="lines"
#     ))
#     fig2.update_layout(height=350, hovermode="x unified",
#                        yaxis_title="Energy (kWh)")
#     st.plotly_chart(fig2, use_container_width=True)

# st.divider()

# # Decision log
# st.subheader("AI Decision Log")
# if not decisions.empty:
#     for _, row in decisions.iterrows():
#         with st.expander(f"[{row['timestamp'][:19]}] {row['action']}"):
#             st.write(f"**Action:** {row['action']}")
#             st.write(f"**Reason:** {row['reason']}")
#             st.write(f"**Energy:** {row['energy_before']} → {row['energy_after']} kWh")
# else:
#     st.info("No decisions yet")

# st.divider()

# # ============================================================================
# # CHATBOT SECTION
# # ============================================================================

# st.subheader("💬 Ask Building AI")

# # Initialize chat history in session state
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # Display chat history
# for message in st.session_state.chat_history:
#     with st.chat_message(message["role"]):
#         st.write(message["content"])

# # Chat input
# user_input = st.chat_input("Ask about the simulation, energy, temperature, decisions...")

# if user_input:
#     # Add user message to history
#     st.session_state.chat_history.append({"role": "user", "content": user_input})
    
#     # Prepare context from simulation data
#     context = f"""
#     You are an AI assistant for a smart building management system.
    
#     Current Building State:
#     - Current Temperature: {latest_temp:.1f}°C
#     - Average Comfort Score: {comfort:.1f}%
#     - Total Energy Used: {latest_energy:.2f} kWh
#     - Baseline Energy (No AI): {baseline:.2f} kWh
#     - Energy Saved: {saved:.2f} kWh ({pct:.1f}%)
#     - Total AI Decisions Made: {total_decisions}
#     - Temperature Range: {sensors['temperature'].min():.1f}°C to {sensors['temperature'].max():.1f}°C
#     - Comfort Zone Target: 21-24°C
    
#     Recent AI Decisions:
#     """
    
#     # Add recent decisions to context
#     if not decisions.empty:
#         for _, decision in decisions.head(5).iterrows():
#             context += f"\n- {decision['timestamp']}: {decision['action']} (Reason: {decision['reason'][:80]})"
    
#     context += "\n\nAnswer the user's question based on this simulation data. Be helpful and specific."
    
#     # Get response from LLM
#     client = Groq(api_key=GROQ_API_KEY)
    
#     response = client.chat.completions.create(
#         model=GROQ_MODEL,
#         messages=[
#             {"role": "system", "content": context},
#             {"role": "user", "content": user_input}
#         ],
#         max_tokens=500,
#         temperature=0.7
#     )
    
#     assistant_message = response.choices[0].message.content
    
#     # Add assistant message to history
#     st.session_state.chat_history.append({"role": "assistant", "content": assistant_message})
    
#     # Display the new response
#     with st.chat_message("assistant"):
#         st.write(assistant_message)

# st.divider()
# st.caption("Real EnergyPlus simulation | Groq Llama 3.3-70B | MCP Pattern | Live Building AI")


# app.py
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sqlite3
import subprocess
import os
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

st.set_page_config(
    page_title="Honeywell Smart Building AI",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stMetric {
        background: linear-gradient(135deg, #1e2130, #252840);
        border: 1px solid #2d3250;
        border-radius: 12px;
        padding: 16px;
    }
    .stMetric label { color: #a0aec0 !important; font-size: 13px !important; }
    .stMetric [data-testid="metric-container"] > div:nth-child(2) {
        font-size: 28px !important; font-weight: 700 !important; color: #ffffff !important;
    }
    .header-banner {
        background: linear-gradient(135deg, #1a1f35 0%, #0d1117 50%, #1a2535 100%);
        border: 1px solid #2d3250;
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 8px;
    }
    .badge-green { background: #0d2818; color: #48bb78; border: 1px solid #276749; }
    .badge-blue  { background: #0d1f2d; color: #63b3ed; border: 1px solid #2b6cb0; }
    .badge-orange{ background: #2d1f0d; color: #ed8936; border: 1px solid #c05621; }
    div[data-testid="stExpander"] {
        background: #1a1f35;
        border: 1px solid #2d3250;
        border-radius: 10px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-banner">
    <h1 style="margin:0; color:#ffffff; font-size:28px;">🏢 Honeywell Smart Building AI</h1>
    <p style="margin:6px 0 12px 0; color:#718096; font-size:14px;">
        Autonomous HVAC Optimization • Real-time Control • Energy Intelligence
    </p>
    <span class="status-badge badge-green">● EnergyPlus 23.2 Physics</span>
    <span class="status-badge badge-blue">● Llama 3.3-70B via Groq</span>
    <span class="status-badge badge-orange">● MCP Tool Calling</span>
    <span class="status-badge badge-green">● ASHRAE 55 Standard</span>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Control Panel")
    run_btn = st.button("▶️ RUN SIMULATION", use_container_width=True, type="primary")

    if run_btn:
        if os.path.exists("building_data.db"):
            os.remove("building_data.db")
        with st.spinner("Running EnergyPlus + LLM..."):
            subprocess.run(["python", "submission_runner.py"], capture_output=False, timeout=300)
        st.success("✅ Simulation complete!")
        st.rerun()

    st.divider()
    st.markdown("""
**🔧 Tech Stack**
- 🏗️ EnergyPlus 23.2 physics engine
- 🤖 Llama 3.3-70B via Groq API
- 🔧 MCP tool calling pattern
- 📊 ASHRAE 55 comfort standard
- 🗄️ SQLite real-time audit trail
    """)

# Load data
def load_data():
    try:
        conn = sqlite3.connect("building_data.db")
        sensors   = pd.read_sql_query("SELECT * FROM sensor_readings ORDER BY id", conn)
        decisions = pd.read_sql_query("SELECT * FROM ai_decisions ORDER BY id DESC LIMIT 30", conn)
        energy    = pd.read_sql_query("SELECT * FROM energy_log ORDER BY id", conn)
        conn.close()
        return sensors, decisions, energy
    except:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

sensors, decisions, energy = load_data()

if sensors.empty:
    st.markdown("""
    <div style="text-align:center; padding:80px; color:#718096;">
        <div style="font-size:64px;">🏢</div>
        <h2 style="color:#a0aec0;">No Simulation Data Yet</h2>
        <p>Click <b>RUN SIMULATION</b> in the sidebar to start</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Compute metrics
latest_temp    = sensors["temperature"].iloc[-1]
total_decisions = len(decisions)
latest_energy  = energy["total_energy"].iloc[-1]
baseline       = energy["baseline_energy"].iloc[-1]
saved          = baseline - latest_energy
pct            = (saved / baseline * 100) if baseline > 0 else 0
comfort        = energy["comfort_score"].mean()
temp_min       = sensors["temperature"].min()
temp_max       = sensors["temperature"].max()

# Metrics row
st.markdown("### 📊 Live Metrics")
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    icon = "✅" if 21 <= latest_temp <= 24 else "⚠️"
    st.metric(f"{icon} Temperature", f"{latest_temp:.1f}°C",
              "Comfort OK" if 21 <= latest_temp <= 24 else "Adjusting")
with c2:
    st.metric("🤖 AI Decisions", total_decisions, "Autonomous")
with c3:
    st.metric("⚡ Energy Used", f"{latest_energy:.3f} kWh", f"Real EnergyPlus")
with c4:
    st.metric("💰 Energy Saved", f"{saved:.2f} kWh", f"{pct:.1f}% vs baseline")
with c5:
    st.metric("😊 Avg Comfort", f"{comfort:.1f}%", "ASHRAE 55")

st.divider()

# Charts row
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("#### 🌡️ Temperature Over Time")
    fig1 = go.Figure()
    fig1.add_hrect(y0=21, y1=24, fillcolor="rgba(72,187,120,0.08)",
                   line_width=0, annotation_text="✅ Comfort Zone 21-24°C",
                   annotation_position="top left",
                   annotation_font=dict(color="#48bb78", size=11))
    fig1.add_trace(go.Scatter(
        x=sensors["timestamp"], y=sensors["temperature"],
        name="Zone Temp", line=dict(color="#ed8936", width=2.5),
        mode="lines", fill="tozeroy", fillcolor="rgba(237,137,54,0.07)"
    ))
    fig1.add_trace(go.Scatter(
        x=sensors["timestamp"], y=sensors["ac_setpoint"],
        name="Heating SP", line=dict(color="#fc8181", dash="dash", width=1.5), mode="lines"
    ))
    fig1.update_layout(
        height=320, paper_bgcolor="#1a1f35", plot_bgcolor="#1a1f35",
        font=dict(color="#a0aec0"), hovermode="x unified",
        legend=dict(bgcolor="#1a1f35", bordercolor="#2d3250"),
        yaxis=dict(title="Temperature (°C)", gridcolor="#2d3250"),
        xaxis=dict(gridcolor="#2d3250"),
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.markdown("#### ⚡ Energy: AI vs Baseline")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=energy["timestamp"], y=energy["baseline_energy"],
        name="Baseline (No AI)", line=dict(color="#fc8181", dash="dash", width=2),
        mode="lines"
    ))
    fig2.add_trace(go.Scatter(
        x=energy["timestamp"], y=energy["total_energy"],
        name="With AI", line=dict(color="#48bb78", width=2.5),
        fill="tonexty", fillcolor="rgba(72,187,120,0.12)", mode="lines"
    ))
    fig2.update_layout(
        height=320, paper_bgcolor="#1a1f35", plot_bgcolor="#1a1f35",
        font=dict(color="#a0aec0"), hovermode="x unified",
        legend=dict(bgcolor="#1a1f35", bordercolor="#2d3250"),
        yaxis=dict(title="Energy (kWh)", gridcolor="#2d3250"),
        xaxis=dict(gridcolor="#2d3250"),
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Comfort gauge + energy donut
col_g1, col_g2, col_g3 = st.columns(3)

with col_g1:
    st.markdown("#### 🎯 Comfort Score Gauge")
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=comfort,
        number={"suffix": "%", "font": {"color": "#ffffff", "size": 36}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#a0aec0"},
            "bar": {"color": "#48bb78"},
            "bgcolor": "#1a1f35",
            "steps": [
                {"range": [0, 50],  "color": "#2d1f1f"},
                {"range": [50, 75], "color": "#2d2a1f"},
                {"range": [75, 100],"color": "#1f2d23"},
            ],
            "threshold": {"line": {"color": "#48bb78", "width": 3}, "value": 80}
        }
    ))
    fig_gauge.update_layout(
        height=250, paper_bgcolor="#1a1f35",
        font=dict(color="#a0aec0"),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_g2:
    st.markdown("#### 🌡️ Temp Distribution")
    fig_hist = go.Figure(go.Histogram(
        x=sensors["temperature"],
        nbinsx=15,
        marker_color="#63b3ed",
        marker_line_color="#2d3250",
        marker_line_width=1
    ))
    fig_hist.add_vline(x=21, line_dash="dash", line_color="#48bb78",
                       annotation_text="Min 21°C", annotation_font_color="#48bb78")
    fig_hist.add_vline(x=24, line_dash="dash", line_color="#48bb78",
                       annotation_text="Max 24°C", annotation_font_color="#48bb78")
    fig_hist.update_layout(
        height=250, paper_bgcolor="#1a1f35", plot_bgcolor="#1a1f35",
        font=dict(color="#a0aec0"),
        yaxis=dict(gridcolor="#2d3250"),
        xaxis=dict(title="Temperature (°C)", gridcolor="#2d3250"),
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col_g3:
    st.markdown("#### 💡 Energy Breakdown")
    fig_pie = go.Figure(go.Pie(
        labels=["AI Optimized", "Baseline Overhead"],
        values=[latest_energy, max(0, baseline - latest_energy)],
        hole=0.6,
        marker_colors=["#48bb78", "#fc8181"],
        textfont=dict(color="#ffffff")
    ))
    fig_pie.update_layout(
        height=250, paper_bgcolor="#1a1f35",
        font=dict(color="#a0aec0"),
        legend=dict(bgcolor="#1a1f35"),
        margin=dict(l=0, r=0, t=10, b=0),
        annotations=[dict(text=f"{pct:.0f}%\nsaved", x=0.5, y=0.5,
                          font=dict(size=16, color="#48bb78"), showarrow=False)]
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# Decision log + Chat side by side
col_dec, col_chat = st.columns([1, 1])

with col_dec:
    st.markdown("#### 🤖 AI Decision Log")
    if not decisions.empty:
        for _, row in decisions.head(10).iterrows():
            with st.expander(f"[{row['timestamp'][11:19]}] {row['action']}"):
                st.markdown(f"**Action:** `{row['action']}`")
                st.markdown(f"**Reason:** {row['reason']}")
                e_b = row['energy_before']
                e_a = row['energy_after']
                delta = round(e_b - e_a, 3)
                color = "green" if delta > 0 else "red"
                st.markdown(f"**Energy:** `{e_b}` → `{e_a}` kWh "
                            f"<span style='color:{color}'>({'−' if delta>0 else '+'}{abs(delta)} kWh)</span>",
                            unsafe_allow_html=True)
    else:
        st.info("No decisions yet")

with col_chat:
    st.markdown("#### 💬 Ask Building AI")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    user_input = st.chat_input("Ask about energy, temperature, decisions...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        recent_decisions = ""
        if not decisions.empty:
            for _, d in decisions.head(5).iterrows():
                recent_decisions += f"\n- {d['timestamp'][11:19]}: {d['action']} | {d['reason'][:80]}"

        context = f"""You are an AI assistant for Honeywell Smart Building Management System.

Current Building State:
- Temperature: {latest_temp:.1f}°C (range: {temp_min:.1f}°C - {temp_max:.1f}°C)
- Comfort Score: {comfort:.1f}% (ASHRAE 55 standard, target 21-24°C)
- Energy Used: {latest_energy:.3f} kWh (real EnergyPlus data)
- Baseline Energy: {baseline:.2f} kWh
- Energy Saved: {saved:.2f} kWh ({pct:.1f}% reduction)
- AI Decisions Made: {total_decisions}

Recent AI Decisions:{recent_decisions}

Answer concisely based on this real simulation data. If asked about building topics, answer specifically."""

        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": user_input}
            ],
            max_tokens=500, temperature=0.7
        )

        reply = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

st.divider()
st.caption(f"🏢 Honeywell Smart Building AI | EnergyPlus 23.2 | Groq Llama 3.3-70B | ASHRAE 55 | SQLite Audit Trail")