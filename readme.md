# 🏢 Eco-Loop Building Agents
### AI-Powered Autonomous Building Management System (BMS)

> **Honeywell Campus Connect 2026**
>
> **Problem Statement:** Eco-Loop Building Agents  
> **Theme:** Smart Cities & Urban Development  
> **Category:** Software

---

## 🌐 Live Demo

**Dashboard:** https://soumyo321-honeywell-bms-app1-snuezx.streamlit.app/

---

## 📋 Problem Statement

**Student:** Soumyodip Bhattacharya  
**Student ID:** 20525115

Buildings account for nearly **40% of global energy consumption**, with HVAC systems being one of the largest contributors. Traditional Building Management Systems (BMS) operate using fixed schedules and static rules, resulting in:

- Excessive energy consumption
- Poor occupant comfort
- No real-time adaptation
- Lack of intelligent decision-making

### Our Solution

**Eco-Loop Building Agents** is a fully autonomous AI-powered Building Management System that combines:

- 🏢 Real EnergyPlus building physics simulation
- 🤖 Llama 3.3-70B reasoning via Groq API
- 🔧 MCP Tool Calling architecture
- 📊 Live monitoring dashboard
- 🌍 Carbon-aware optimization

The system continuously balances **comfort, energy efficiency, and sustainability** without human intervention.

---

# 🚀 Features

## 🔄 Autonomous Closed-Loop HVAC Control

The AI continuously controls the building by:

- Reading live sensor data from EnergyPlus
- Reasoning using Llama 3.3-70B
- Calling MCP tools
- Updating HVAC setpoints automatically
- Logging every decision with complete reasoning

No manual intervention is required.

---

## 🏢 Real Building Physics

Unlike mock simulations, this project uses:

- EnergyPlus 23.2
- Real IDF building model
- Real weather file
- Python callback API
- Dynamic HVAC actuators

This enables realistic building behavior.

---

## 📊 Live Dashboard

The Streamlit dashboard provides:

- 📈 Real-time temperature graph
- 🌡 Comfort zone visualization (21–24°C)
- ⚡ Energy consumption
- 🌍 Carbon emissions tracking
- 🎯 Comfort gauge
- 🍩 Energy optimization donut chart
- 📚 Decision history
- 💬 AI chatbot

---

## 🎭 Multi-Scenario Simulation

Compare AI performance across different weather conditions.

| Scenario | Outdoor Temp | Baseline | AI Usage | Energy Saved |
|-----------|-------------|-----------|----------|--------------|
| 🌤 Normal Day | 22°C | 8.0 kWh | 2.57 kWh | **67.8%** |
| ☀️ Heatwave | 42°C | 18.0 kWh | 4.2 kWh | **76.7%** |
| ❄️ Winter Cold | -5°C | 15.0 kWh | 3.8 kWh | **74.7%** |

### Average Savings

**73.1% energy reduction** across all scenarios.

---

## 🌍 Carbon Awareness

The system estimates avoided emissions using:

- **CEA India Grid Emission Factor**
- **0.233 kg CO₂/kWh**

Carbon savings are displayed live on the dashboard.

---

## 💬 AI Building Assistant

Interact with the building in natural language.

Example questions:

- How much energy did we save?
- Why did the AI lower the heating setpoint?
- Is the building comfortable?
- Show today's AI decisions.
- How much carbon was avoided?

---

# 🏗 System Architecture

```text
                    Closed-Loop AI Control

        +-----------------------------------------------+

        EnergyPlus 23.2
               │
               │ Live Sensor Data
               ▼
        MCP Tool Bridge
        ├── get_sensor_data()
        ├── set_hvac_setpoints()
        └── log_decision()
               │
               ▼
      Llama 3.3-70B (Groq API)
               │
      AI Decision + Tool Calls
               │
               ▼
        EnergyPlus Actuators
               │
               ▼
      SQLite Decision Database
               │
               ▼
      Streamlit Dashboard
```

---

# 🛠 Technology Stack

| Layer | Technology |
|--------|------------|
| Building Simulation | EnergyPlus 23.2 |
| AI Model | Llama 3.3-70B |
| LLM Provider | Groq API |
| AI Pattern | MCP Tool Calling |
| Comfort Standard | ASHRAE 55 |
| Energy Standard | ASHRAE 90.1 |
| Carbon Tracking | CEA India Grid |
| Database | SQLite |
| Dashboard | Streamlit |
| Charts | Plotly |
| Language | Python 3.10+ |

---

# 📂 Project Structure

```text
honeywell-smart-building-ai/
│
├── app.py
├── energyplus_real_bridge.py
├── submission_runner.py
├── scenario_runner.py
├── config.py
│
├── building_model.idf
├── weather.epw
├── building_data.db
│
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## Prerequisites

- Python 3.10+
- EnergyPlus 23.2
- Groq API Key

---

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/honeywell-smart-building-ai.git

cd honeywell-smart-building-ai
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure API

Create a file named `config.py`

```python
GROQ_API_KEY = "your_api_key_here"

GROQ_MODEL = "llama-3.3-70b-versatile"
```

---

# ▶️ Run

Start the dashboard.

```bash
streamlit run app.py
```

Inside the dashboard:

- ▶ Run EnergyPlus Simulation
- 🎭 Run All Scenarios

---

# 📊 Results

| Metric | Result |
|---------|--------|
| Normal Energy Saving | **67.8%** |
| Average Scenario Saving | **73.1%** |
| Comfort Score | **81.7%** |
| Carbon Avoided | **1.27 kg CO₂** |
| AI Decisions | **30 per simulation** |
| Simulation Engine | EnergyPlus 23.2 |

---

# 🎯 Why This Project?

Traditional Building Management Systems typically rely on static schedules and predefined rules.

Our system introduces:

- ✅ Real building physics
- ✅ Autonomous AI reasoning
- ✅ Explainable decision making
- ✅ Tool-calling architecture
- ✅ Carbon-aware optimization
- ✅ Scenario-based evaluation

Every HVAC adjustment is made intelligently and logged with transparent reasoning.

---

# 📈 Comparison

| Feature | Eco-Loop Building Agents | Traditional BMS |
|----------|-------------------------|-----------------|
| Real Physics Simulation | ✅ EnergyPlus | ❌ Simplified Models |
| AI Decision Making | ✅ Llama 3.3-70B | ❌ Rule-Based |
| MCP Tool Calling | ✅ Yes | ❌ No |
| Explainable Decisions | ✅ Full Reasoning Logs | ❌ Limited |
| Carbon Tracking | ✅ Yes | ❌ No |
| Multi-Scenario Testing | ✅ Normal / Heatwave / Winter | ❌ Single Scenario |
| Live Dashboard | ✅ Streamlit | ⚠ Limited |

---

# 🏆 Hackathon

**Honeywell Campus Connect 2026**

**Problem Statement:** Eco-Loop Building Agents

**Theme:** Smart Cities & Urban Development

**Category:** Software

---

# 👨‍💻 Author

**Soumyodip Bhattacharya**

- B.Tech CSE — VIT Bhopal University
- BS Data Science — IIT Madras
- Student ID: **20525115**

---

# 📄 License

This project is licensed under the **MIT License**.

---

## ⭐ If you found this project interesting, consider giving it a star!
