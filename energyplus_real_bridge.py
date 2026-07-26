# energyplus_real_bridge.py
import sys
import os
from datetime import datetime
import queue
import json

sys.path.insert(0, "C:\\EnergyPlusV23-2-0")
os.environ["PATH"] = "C:\\EnergyPlusV23-2-0" + os.pathsep + os.environ["PATH"]

from pyenergyplus.api import EnergyPlusAPI
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL
import sqlite3

DB_PATH = "building_data.db"
client = Groq(api_key=GROQ_API_KEY)
api = EnergyPlusAPI()
state = api.state_manager.new_state()

handles = {
    "zone_temp": -1,
    "heating_actuator": -1,
    "cooling_actuator": -1,
     "facility_energy": -1,
    "initialized": False
}

current_heating_sp = [21.0]
current_cooling_sp = [24.0]
call_every = [0]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sensor_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT, room_id TEXT, room_name TEXT,
        temperature REAL, co2 REAL, occupancy INTEGER,
        energy_consumption REAL, ac_setpoint REAL,
        ventilation_level REAL, lighting_level REAL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS ai_decisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT, room_id TEXT, action TEXT,
        reason TEXT, energy_before REAL, energy_after REAL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS energy_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT, total_energy REAL,
        baseline_energy REAL, energy_saved REAL, comfort_score REAL
    )''')
    conn.commit()
    conn.close()

# def save_reading(temp, heating_sp, cooling_sp):
#     """Save sensor reading to DB"""
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
    
#     # Calculate energy (simplified ASHRAE model)
#     cooling_load = max(0, temp - cooling_sp) * 0.36
#     heating_load = max(0, heating_sp - temp) * 0.36
#     energy = round((cooling_load + heating_load) / 3.5 + 2.0, 2)
#     baseline = 8.0
    
#     # Comfort score
#     comfort = 100 if 21 <= temp <= 24 else max(0, 100 - abs(temp - 22.5) * 10)
    
#     # Save sensor reading
#     c.execute('''INSERT INTO sensor_readings 
#         (timestamp, room_id, room_name, temperature, co2, occupancy, 
#          energy_consumption, ac_setpoint, ventilation_level, lighting_level)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
#         (datetime.now().isoformat(), "core_zone", "Core Zone",
#          temp, 500, 10, energy, heating_sp, 0.5, 1.0))
    
#     # Save energy log
#     c.execute('''INSERT INTO energy_log 
#         (timestamp, total_energy, baseline_energy, energy_saved, comfort_score)
#         VALUES (?, ?, ?, ?, ?)''',
#         (datetime.now().isoformat(), energy, baseline, baseline - energy, comfort))
    
#     conn.commit()
#     conn.close()
#     return energy


def save_reading(temp, heating_sp, cooling_sp, real_energy_j=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Real EnergyPlus energy (Joules → kWh)
    if real_energy_j and real_energy_j > 0:
        energy = round(real_energy_j / 3_600_000, 3)
    else:
        # Fallback only if meter not available
        cooling_load = max(0, temp - cooling_sp) * 0.36
        heating_load = max(0, heating_sp - temp) * 0.36
        energy = round((cooling_load + heating_load) / 3.5 + 2.0, 2)
    
    baseline = 8.0
    comfort = 100 if 21 <= temp <= 24 else max(0, 100 - abs(temp - 22.5) * 10)
    
    c.execute('''INSERT INTO sensor_readings 
        (timestamp, room_id, room_name, temperature, co2, occupancy, 
         energy_consumption, ac_setpoint, ventilation_level, lighting_level)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (datetime.now().isoformat(), "core_zone", "Core Zone",
         temp, 500, 10, energy, heating_sp, 0.5, 1.0))
    
    c.execute('''INSERT INTO energy_log 
        (timestamp, total_energy, baseline_energy, energy_saved, comfort_score)
        VALUES (?, ?, ?, ?, ?)''',
        (datetime.now().isoformat(), energy, baseline, baseline - energy, comfort))
    
    conn.commit()
    conn.close()
    return energy
def save_decision(action, reason, e_before, e_after):
    """Save AI decision to DB"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO ai_decisions
        (timestamp, room_id, action, reason, energy_before, energy_after)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (datetime.now().isoformat(), "core_zone", action, reason, e_before, e_after))
    conn.commit()
    conn.close()

def ask_llm(temp, heating_sp, cooling_sp):
    """Ask LLM for new setpoints"""
    try:
        prompt = f"""You are an autonomous HVAC optimizer for a smart building.

Current state:
- Indoor temperature: {temp:.1f}C
- Heating setpoint: {heating_sp}C
- Cooling setpoint: {cooling_sp}C

Rules:
- Comfort zone: 21-24C
- If temp < 20C: raise heating to 21.5C (cold recovery needed)
- If temp > 25C: lower cooling to 23.0C (active cooling needed)  
- If 21-24C and heating > 20C: lower heating to 20.0C (save energy)
- If 21-24C and cooling > 23.5C: lower cooling to 23.5C (save energy)
- heating must always be 2C below cooling minimum

You MUST change setpoints. Always optimize for energy saving while maintaining comfort.
Respond ONLY as valid JSON with no extra text:
{{"heating_setpoint": 21.0, "cooling_setpoint": 24.0, "reasoning": "explain your decision"}}"""

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )
        
        text = response.choices[0].message.content.strip()
        
        # Clean up response
        if "```" in text:
            text = text.split("```")[1].replace("json", "").strip()
        
        result = json.loads(text)
        heating = float(result["heating_setpoint"])
        cooling = float(result["cooling_setpoint"])
        reasoning = result.get("reasoning", "Optimizing setpoints")
        
        # Safety bounds
        heating = max(18, min(22, heating))
        cooling = max(22, min(28, cooling))
        if heating >= cooling:
            heating = cooling - 2.0
        
        return heating, cooling, reasoning
        
    except Exception as e:
        print(f"[LLM Error] {e}")
        return heating_sp, cooling_sp, "Keeping current setpoints"

def time_step_callback(state):
    """Called every timestep by EnergyPlus"""
    global handles, current_heating_sp, current_cooling_sp, call_every
    
    if api.exchange.warmup_flag(state):
        return
    
    if not handles["initialized"]:
        if api.exchange.api_data_fully_ready(state):
            handles["zone_temp"] = api.exchange.get_variable_handle(
                state, "Zone Mean Air Temperature", "Core_ZN"
            )
            handles["heating_actuator"] = api.exchange.get_actuator_handle(
                state, "Schedule:Constant", "Schedule Value", "AI_Heating_Setpoint"
            )
            handles["cooling_actuator"] = api.exchange.get_actuator_handle(
                state, "Schedule:Constant", "Schedule Value", "AI_Cooling_Setpoint"
            )
            # ← YE ADD KAR
            handles["facility_energy"] = api.exchange.get_meter_handle(
                state, "Electricity:Facility"
            )
            handles["initialized"] = True
            print("[EP] Handles initialized")
            return
    
    temp = api.exchange.get_variable_value(state, handles["zone_temp"])
    if temp == 0:
        return
    
    call_every[0] += 1
    
    # Log every 4 timesteps (every simulated hour)
    # if call_every[0] % 4 == 0:
    #     energy = save_reading(temp, current_heating_sp[0], current_cooling_sp[0])
    #     print(f"[EP] Temp={temp:.2f}C H={current_heating_sp[0]}C C={current_cooling_sp[0]}C E={energy}kWh")
    if call_every[0] % 4 == 0:
    # Real energy from EnergyPlus meter
        real_energy_j = None
        if handles["facility_energy"] != -1:
            real_energy_j = api.exchange.get_meter_value(
                state, handles["facility_energy"]
            )
        
        energy = save_reading(
            temp, 
            current_heating_sp[0], 
            current_cooling_sp[0],
            real_energy_j  # ← real value pass kar raha hai
        )
        print(f"[EP] Temp={temp:.2f}C H={current_heating_sp[0]}C C={current_cooling_sp[0]}C E={energy}kWh")
    # Ask LLM every 16 timesteps (every 4 simulated hours)
    if call_every[0] % 16 == 0:
        print(f"[LLM] Asking for decision at Temp={temp:.2f}C...")
        
        e_before = max(0, temp - current_cooling_sp[0]) * 0.1 + 2.0
        
        new_heating, new_cooling, reasoning = ask_llm(
            temp, current_heating_sp[0], current_cooling_sp[0]
        )
        
        # Apply new setpoints
        api.exchange.set_actuator_value(state, handles["heating_actuator"], new_heating)
        api.exchange.set_actuator_value(state, handles["cooling_actuator"], new_cooling)
        
        current_heating_sp[0] = new_heating
        current_cooling_sp[0] = new_cooling
        
        e_after = max(0, temp - new_cooling) * 0.1 + 2.0
        
        save_decision(
            f"H:{new_heating}C C:{new_cooling}C",
            reasoning,
            round(e_before, 2),
            round(e_after, 2)
        )
        
        print(f"[LLM] Decision: H={new_heating}C C={new_cooling}C | {reasoning[:60]}")
    
    # Apply current setpoints every timestep
    api.exchange.set_actuator_value(state, handles["heating_actuator"], current_heating_sp[0])
    api.exchange.set_actuator_value(state, handles["cooling_actuator"], current_cooling_sp[0])

def run_energyplus():
    init_db()
    print("\n[EP] Starting simulation...\n")
    
    api.runtime.callback_begin_zone_timestep_after_init_heat_balance(state, time_step_callback)
    
    api.runtime.run_energyplus(state, [
        "-w", "weather.epw",
        "-d", "output",
        "-r",
        "building_model.idf"
    ])
    
    print("\n[EP] Simulation complete!")

def get_sensor_data():
    return {
        "temp": 22.0,
        "heating_sp": current_heating_sp[0],
        "cooling_sp": current_cooling_sp[0],
        "time": datetime.now()
    }

def send_setpoint(heating, cooling):
    current_heating_sp[0] = heating
    current_cooling_sp[0] = cooling

if __name__ == "__main__":
    run_energyplus()