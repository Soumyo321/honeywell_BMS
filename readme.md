# 🏢 Honeywell Smart Building AI

> AI-Powered Autonomous Building Management System using **EnergyPlus**, **Model Context Protocol (MCP)**, and **Open-Source LLMs** for intelligent HVAC optimization.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![EnergyPlus](https://img.shields.io/badge/EnergyPlus-23.2-green)
![Groq](https://img.shields.io/badge/Groq-LLM-orange)
![MCP](https://img.shields.io/badge/MCP-Tool%20Calling-purple)
![License](https://img.shields.io/badge/License-MIT-red)

---

## 📌 Overview

Buildings account for a significant portion of global energy consumption, with HVAC systems being the largest contributor. Traditional Building Management Systems rely on static rules that cannot adapt intelligently to changing occupancy or environmental conditions.

This project introduces an **AI-powered autonomous Building Management System** that integrates:

- 🏢 EnergyPlus Building Simulation
- 🤖 Open-source LLM (via Groq)
- 🔌 Model Context Protocol (MCP)
- 📊 Interactive Dashboard
- 💬 AI Building Assistant

The AI continuously monitors live building conditions, reasons about occupant comfort and energy efficiency, and autonomously adjusts HVAC setpoints to minimize energy usage while maintaining thermal comfort.

---

# 🚀 Features

### ✅ Autonomous HVAC Optimization

- AI automatically adjusts Heating & Cooling Setpoints
- Closed-loop control
- Continuous optimization

---

### 📈 Live Dashboard

Displays

- Current Temperature
- AI Decisions
- Energy Saved
- Comfort Score
- Temperature Trends
- Energy Comparison

---

### 💬 AI Building Assistant

The integrated chatbot can answer questions such as:

- What is happening in the building?
- Why did the AI change HVAC settings?
- How much energy has been saved?
- What is the current comfort level?
- Explain the latest AI decisions.

---

### 📊 EnergyPlus Integration

Uses EnergyPlus to simulate

- Building Physics
- Indoor Temperature
- HVAC Behaviour
- Energy Consumption
- Occupancy Effects

---

### 🔌 MCP Tool Calling

The LLM interacts with the building through Model Context Protocol tools.

Example workflow:

```
EnergyPlus
      ↓
Sensor Data
      ↓
MCP Tools
      ↓
LLM Reasoning
      ↓
HVAC Decision
      ↓
Updated Setpoints
```

---

# 🏗 System Architecture

```
                +--------------------+
                |  EnergyPlus Model  |
                +---------+----------+
                          |
                    Live Sensor Data
                          |
                 MCP Tool Interface
                          |
                +---------v----------+
                |    Groq LLM AI     |
                | Decision Engine    |
                +---------+----------+
                          |
              HVAC Setpoint Adjustment
                          |
                +---------v----------+
                |   Building Model   |
                +---------+----------+
                          |
                     Dashboard
                          |
                    AI Chat Assistant
```

---

# 🛠 Tech Stack

### Backend

- Python
- SQLite
- Pandas

### AI

- Groq API
- Llama 3.1 / Llama 3.3
- MCP (Model Context Protocol)

### Simulation

- EnergyPlus

### Frontend

- Streamlit
- Plotly

---

# 📂 Project Structure

```
Honeywell-Smart-Building-AI/

│
├── app.py
├── config.py
├── mcp_server.py
├── building_ai.py
├── simulation.py
├── energyplus/
│
├── database/
│
├── dashboard/
│
├── assets/
│
├── requirements.txt
│
└── README.md
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/Honeywell-Smart-Building-AI.git

cd Honeywell-Smart-Building-AI
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configure API Key

Create a `.env`

```env
GROQ_API_KEY=your_api_key
```

or edit

```python
config.py
```

```python
GROQ_MODEL="llama-3.1-8b-instant"
```

---

# ▶ Running the Project

```bash
streamlit run app.py
```

The dashboard will launch locally.

---

# 🔄 Workflow

1. Start EnergyPlus Simulation
2. Read Building Sensors
3. MCP exposes sensor tools
4. LLM analyzes building state
5. AI adjusts HVAC setpoints
6. Dashboard updates live
7. User can interact with AI Assistant

---

# 📊 Dashboard

The dashboard includes

- Live Temperature
- AI Decision Count
- Energy Saved
- Comfort Score
- Temperature Timeline
- Energy Comparison (Baseline vs AI)
- AI Decision Logs
- Interactive AI Chat Assistant

---

# 💬 Example Questions

```
What are we doing here?

```

```
Why did the AI adjust the HVAC settings?

```

```
How much energy has been saved?

```

```
Explain the latest AI decision.

```

```
What is the current comfort score?

```

```
Compare AI energy usage with baseline.

```

---

# 📈 Results

The autonomous controller successfully demonstrates

- ✅ Continuous HVAC optimization
- ✅ Reduced energy consumption
- ✅ Maintained occupant comfort
- ✅ Explainable AI decisions
- ✅ Real-time monitoring
- ✅ Interactive building assistant

---

# 🎯 Future Improvements

- Weather Forecast Integration
- Reinforcement Learning Controller
- Multi-building Support
- Occupancy Prediction
- Carbon Emission Optimization
- BACnet / IoT Sensor Integration
- Digital Twin Visualization

---

# 👥 Team

Developed for the

**AI-Powered Autonomous Smart Building Optimization Challenge**

Built with ❤️ using

- EnergyPlus
- MCP
- Groq LLM
- Streamlit
- Python

---

# 📜 License

This project is released under the MIT License.