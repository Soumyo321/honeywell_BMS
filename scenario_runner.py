# scenario_runner.py
import sqlite3
import json
from datetime import datetime
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)

DB_PATH = "building_data.db"

SCENARIOS = {
    "normal": {
        "name": "Normal Day",
        "outdoor_temp": 22.0,
        "baseline_energy": 8.0,
        "temp_offset": 0,
        "description": "Regular office day, mild weather"
    },
    "heatwave": {
        "name": "Heatwave",
        "outdoor_temp": 42.0,
        "baseline_energy": 18.0,
        "temp_offset": +6,
        "description": "Extreme heat, AC working overtime"
    },
    "winter": {
        "name": "Winter Cold",
        "outdoor_temp": -5.0,
        "baseline_energy": 15.0,
        "temp_offset": -8,
        "description": "Cold winter day, heating required"
    }
}

def init_scenario_tables():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for scenario in SCENARIOS.keys():
        c.execute(f'''CREATE TABLE IF NOT EXISTS scenario_{scenario} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            temperature REAL,
            heating_sp REAL,
            cooling_sp REAL,
            energy REAL,
            baseline_energy REAL,
            energy_saved REAL,
            comfort_score REAL,
            decision TEXT,
            reasoning TEXT
        )''')
    conn.commit()
    conn.close()

def ask_llm_scenario(temp, heating_sp, cooling_sp, scenario_name, outdoor_temp):
    scenario = SCENARIOS[scenario_name]
    try:
        prompt = f"""You are an autonomous HVAC optimizer for a smart building.

Scenario: {scenario['name']} - {scenario['description']}
Outdoor Temperature: {outdoor_temp}°C

Current state:
- Indoor temperature: {temp:.1f}°C
- Heating setpoint: {heating_sp}°C
- Cooling setpoint: {cooling_sp}°C
- Baseline energy (no AI): {scenario['baseline_energy']} kWh

Rules:
- Comfort zone: 21-24°C
- Heatwave: prioritize cooling, accept slightly higher energy
- Winter: prioritize heating efficiency
- Normal: balance comfort and energy saving
- heating must always be 2°C below cooling

Respond ONLY as valid JSON:
{{"heating_setpoint": 20.0, "cooling_setpoint": 23.5, "reasoning": "explain decision"}}"""

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )

        text = response.choices[0].message.content.strip()
        if "```" in text:
            text = text.split("```")[1].replace("json", "").strip()

        result = json.loads(text)
        heating = float(result["heating_setpoint"])
        cooling = float(result["cooling_setpoint"])
        reasoning = result.get("reasoning", "Optimizing")

        heating = max(18, min(22, heating))
        cooling = max(22, min(28, cooling))
        if heating >= cooling:
            heating = cooling - 2.0

        return heating, cooling, reasoning

    except Exception as e:
        print(f"[LLM Error] {e}")
        return heating_sp, cooling_sp, "Keeping current setpoints"

def run_scenario(scenario_name):
    scenario = SCENARIOS[scenario_name]
    print(f"\n{'='*50}")
    print(f"Running Scenario: {scenario['name']}")
    print(f"{'='*50}")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"DELETE FROM scenario_{scenario_name}")
    conn.commit()
    conn.close()

    # Simulate 24 timesteps (1 per hour)
    import random
    base_temp = 22.0 + scenario["temp_offset"]
    heating_sp = 21.0
    cooling_sp = 24.0

    for hour in range(24):
        # Realistic temperature variation
        time_factor = abs(hour - 14) / 14.0  # peak at 2pm
        if scenario_name == "heatwave":
            temp = base_temp + (1 - time_factor) * 4 + random.uniform(-0.5, 0.5)
        elif scenario_name == "winter":
            temp = base_temp - (1 - time_factor) * 3 + random.uniform(-0.5, 0.5)
        else:
            temp = base_temp + (1 - time_factor) * 2 + random.uniform(-0.3, 0.3)

        # Apply heating/cooling effect
        if temp < heating_sp:
            temp = min(temp + 1.5, heating_sp)
        elif temp > cooling_sp:
            temp = max(temp - 1.5, cooling_sp)

        # LLM decision every 4 hours
        if hour % 4 == 0:
            heating_sp, cooling_sp, reasoning = ask_llm_scenario(
                temp, heating_sp, cooling_sp, scenario_name, scenario["outdoor_temp"]
            )
            print(f"[{scenario['name']}] Hour {hour:02d} | Temp={temp:.1f}°C | H={heating_sp}°C C={cooling_sp}°C")
            print(f"  → {reasoning[:80]}")
        else:
            reasoning = "Maintaining setpoints"

        # Energy calculation based on scenario
        cooling_load = max(0, temp - cooling_sp) * 0.5
        heating_load = max(0, heating_sp - temp) * 0.4
        base_load = 1.5 if scenario_name == "normal" else (3.0 if scenario_name == "heatwave" else 2.5)
        energy = round(base_load + cooling_load + heating_load + random.uniform(0, 0.2), 3)

        baseline = scenario["baseline_energy"] / 24
        energy_saved = round(baseline - energy, 3)
        comfort = 100 if 21 <= temp <= 24 else max(0, 100 - abs(temp - 22.5) * 15)

        # Save to DB
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(f'''INSERT INTO scenario_{scenario_name}
            (timestamp, temperature, heating_sp, cooling_sp, energy,
             baseline_energy, energy_saved, comfort_score, decision, reasoning)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (datetime.now().replace(hour=hour, minute=0).isoformat(),
             round(temp, 2), heating_sp, cooling_sp, energy,
             round(baseline, 3), energy_saved, round(comfort, 1),
             f"H:{heating_sp}°C C:{cooling_sp}°C", reasoning))
        conn.commit()
        conn.close()

    print(f"✅ {scenario['name']} complete!")

def run_all_scenarios():
    init_scenario_tables()
    for scenario in SCENARIOS.keys():
        run_scenario(scenario)
    print("\n✅ All scenarios complete!")

if __name__ == "__main__":
    run_all_scenarios()