# # app.py
# import streamlit as st
# import plotly.graph_objects as go
# import pandas as pd
# import sqlite3
# import subprocess
# import os
# from groq import Groq
# from config import GROQ_API_KEY, GROQ_MODEL

# st.set_page_config(
#     page_title="Honeywell Smart Building AI",
#     page_icon="🏢",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# st.markdown("""
# <style>
#     .main { background-color: #0e1117; }
#     .stMetric {
#         background: linear-gradient(135deg, #1e2130, #252840);
#         border: 1px solid #2d3250;
#         border-radius: 12px;
#         padding: 16px;
#     }
#     .header-banner {
#         background: linear-gradient(135deg, #1a1f35 0%, #0d1117 50%, #1a2535 100%);
#         border: 1px solid #2d3250;
#         border-radius: 16px;
#         padding: 24px 32px;
#         margin-bottom: 24px;
#     }
#     .status-badge {
#         display: inline-block;
#         padding: 4px 12px;
#         border-radius: 20px;
#         font-size: 12px;
#         font-weight: 600;
#         margin-right: 8px;
#     }
#     .badge-green { background: #0d2818; color: #48bb78; border: 1px solid #276749; }
#     .badge-blue  { background: #0d1f2d; color: #63b3ed; border: 1px solid #2b6cb0; }
#     .badge-orange{ background: #2d1f0d; color: #ed8936; border: 1px solid #c05621; }
#     div[data-testid="stExpander"] {
#         background: #1a1f35;
#         border: 1px solid #2d3250;
#         border-radius: 10px;
#         margin-bottom: 8px;
#     }
# </style>
# """, unsafe_allow_html=True)

# st.markdown("""
# <div class="header-banner">
#     <h1 style="margin:0; color:#ffffff; font-size:28px;">🏢 Honeywell Smart Building AI</h1>
#     <p style="margin:6px 0 12px 0; color:#718096; font-size:14px;">
#         Autonomous HVAC Optimization • Real-time Control • Energy Intelligence
#     </p>
#     <span class="status-badge badge-green">● EnergyPlus 23.2 Physics</span>
#     <span class="status-badge badge-blue">● Llama 3.3-70B via Groq</span>
#     <span class="status-badge badge-orange">● MCP Tool Calling</span>
#     <span class="status-badge badge-green">● ASHRAE 55 Standard</span>
# </div>
# """, unsafe_allow_html=True)

# # Sidebar
# with st.sidebar:
#     st.markdown("### ⚙️ Control Panel")

#     run_btn = st.button("▶️ RUN SIMULATION", use_container_width=True, type="primary")
#     if run_btn:
#         if os.path.exists("building_data.db"):
#             os.remove("building_data.db")
#         with st.spinner("Running EnergyPlus + LLM..."):
#             subprocess.run(["python", "submission_runner.py"], capture_output=False, timeout=300)
#         st.success("✅ Simulation complete!")
#         st.rerun()

#     run_scenarios_btn = st.button("🎭 RUN ALL SCENARIOS", use_container_width=True)
#     if run_scenarios_btn:
#         with st.spinner("Running 3 scenarios (Normal, Heatwave, Winter)..."):
#             subprocess.run(["python", "scenario_runner.py"], capture_output=False, timeout=300)
#         st.success("✅ All scenarios done!")
#         st.rerun()

#     st.divider()
#     st.markdown("""
# **🔧 Tech Stack**
# - 🏗️ EnergyPlus 23.2 physics engine
# - 🤖 Llama 3.3-70B via Groq API
# - 🔧 MCP tool calling pattern
# - 📊 ASHRAE 55 comfort standard
# - 🗄️ SQLite real-time audit trail
#     """)

# # Load EnergyPlus data
# def load_data():
#     try:
#         conn = sqlite3.connect("building_data.db")
#         sensors   = pd.read_sql_query("SELECT * FROM sensor_readings ORDER BY id", conn)
#         decisions = pd.read_sql_query("SELECT * FROM ai_decisions ORDER BY id DESC LIMIT 30", conn)
#         energy    = pd.read_sql_query("SELECT * FROM energy_log ORDER BY id", conn)
#         conn.close()
#         return sensors, decisions, energy
#     except:
#         return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# # Load scenario data
# def load_scenario(name):
#     try:
#         conn = sqlite3.connect("building_data.db")
#         df = pd.read_sql_query(f"SELECT * FROM scenario_{name} ORDER BY id", conn)
#         conn.close()
#         return df
#     except:
#         return pd.DataFrame()

# sensors, decisions, energy = load_data()

# # ================================================================
# # TABS
# # ================================================================
# tab1, tab2, tab3, tab4 = st.tabs([
#     "📊 EnergyPlus Real Simulation",
#     "☀️ Heatwave Scenario",
#     "❄️ Winter Scenario",
#     "🌤️ Normal Day Scenario"
# ])

# # ================================================================
# # TAB 1 — Real EnergyPlus
# # ================================================================
# with tab1:
#     if sensors.empty:
#         st.markdown("""
#         <div style="text-align:center; padding:80px; color:#718096;">
#             <div style="font-size:64px;">🏢</div>
#             <h2 style="color:#a0aec0;">No Simulation Data Yet</h2>
#             <p>Click <b>RUN SIMULATION</b> in the sidebar to start</p>
#         </div>
#         """, unsafe_allow_html=True)
#     else:
#         latest_temp     = sensors["temperature"].iloc[-1]
#         total_decisions = len(decisions)
#         latest_energy   = energy["total_energy"].iloc[-1]
#         baseline        = energy["baseline_energy"].iloc[-1]
#         saved           = baseline - latest_energy
#         pct             = (saved / baseline * 100) if baseline > 0 else 0
#         comfort         = energy["comfort_score"].mean()
#         temp_min        = sensors["temperature"].min()
#         temp_max        = sensors["temperature"].max()

#         st.markdown("### 📊 Live Metrics")
#         c1, c2, c3, c4, c5, c6 = st.columns(6)
#         with c1:
#             icon = "✅" if 21 <= latest_temp <= 24 else "⚠️"
#             st.metric(f"{icon} Temperature", f"{latest_temp:.1f}°C",
#                       "Comfort OK" if 21 <= latest_temp <= 24 else "Adjusting")
#         with c2:
#             st.metric("🤖 AI Decisions", total_decisions, "Autonomous")
#         with c3:
#             st.metric("⚡ Energy Used", f"{latest_energy:.3f} kWh", "Real EnergyPlus")
#         with c4:
#             st.metric("💰 Energy Saved", f"{saved:.2f} kWh", f"{pct:.1f}% vs baseline")
#         with c5:
#             st.metric("😊 Avg Comfort", f"{comfort:.1f}%", "ASHRAE 55")
#         with c6:
#             carbon = saved * 0.233
#             st.metric("🌿 Carbon Avoided", f"{carbon:.2f} kg CO₂", "CEA Grid Factor")   

#         st.divider()

#         col_left, col_right = st.columns(2)
#         with col_left:
#             st.markdown("#### 🌡️ Temperature Over Time")
#             fig1 = go.Figure()
#             fig1.add_hrect(y0=21, y1=24, fillcolor="rgba(72,187,120,0.08)", line_width=0,
#                            annotation_text="✅ Comfort Zone", annotation_position="top left",
#                            annotation_font=dict(color="#48bb78", size=11))
#             fig1.add_trace(go.Scatter(x=sensors["timestamp"], y=sensors["temperature"],
#                 name="Zone Temp", line=dict(color="#ed8936", width=2.5),
#                 mode="lines", fill="tozeroy", fillcolor="rgba(237,137,54,0.07)"))
#             fig1.add_trace(go.Scatter(x=sensors["timestamp"], y=sensors["ac_setpoint"],
#                 name="Heating SP", line=dict(color="#fc8181", dash="dash", width=1.5), mode="lines"))
#             fig1.update_layout(height=320, paper_bgcolor="#1a1f35", plot_bgcolor="#1a1f35",
#                 font=dict(color="#a0aec0"), hovermode="x unified",
#                 legend=dict(bgcolor="#1a1f35"), yaxis=dict(title="Temperature (°C)", gridcolor="#2d3250"),
#                 xaxis=dict(gridcolor="#2d3250"), margin=dict(l=0,r=0,t=10,b=0))
#             st.plotly_chart(fig1, use_container_width=True)

#         with col_right:
#             st.markdown("#### ⚡ Energy: AI vs Baseline")
#             fig2 = go.Figure()
#             fig2.add_trace(go.Scatter(x=energy["timestamp"], y=energy["baseline_energy"],
#                 name="Baseline (No AI)", line=dict(color="#fc8181", dash="dash", width=2), mode="lines"))
#             fig2.add_trace(go.Scatter(x=energy["timestamp"], y=energy["total_energy"],
#                 name="With AI", line=dict(color="#48bb78", width=2.5),
#                 fill="tonexty", fillcolor="rgba(72,187,120,0.12)", mode="lines"))
#             fig2.update_layout(height=320, paper_bgcolor="#1a1f35", plot_bgcolor="#1a1f35",
#                 font=dict(color="#a0aec0"), hovermode="x unified",
#                 legend=dict(bgcolor="#1a1f35"), yaxis=dict(title="Energy (kWh)", gridcolor="#2d3250"),
#                 xaxis=dict(gridcolor="#2d3250"), margin=dict(l=0,r=0,t=10,b=0))
#             st.plotly_chart(fig2, use_container_width=True)

#         st.divider()

#         col_g1, col_g2, col_g3 = st.columns(3)
#         with col_g1:
#             st.markdown("#### 🎯 Comfort Score")
#             fig_gauge = go.Figure(go.Indicator(
#                 mode="gauge+number", value=comfort,
#                 number={"suffix": "%", "font": {"color": "#ffffff", "size": 36}},
#                 gauge={"axis": {"range": [0,100]}, "bar": {"color": "#48bb78"},
#                        "bgcolor": "#1a1f35",
#                        "steps": [{"range":[0,50],"color":"#2d1f1f"},
#                                   {"range":[50,75],"color":"#2d2a1f"},
#                                   {"range":[75,100],"color":"#1f2d23"}],
#                        "threshold": {"line": {"color":"#48bb78","width":3},"value":80}}))
#             fig_gauge.update_layout(height=250, paper_bgcolor="#1a1f35",
#                 font=dict(color="#a0aec0"), margin=dict(l=20,r=20,t=20,b=20))
#             st.plotly_chart(fig_gauge, use_container_width=True)

#         with col_g2:
#             st.markdown("#### 🌡️ Temp Distribution")
#             fig_hist = go.Figure(go.Histogram(x=sensors["temperature"], nbinsx=15,
#                 marker_color="#63b3ed", marker_line_color="#2d3250", marker_line_width=1))
#             fig_hist.add_vline(x=21, line_dash="dash", line_color="#48bb78",
#                 annotation_text="Min 21°C", annotation_font_color="#48bb78")
#             fig_hist.add_vline(x=24, line_dash="dash", line_color="#48bb78",
#                 annotation_text="Max 24°C", annotation_font_color="#48bb78")
#             fig_hist.update_layout(height=250, paper_bgcolor="#1a1f35", plot_bgcolor="#1a1f35",
#                 font=dict(color="#a0aec0"), yaxis=dict(gridcolor="#2d3250"),
#                 xaxis=dict(title="Temperature (°C)", gridcolor="#2d3250"),
#                 margin=dict(l=0,r=0,t=10,b=0))
#             st.plotly_chart(fig_hist, use_container_width=True)

#         with col_g3:
#             st.markdown("#### 💡 Energy Breakdown")
#             fig_pie = go.Figure(go.Pie(
#                 labels=["AI Optimized", "Baseline Overhead"],
#                 values=[latest_energy, max(0, baseline - latest_energy)],
#                 hole=0.6, marker_colors=["#48bb78","#fc8181"],
#                 textfont=dict(color="#ffffff")))
#             fig_pie.update_layout(height=250, paper_bgcolor="#1a1f35",
#                 font=dict(color="#a0aec0"), legend=dict(bgcolor="#1a1f35"),
#                 margin=dict(l=0,r=0,t=10,b=0),
#                 annotations=[dict(text=f"{pct:.0f}%\nsaved", x=0.5, y=0.5,
#                     font=dict(size=16, color="#48bb78"), showarrow=False)])
#             st.plotly_chart(fig_pie, use_container_width=True)

#         st.divider()

#         col_dec, col_chat = st.columns([1, 1])
#         with col_dec:
#             st.markdown("#### 🤖 AI Decision Log")
#             if not decisions.empty:
#                 for _, row in decisions.head(10).iterrows():
#                     with st.expander(f"[{row['timestamp'][11:19]}] {row['action']}"):
#                         st.markdown(f"**Action:** `{row['action']}`")
#                         st.markdown(f"**Reason:** {row['reason']}")
#                         e_b = row['energy_before']
#                         e_a = row['energy_after']
#                         delta = round(e_b - e_a, 3)
#                         color = "green" if delta > 0 else "red"
#                         st.markdown(f"**Energy:** `{e_b}` → `{e_a}` kWh "
#                             f"<span style='color:{color}'>({'−' if delta>0 else '+'}{abs(delta)} kWh)</span>",
#                             unsafe_allow_html=True)
#             else:
#                 st.info("No decisions yet")

#         with col_chat:
#             st.markdown("#### 💬 Ask Building AI")
#             if "chat_history" not in st.session_state:
#                 st.session_state.chat_history = []
#             for message in st.session_state.chat_history:
#                 with st.chat_message(message["role"]):
#                     st.write(message["content"])

#             user_input = st.chat_input("Ask about energy, temperature, decisions...")
#             if user_input:
#                 st.session_state.chat_history.append({"role": "user", "content": user_input})
#                 recent_decisions = ""
#                 if not decisions.empty:
#                     for _, d in decisions.head(5).iterrows():
#                         recent_decisions += f"\n- {d['timestamp'][11:19]}: {d['action']} | {d['reason'][:80]}"

#                 context = f"""You are an AI assistant for Honeywell Smart Building Management System.
# Current Building State:
# - Temperature: {latest_temp:.1f}°C (range: {temp_min:.1f}°C - {temp_max:.1f}°C)
# - Comfort Score: {comfort:.1f}% (ASHRAE 55, target 21-24°C)
# - Energy Used: {latest_energy:.3f} kWh (real EnergyPlus)
# - Baseline: {baseline:.2f} kWh | Saved: {saved:.2f} kWh ({pct:.1f}%)
# - AI Decisions: {total_decisions}
# Recent Decisions:{recent_decisions}
# Answer concisely based on real simulation data."""

#                 client = Groq(api_key=GROQ_API_KEY)
#                 response = client.chat.completions.create(
#                     model=GROQ_MODEL,
#                     messages=[{"role": "system", "content": context},
#                                {"role": "user", "content": user_input}],
#                     max_tokens=500, temperature=0.7)
#                 reply = response.choices[0].message.content
#                 st.session_state.chat_history.append({"role": "assistant", "content": reply})
#                 st.rerun()

# # ================================================================
# # SCENARIO TAB HELPER
# # ================================================================
# def render_scenario_tab(scenario_name, icon, color, baseline_kwh):
#     df = load_scenario(scenario_name)
#     if df.empty:
#         st.markdown(f"""
#         <div style="text-align:center; padding:60px; color:#718096;">
#             <div style="font-size:48px;">{icon}</div>
#             <h3 style="color:#a0aec0;">No {scenario_name.title()} Data</h3>
#             <p>Click <b>🎭 RUN ALL SCENARIOS</b> in the sidebar</p>
#         </div>
#         """, unsafe_allow_html=True)
#         return

#     avg_temp    = df["temperature"].mean()
#     avg_comfort = df["comfort_score"].mean()
#     total_energy = df["energy"].sum()
#     total_baseline = df["baseline_energy"].sum()
#     total_saved = total_baseline - total_energy
#     pct_saved   = (total_saved / total_baseline * 100) if total_baseline > 0 else 0

#     # Metrics
#     c1, c2, c3, c4 = st.columns(4)
#     with c1:
#         st.metric(f"{icon} Avg Temp", f"{avg_temp:.1f}°C")
#     with c2:
#         st.metric("⚡ Total Energy", f"{total_energy:.2f} kWh")
#     with c3:
#         st.metric("💰 Energy Saved", f"{total_saved:.2f} kWh", f"{pct_saved:.1f}%")
#     with c4:
#         st.metric("😊 Avg Comfort", f"{avg_comfort:.1f}%")

#     st.divider()

#     col_l, col_r = st.columns(2)
#     with col_l:
#         st.markdown("#### 🌡️ Temperature Over 24 Hours")
#         fig = go.Figure()
#         fig.add_hrect(y0=21, y1=24, fillcolor="rgba(72,187,120,0.08)", line_width=0,
#                       annotation_text="Comfort Zone", annotation_font=dict(color="#48bb78"))
#         fig.add_trace(go.Scatter(x=df["timestamp"], y=df["temperature"],
#             name="Temperature", line=dict(color=color, width=2.5),
#             fill="tozeroy", fillcolor=f"rgba{tuple(list(bytes.fromhex(color[1:])) + [25])}",
#             mode="lines"))
#         fig.add_trace(go.Scatter(x=df["timestamp"], y=df["heating_sp"],
#             name="Heating SP", line=dict(color="#fc8181", dash="dash"), mode="lines"))
#         fig.add_trace(go.Scatter(x=df["timestamp"], y=df["cooling_sp"],
#             name="Cooling SP", line=dict(color="#63b3ed", dash="dash"), mode="lines"))
#         fig.update_layout(height=300, paper_bgcolor="#1a1f35", plot_bgcolor="#1a1f35",
#             font=dict(color="#a0aec0"), hovermode="x unified",
#             legend=dict(bgcolor="#1a1f35"), yaxis=dict(gridcolor="#2d3250"),
#             xaxis=dict(gridcolor="#2d3250"), margin=dict(l=0,r=0,t=10,b=0))
#         st.plotly_chart(fig, use_container_width=True)

#     with col_r:
#         st.markdown("#### ⚡ Energy: AI vs Baseline")
#         fig2 = go.Figure()
#         fig2.add_trace(go.Scatter(x=df["timestamp"], y=df["baseline_energy"],
#             name="Baseline", line=dict(color="#fc8181", dash="dash", width=2), mode="lines"))
#         fig2.add_trace(go.Scatter(x=df["timestamp"], y=df["energy"],
#             name="With AI", line=dict(color="#48bb78", width=2.5),
#             fill="tonexty", fillcolor="rgba(72,187,120,0.12)", mode="lines"))
#         fig2.update_layout(height=300, paper_bgcolor="#1a1f35", plot_bgcolor="#1a1f35",
#             font=dict(color="#a0aec0"), hovermode="x unified",
#             legend=dict(bgcolor="#1a1f35"), yaxis=dict(gridcolor="#2d3250"),
#             xaxis=dict(gridcolor="#2d3250"), margin=dict(l=0,r=0,t=10,b=0))
#         st.plotly_chart(fig2, use_container_width=True)

#     st.divider()
#     st.markdown("#### 🤖 AI Decisions")
#     for _, row in df[df["decision"] != "Maintaining setpoints"].iterrows():
#         with st.expander(f"[Hour {row['timestamp'][11:13]}:00] {row['decision']}"):
#             st.write(f"**Reasoning:** {row['reasoning']}")
#             st.write(f"**Temp:** {row['temperature']}°C | **Energy:** {row['energy']} kWh")

# # ================================================================
# # TAB 2 — Heatwave
# # ================================================================
# with tab2:
#     st.markdown("### ☀️ Heatwave Scenario — Outdoor: 42°C")
#     st.caption("AI managing extreme heat — cooling priority, energy vs comfort tradeoff")
#     render_scenario_tab("heatwave", "☀️", "#fc8181", 18.0)

# # ================================================================
# # TAB 3 — Winter
# # ================================================================
# with tab3:
#     st.markdown("### ❄️ Winter Scenario — Outdoor: -5°C")
#     st.caption("AI managing cold weather — heating efficiency, preventing overcooling")
#     render_scenario_tab("winter", "❄️", "#63b3ed", 15.0)

# # ================================================================
# # TAB 4 — Normal
# # ================================================================
# with tab4:
#     st.markdown("### 🌤️ Normal Day Scenario — Outdoor: 22°C")
#     st.caption("AI in standard conditions — balanced comfort and energy optimization")
#     render_scenario_tab("normal", "🌤️", "#48bb78", 8.0)

# st.divider()
# st.caption("🏢 Honeywell Smart Building AI | EnergyPlus 23.2 | Groq Llama 3.3-70B | ASHRAE 55 | SQLite Audit Trail")

# app.py
import streamlit as st
import plotly.graph_objects as go
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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.main .block-container { padding: 2rem 2.5rem; max-width: 1400px; }

section[data-testid="stSidebar"] {
    background: #0a0e1a;
    border-right: 1px solid #1e2438;
}

.header-card {
    background: linear-gradient(135deg, #0d1117 0%, #1a1f35 50%, #0d1117 100%);
    border: 1px solid #1e2438;
    border-radius: 20px;
    padding: 28px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.header-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #667eea, #48bb78, #ed8936, #667eea);
}
.header-title {
    font-size: 26px; font-weight: 700;
    color: #f7fafc; margin: 0 0 6px 0; letter-spacing: -0.5px;
}
.header-sub {
    font-size: 13px; color: #718096; margin: 0 0 16px 0;
}
.badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 5px 14px; border-radius: 100px;
    font-size: 11px; font-weight: 600; margin-right: 8px;
    letter-spacing: 0.3px;
}
.badge-green { background: rgba(72,187,120,0.12); color: #68d391; border: 1px solid rgba(72,187,120,0.25); }
.badge-blue  { background: rgba(99,179,237,0.12); color: #76e4f7; border: 1px solid rgba(99,179,237,0.25); }
.badge-purple{ background: rgba(159,122,234,0.12); color: #b794f4; border: 1px solid rgba(159,122,234,0.25); }
.badge-orange{ background: rgba(237,137,54,0.12);  color: #f6ad55; border: 1px solid rgba(237,137,54,0.25); }

.metric-card {
    background: #0d1117;
    border: 1px solid #1e2438;
    border-radius: 16px;
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.metric-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0; height: 3px;
    border-radius: 0 0 16px 16px;
}
.metric-card.green::after  { background: linear-gradient(90deg, #48bb78, #68d391); }
.metric-card.blue::after   { background: linear-gradient(90deg, #4299e1, #76e4f7); }
.metric-card.purple::after { background: linear-gradient(90deg, #9f7aea, #b794f4); }
.metric-card.orange::after { background: linear-gradient(90deg, #ed8936, #f6ad55); }
.metric-card.teal::after   { background: linear-gradient(90deg, #38b2ac, #4fd1c5); }
.metric-card.red::after    { background: linear-gradient(90deg, #fc8181, #feb2b2); }

.metric-label { font-size: 11px; font-weight: 600; color: #4a5568; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
.metric-value { font-size: 28px; font-weight: 700; color: #f7fafc; letter-spacing: -1px; margin-bottom: 6px; }
.metric-delta { font-size: 12px; font-weight: 500; color: #48bb78; }
.metric-delta.warn { color: #f6ad55; }

.section-title {
    font-size: 14px; font-weight: 600; color: #a0aec0;
    text-transform: uppercase; letter-spacing: 1.5px;
    margin: 0 0 16px 0; padding-bottom: 10px;
    border-bottom: 1px solid #1e2438;
}

.empty-state {
    text-align: center; padding: 80px 20px;
    background: #0d1117; border: 1px dashed #2d3748;
    border-radius: 16px;
}

div[data-testid="stExpander"] {
    background: #0d1117 !important;
    border: 1px solid #1e2438 !important;
    border-radius: 12px !important;
    margin-bottom: 6px !important;
}
div[data-testid="stExpander"]:hover {
    border-color: #2d3748 !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: #0d1117;
    border-bottom: 1px solid #1e2438;
    gap: 4px; padding: 0 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #718096;
    border-radius: 8px 8px 0 0;
    font-size: 13px; font-weight: 500;
    padding: 10px 20px;
}
.stTabs [aria-selected="true"] {
    background: #1a1f35 !important;
    color: #f7fafc !important;
    border-bottom: 2px solid #667eea !important;
}

.stChatMessage { background: #0d1117 !important; border: 1px solid #1e2438 !important; border-radius: 12px !important; }

[data-testid="stMetric"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────
st.markdown("""
<div class="header-card">
  <p class="header-title">🏢 Honeywell Smart Building AI</p>
  <p class="header-sub">Autonomous HVAC Optimization · Real-time Closed Loop Control · Energy Intelligence</p>
  <span class="badge badge-green">● EnergyPlus 23.2</span>
  <span class="badge badge-blue">● Llama 3.3-70B</span>
  <span class="badge badge-purple">● MCP Tool Calling</span>
  <span class="badge badge-orange">● ASHRAE 55</span>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<p style='color:#a0aec0;font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:16px;'>Control Panel</p>", unsafe_allow_html=True)

    run_btn = st.button("▶ Run EnergyPlus Simulation", use_container_width=True, type="primary")
    if run_btn:
        if os.path.exists("building_data.db"):
            os.remove("building_data.db")
        with st.spinner("Running EnergyPlus + LLM..."):
            subprocess.run(["python", "submission_runner.py"], capture_output=False, timeout=300)
        st.success("✅ Done!")
        st.rerun()

    st.markdown("<div style='margin:8px 0'></div>", unsafe_allow_html=True)

    run_sc = st.button("🎭 Run All Scenarios", use_container_width=True)
    if run_sc:
        with st.spinner("Running 3 scenarios..."):
            subprocess.run(["python", "scenario_runner.py"], capture_output=False, timeout=300)
        st.success("✅ Scenarios done!")
        st.rerun()

    st.markdown("""
    <div style='margin-top:24px; padding:16px; background:#0d1117; border:1px solid #1e2438; border-radius:12px;'>
        <p style='font-size:11px;font-weight:600;color:#4a5568;text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;'>Tech Stack</p>
        <p style='font-size:12px;color:#718096;line-height:1.8;margin:0;'>
        🏗 EnergyPlus 23.2 Physics<br>
        🤖 Llama 3.3-70B via Groq<br>
        🔧 MCP Tool Calling Pattern<br>
        📊 ASHRAE 55 Comfort Standard<br>
        🗄 SQLite Real-time Audit Trail
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── Data Loading ──────────────────────────────────────────────────────
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

def load_scenario(name):
    try:
        conn = sqlite3.connect("building_data.db")
        df = pd.read_sql_query(f"SELECT * FROM scenario_{name} ORDER BY id", conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

def make_chart(layout_overrides={}):
    base = dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#718096", size=11),
        hovermode="x unified",
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#1e2438",
                    borderwidth=1, font=dict(size=11)),
        xaxis=dict(gridcolor="#1e2438", showgrid=True, zeroline=False,
                   tickfont=dict(size=10, color="#4a5568")),
        yaxis=dict(gridcolor="#1e2438", showgrid=True, zeroline=False,
                   tickfont=dict(size=10, color="#4a5568")),
        margin=dict(l=8, r=8, t=16, b=8),
    )
    base.update(layout_overrides)
    return base

def metric_card(label, value, delta, color="green", delta_warn=False):
    warn_class = "warn" if delta_warn else ""
    return f"""
    <div class="metric-card {color}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-delta {warn_class}">{delta}</div>
    </div>"""

sensors, decisions, energy = load_data()

# ── Tabs ──────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊  Real Simulation",
    "☀️  Heatwave",
    "❄️  Winter",
    "🌤️  Normal Day"
])

# ══════════════════════════════════════════════════════════════
# TAB 1
# ══════════════════════════════════════════════════════════════
with tab1:
    if sensors.empty:
        st.markdown("""
        <div class="empty-state">
            <div style="font-size:52px;margin-bottom:16px;">🏢</div>
            <p style="font-size:18px;font-weight:600;color:#a0aec0;margin-bottom:8px;">No Simulation Data</p>
            <p style="color:#4a5568;font-size:14px;">Click <b style="color:#667eea">▶ Run EnergyPlus Simulation</b> in the sidebar</p>
        </div>""", unsafe_allow_html=True)
    else:
        lt = sensors["temperature"].iloc[-1]
        nd = len(decisions)
        le = energy["total_energy"].iloc[-1]
        bl = energy["baseline_energy"].iloc[-1]
        sv = bl - le
        pt = (sv / bl * 100) if bl > 0 else 0
        cf = energy["comfort_score"].mean()
        co = sv * 0.233

        # Metrics
        st.markdown("<p class='section-title'>Live Metrics</p>", unsafe_allow_html=True)
        c1,c2,c3,c4,c5,c6 = st.columns(6)
        temp_ok = 21 <= lt <= 24
        with c1: st.markdown(metric_card("Temperature", f"{lt:.1f}°C",
            "✓ Comfort OK" if temp_ok else "⚠ Adjusting", "green" if temp_ok else "orange",
            not temp_ok), unsafe_allow_html=True)
        with c2: st.markdown(metric_card("AI Decisions", str(nd), "Autonomous Control", "blue"), unsafe_allow_html=True)
        with c3: st.markdown(metric_card("Energy Used", f"{le:.3f} kWh", "Real EnergyPlus Meter", "purple"), unsafe_allow_html=True)
        with c4: st.markdown(metric_card("Energy Saved", f"{sv:.2f} kWh", f"↓ {pt:.1f}% vs Baseline", "green"), unsafe_allow_html=True)
        with c5: st.markdown(metric_card("Avg Comfort", f"{cf:.1f}%", "ASHRAE 55 Standard", "teal"), unsafe_allow_html=True)
        with c6: st.markdown(metric_card("Carbon Avoided", f"{co:.2f} kg", "CO₂ · CEA Grid Factor", "green"), unsafe_allow_html=True)

        st.markdown("<div style='margin:28px 0 20px'><p class='section-title'>Performance Charts</p></div>", unsafe_allow_html=True)

        col_l, col_r = st.columns(2, gap="medium")
        with col_l:
            st.markdown("<p style='font-size:13px;font-weight:600;color:#a0aec0;margin-bottom:8px;'>🌡 Zone Temperature</p>", unsafe_allow_html=True)
            fig1 = go.Figure()
            fig1.add_hrect(y0=21, y1=24, fillcolor="rgba(72,187,120,0.06)", line_width=0,
                annotation_text="Comfort Zone  21–24°C", annotation_position="top left",
                annotation_font=dict(color="#48bb78", size=10))
            fig1.add_trace(go.Scatter(x=sensors["timestamp"], y=sensors["temperature"],
                name="Zone Temp", line=dict(color="#ed8936", width=2),
                fill="tozeroy", fillcolor="rgba(237,137,54,0.05)", mode="lines"))
            fig1.add_trace(go.Scatter(x=sensors["timestamp"], y=sensors["ac_setpoint"],
                name="Heating SP", line=dict(color="#fc8181", dash="dot", width=1.5), mode="lines"))
            fig1.update_layout(height=280, **make_chart({"yaxis": {"title": "°C", "gridcolor": "#1e2438"}}))
            st.plotly_chart(fig1, use_container_width=True)

        with col_r:
            st.markdown("<p style='font-size:13px;font-weight:600;color:#a0aec0;margin-bottom:8px;'>⚡ Energy: AI vs Baseline</p>", unsafe_allow_html=True)
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=energy["timestamp"], y=energy["baseline_energy"],
                name="Baseline", line=dict(color="#fc8181", dash="dot", width=1.5), mode="lines"))
            fig2.add_trace(go.Scatter(x=energy["timestamp"], y=energy["total_energy"],
                name="With AI", line=dict(color="#48bb78", width=2),
                fill="tonexty", fillcolor="rgba(72,187,120,0.08)", mode="lines"))
            fig2.update_layout(height=280, **make_chart({"yaxis": {"title": "kWh", "gridcolor": "#1e2438"}}))
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("<div style='margin:8px 0 20px'><p class='section-title'>Analytics</p></div>", unsafe_allow_html=True)

        cg1, cg2, cg3 = st.columns(3, gap="medium")
        with cg1:
            st.markdown("<p style='font-size:13px;font-weight:600;color:#a0aec0;margin-bottom:8px;'>🎯 Comfort Score</p>", unsafe_allow_html=True)
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number", value=cf,
                number={"suffix": "%", "font": {"color": "#f7fafc", "size": 32}},
                gauge={"axis": {"range": [0,100], "tickcolor": "#4a5568"},
                       "bar": {"color": "#48bb78", "thickness": 0.25},
                       "bgcolor": "rgba(0,0,0,0)",
                       "borderwidth": 0,
                       "steps": [{"range":[0,50],"color":"rgba(252,129,129,0.1)"},
                                  {"range":[50,75],"color":"rgba(246,173,85,0.1)"},
                                  {"range":[75,100],"color":"rgba(72,187,120,0.1)"}],
                       "threshold": {"line":{"color":"#48bb78","width":2},"value":80}}))
            fig_g.update_layout(height=220, paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#718096"), margin=dict(l=16,r=16,t=16,b=16))
            st.plotly_chart(fig_g, use_container_width=True)

        with cg2:
            st.markdown("<p style='font-size:13px;font-weight:600;color:#a0aec0;margin-bottom:8px;'>🌡 Temp Distribution</p>", unsafe_allow_html=True)
            fig_h = go.Figure(go.Histogram(x=sensors["temperature"], nbinsx=12,
                marker_color="rgba(99,179,237,0.7)", marker_line_color="#1e2438", marker_line_width=1))
            fig_h.add_vline(x=21, line_dash="dot", line_color="#48bb78", line_width=1.5)
            fig_h.add_vline(x=24, line_dash="dot", line_color="#48bb78", line_width=1.5)
            fig_h.update_layout(height=220, **make_chart({"xaxis":{"title":"°C","gridcolor":"#1e2438"}}))
            st.plotly_chart(fig_h, use_container_width=True)

        with cg3:
            st.markdown("<p style='font-size:13px;font-weight:600;color:#a0aec0;margin-bottom:8px;'>💡 Energy Split</p>", unsafe_allow_html=True)
            fig_p = go.Figure(go.Pie(
                labels=["AI Optimized", "Baseline Overhead"],
                values=[le, max(0, bl-le)], hole=0.65,
                marker_colors=["#48bb78","rgba(252,129,129,0.6)"],
                textfont=dict(size=11, color="#a0aec0"),
                hovertemplate="%{label}: %{value:.3f} kWh<extra></extra>"))
            fig_p.update_layout(height=220, paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#718096"), legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
                margin=dict(l=0,r=0,t=0,b=0),
                annotations=[dict(text=f"<b>{pt:.0f}%</b><br>saved",
                    x=0.5, y=0.5, font=dict(size=14, color="#48bb78"), showarrow=False)])
            st.plotly_chart(fig_p, use_container_width=True)

        st.markdown("<div style='margin:8px 0 20px'><p class='section-title'>AI Decisions & Assistant</p></div>", unsafe_allow_html=True)

        cd, cc = st.columns([1,1], gap="medium")
        with cd:
            st.markdown("<p style='font-size:13px;font-weight:600;color:#a0aec0;margin-bottom:12px;'>🤖 Decision Log</p>", unsafe_allow_html=True)
            if not decisions.empty:
                for _, row in decisions.head(8).iterrows():
                    with st.expander(f"{row['timestamp'][11:19]}  ·  {row['action']}"):
                        st.markdown(f"<p style='color:#a0aec0;font-size:13px;'>{row['reason']}</p>", unsafe_allow_html=True)
                        eb, ea = row['energy_before'], row['energy_after']
                        d = round(eb-ea, 3)
                        col = "#48bb78" if d > 0 else "#fc8181"
                        st.markdown(f"<p style='font-size:12px;color:#718096;'>Energy: <code>{eb}</code> → <code>{ea}</code> kWh &nbsp;<span style='color:{col}'>({'−' if d>0 else '+'}{abs(d)} kWh)</span></p>", unsafe_allow_html=True)
            else:
                st.info("No decisions yet")

        with cc:
            st.markdown("<p style='font-size:13px;font-weight:600;color:#a0aec0;margin-bottom:12px;'>💬 Building AI Assistant</p>", unsafe_allow_html=True)
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            for m in st.session_state.chat_history:
                with st.chat_message(m["role"]):
                    st.write(m["content"])

            user_input = st.chat_input("Ask about energy, comfort, decisions...")
            if user_input:
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                rd = ""
                if not decisions.empty:
                    for _, d in decisions.head(5).iterrows():
                        rd += f"\n- {d['timestamp'][11:19]}: {d['action']} | {d['reason'][:80]}"
                ctx = f"""You are an AI assistant for Honeywell Smart Building.
State: Temp={lt:.1f}°C, Comfort={cf:.1f}%, Energy={le:.3f}kWh, Baseline={bl:.2f}kWh, Saved={sv:.2f}kWh ({pt:.1f}%), Carbon Avoided={co:.2f}kg CO2, Decisions={nd}
Recent:{rd}
Answer concisely from real data."""
                client = Groq(api_key=GROQ_API_KEY)
                resp = client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=[{"role":"system","content":ctx},{"role":"user","content":user_input}],
                    max_tokens=400, temperature=0.7)
                reply = resp.choices[0].message.content
                st.session_state.chat_history.append({"role":"assistant","content":reply})
                st.rerun()

# ══════════════════════════════════════════════════════════════
# SCENARIO TAB RENDERER
# ══════════════════════════════════════════════════════════════
def render_scenario(scenario_name, icon, line_color, outdoor_temp, description):
    df = load_scenario(scenario_name)

    st.markdown(f"""
    <div style='background:#0d1117;border:1px solid #1e2438;border-radius:14px;padding:18px 22px;margin-bottom:20px;'>
        <p style='margin:0;font-size:16px;font-weight:600;color:#f7fafc;'>{icon} {scenario_name.title()} Scenario</p>
        <p style='margin:4px 0 0;font-size:13px;color:#718096;'>Outdoor: {outdoor_temp}°C · {description}</p>
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.markdown("""
        <div class="empty-state">
            <p style="font-size:16px;font-weight:600;color:#a0aec0;">No scenario data yet</p>
            <p style="color:#4a5568;font-size:13px;">Click <b style="color:#667eea">🎭 Run All Scenarios</b> in the sidebar</p>
        </div>""", unsafe_allow_html=True)
        return

    avg_t = df["temperature"].mean()
    tot_e = df["energy"].sum()
    tot_b = df["baseline_energy"].sum()
    tot_s = tot_b - tot_e
    pct_s = (tot_s / tot_b * 100) if tot_b > 0 else 0
    avg_c = df["comfort_score"].mean()
    carbon = tot_s * 0.233

    st.markdown("<p class='section-title'>Scenario Metrics</p>", unsafe_allow_html=True)
    mc1,mc2,mc3,mc4,mc5 = st.columns(5)
    with mc1: st.markdown(metric_card("Avg Temperature", f"{avg_t:.1f}°C", f"Outdoor: {outdoor_temp}°C", "orange"), unsafe_allow_html=True)
    with mc2: st.markdown(metric_card("Total Energy", f"{tot_e:.2f} kWh", "AI Optimized", "purple"), unsafe_allow_html=True)
    with mc3: st.markdown(metric_card("Energy Saved", f"{tot_s:.2f} kWh", f"↓ {pct_s:.1f}% vs Baseline", "green"), unsafe_allow_html=True)
    with mc4: st.markdown(metric_card("Avg Comfort", f"{avg_c:.1f}%", "ASHRAE 55", "teal"), unsafe_allow_html=True)
    with mc5: st.markdown(metric_card("Carbon Avoided", f"{carbon:.2f} kg", "CO₂ Avoided", "green"), unsafe_allow_html=True)

    st.markdown("<div style='margin:20px 0 16px'></div>", unsafe_allow_html=True)

    sl, sr = st.columns(2, gap="medium")
    with sl:
        st.markdown("<p style='font-size:13px;font-weight:600;color:#a0aec0;margin-bottom:8px;'>🌡 Temperature Over 24 Hours</p>", unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_hrect(y0=21, y1=24, fillcolor="rgba(72,187,120,0.06)", line_width=0,
            annotation_text="Comfort Zone", annotation_font=dict(color="#48bb78", size=10))
        fig.add_trace(go.Scatter(x=df["timestamp"], y=df["temperature"],
            name="Temperature", line=dict(color=line_color, width=2),
            fill="tozeroy", fillcolor=f"rgba{(*bytes.fromhex(line_color[1:]),)}".replace(")", ",0.06)"),
            mode="lines"))
        fig.add_trace(go.Scatter(x=df["timestamp"], y=df["heating_sp"],
            name="Heating SP", line=dict(color="#fc8181", dash="dot", width=1.5), mode="lines"))
        fig.add_trace(go.Scatter(x=df["timestamp"], y=df["cooling_sp"],
            name="Cooling SP", line=dict(color="#63b3ed", dash="dot", width=1.5), mode="lines"))
        fig.update_layout(height=280, **make_chart())
        st.plotly_chart(fig, use_container_width=True)

    with sr:
        st.markdown("<p style='font-size:13px;font-weight:600;color:#a0aec0;margin-bottom:8px;'>⚡ Energy: AI vs Baseline</p>", unsafe_allow_html=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=df["timestamp"], y=df["baseline_energy"],
            name="Baseline", line=dict(color="#fc8181", dash="dot", width=1.5), mode="lines"))
        fig2.add_trace(go.Scatter(x=df["timestamp"], y=df["energy"],
            name="With AI", line=dict(color="#48bb78", width=2),
            fill="tonexty", fillcolor="rgba(72,187,120,0.08)", mode="lines"))
        fig2.update_layout(height=280, **make_chart())
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div style='margin:8px 0 16px'><p class='section-title'>AI Decisions This Scenario</p></div>", unsafe_allow_html=True)
    for _, row in df[df["reasoning"] != "Maintaining setpoints"].iterrows():
        with st.expander(f"Hour {row['timestamp'][11:13]}:00  ·  {row['decision']}"):
            st.markdown(f"<p style='color:#a0aec0;font-size:13px;'>{row['reasoning']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:12px;color:#718096;'>Temp: <code>{row['temperature']}°C</code> · Energy: <code>{row['energy']} kWh</code></p>", unsafe_allow_html=True)

with tab2: render_scenario("heatwave", "☀️", "#fc8181", 42, "Extreme heat — cooling priority")
with tab3: render_scenario("winter",   "❄️", "#63b3ed", -5, "Cold winter — heating efficiency")
with tab4: render_scenario("normal",   "🌤️", "#48bb78", 22, "Mild day — balanced optimization")

st.markdown("<div style='margin:32px 0 8px;text-align:center;'><p style='font-size:11px;color:#2d3748;'>Honeywell Smart Building AI · EnergyPlus 23.2 · Groq Llama 3.3-70B · ASHRAE 55 · SQLite</p></div>", unsafe_allow_html=True)