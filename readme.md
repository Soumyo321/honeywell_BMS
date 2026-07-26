live link https://soumyo321-honeywell-bms-app1-snuezx.streamlit.app/

→ Open Live Dashboard

📋 Problem Statement

ID: 1 | Title: Eco-Loop Building Agents
Theme: Smart Cities & Urban Development | Category: Software
Student: Soumyodip Bhattacharya | ID: 20525115

Buildings consume 40% of global energy — mostly through HVAC systems running on fixed, dumb schedules with no real-time adaptation. Traditional Building Management Systems (BMS) either waste energy or sacrifice occupant comfort with no intelligent tradeoff.

🚀 What We Built

A fully autonomous BMS that:

Runs real EnergyPlus 23.2 building physics simulation
Reads live sensor data via Python API callbacks at every timestep
Sends data to Llama 3.3-70B (open-source LLM) via Groq API
LLM reasons about comfort vs energy vs carbon goals and calls MCP tools
New HVAC setpoints are written directly into EnergyPlus actuators in real-time
Every decision is logged to SQLite with full AI reasoning
Streamlit dashboard shows live metrics, charts, AI chat, and 3-scenario comparison
🏗 Architecture
┌─────────────────────────────────────────────────────────────┐
│                  Closed-Loop AI Control                      │
│                                                              │
│  EnergyPlus  ──sensor data──▶  MCP Bridge  ──tool call──▶  LLM  │
│      ▲                             │                         │
│      └────── actuator write ───────┘                         │
│                                                              │
│              SQLite ◀── log ──── Dashboard                   │
└─────────────────────────────────────────────────────────────┘
Layer	Component	Role
Physics	EnergyPlus 23.2	Real building simulation with building_model.idf + Chicago weather
Bridge	MCP Tool Bridge	get_sensor_data(), set_hvac_setpoints(), log_decision()
AI	Llama 3.3-70B via Groq	Autonomous HVAC decisions every 4 simulation hours
Storage	SQLite	Full audit trail — sensor readings, decisions, reasoning
UI	Streamlit + Plotly	Live dashboard, charts, comfort gauge, AI chatbot
✨ Key Features
🔄 Closed-Loop Autonomous Control
LLM receives real-time temperature from EnergyPlus
Decides heating/cooling setpoints based on comfort + energy rules
Writes setpoints directly to HVAC actuators — zero human intervention
📊 Live Dashboard
Temperature chart — zone temp vs comfort zone (21–24°C)
Energy comparison — AI usage vs 8 kWh baseline
Comfort gauge — ASHRAE 55 standard score
Energy donut — AI optimized vs baseline overhead
Carbon tracking — CO₂ avoided (CEA grid factor: 0.233 kg/kWh)
🎭 Multi-Scenario Comparison
Scenario	Outdoor Temp	Baseline	With AI	Saving
🌤 Normal Day	22°C	8.0 kWh	2.57 kWh	67.8%
☀️ Heatwave	42°C	18.0 kWh	4.2 kWh	76.7%
❄️ Winter Cold	-5°C	15.0 kWh	3.8 kWh	74.7%

Average AI savings: 73.1% across all scenarios

💬 AI Chat Assistant

Ask the building AI anything about the simulation in real-time:

"How much energy did we save?"
"Why did the AI lower the heating setpoint?"
"Is the building in the comfort zone?"
🧰 Tech Stack
├── Building Physics    → EnergyPlus 23.2 (pyenergyplus API)
├── LLM                 → Llama 3.3-70B via Groq API
├── AI Pattern          → MCP Tool Calling
├── Energy Standard     → ASHRAE 55 Comfort + ASHRAE 90.1
├── Carbon Factor       → CEA India Grid (0.233 kg CO₂/kWh)
├── Database            → SQLite (real-time audit trail)
├── Dashboard           → Streamlit + Plotly
└── Language            → Python 3.10+
📁 Project Structure
honeywell-smart-building-ai/
│
├── app.py                      # Main Streamlit dashboard
├── energyplus_real_bridge.py   # EnergyPlus ↔ LLM closed-loop
├── submission_runner.py        # EnergyPlus simulation runner
├── scenario_runner.py          # Multi-scenario simulator (Normal/Heatwave/Winter)
├── config.py                   # API keys + model config
│
├── building_model.idf          # EnergyPlus building definition
├── weather.epw                 # Chicago climate weather file
├── building_data.db            # SQLite database (auto-generated)
│
├── requirements.txt
└── README.md
⚙️ Setup & Run
Prerequisites
Python 3.10+
EnergyPlus 23.2 installed at C:\EnergyPlusV23-2-0
Groq API Key (free tier available)
Installation
bash
git clone https://github.com/YOUR_USERNAME/honeywell-smart-building-ai.git
cd honeywell-smart-building-ai
pip install -r requirements.txt
Configuration

Create a config.py:

python
GROQ_API_KEY = "your_groq_api_key_here"
GROQ_MODEL   = "llama-3.3-70b-versatile"
Run
bash
# Start dashboard
streamlit run app.py

In the sidebar:

Click ▶ Run EnergyPlus Simulation — runs real physics + LLM control
Click 🎭 Run All Scenarios — runs Normal, Heatwave, Winter comparison
📈 Results
Metric	Value
Energy saved (normal)	67.8% vs baseline
Average comfort score	81.7% (ASHRAE 55)
Carbon avoided	1.27 kg CO₂ per run
AI decisions per run	30 autonomous decisions
Simulation engine	Real EnergyPlus 23.2
🎯 What Makes This Different
Feature	Our System	Typical BMS
Physics engine	Real EnergyPlus	Simplified mock
AI control	Open-source LLM (Llama 3.3-70B)	Rule-based or GPT
Tool calling	True MCP pattern	Direct prompting
Transparency	Full decision log + reasoning	Black box
Carbon tracking	CEA grid factor	Not tracked
Multi-scenario	Heatwave / Winter / Normal	Single scenario
🏆 Hackathon

Honeywell Campus Connect 2026
Problem Statement: Eco-Loop Building Agents
Category: Software | Theme: Smart Cities & Urban Development

👨‍💻 Author

Soumyodip Bhattacharya
B.Tech CSE — VIT Bhopal University
BS Data Science — IIT Madras
Student ID: 20525115

📄 License

MIT License — see LICENSE for details.
