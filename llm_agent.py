# llm_agent.py
import json
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL, BUILDING_CONFIG
from database import log_ai_decision

client = Groq(api_key=GROQ_API_KEY)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "set_ac_setpoint",
            "description": "Update the AC temperature setpoint for a room to save energy or improve comfort",
            "parameters": {
                "type": "object",
                "properties": {
                    "room_id": {"type": "string", "description": "The room ID"},
                    "temperature": {"type": "number", "description": "Target temperature in Celsius (18-28)"},
                    "reason": {"type": "string", "description": "Why this change is being made"}
                },
                "required": ["room_id", "temperature", "reason"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_ventilation",
            "description": "Adjust ventilation level for a room to control CO2 or save energy",
            "parameters": {
                "type": "object",
                "properties": {
                    "room_id": {"type": "string", "description": "The room ID"},
                    "level": {"type": "number", "description": "Ventilation level 0.1 to 1.0"},
                    "reason": {"type": "string", "description": "Why this change is being made"}
                },
                "required": ["room_id", "level", "reason"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_lighting",
            "description": "Adjust lighting level for a room to save energy",
            "parameters": {
                "type": "object",
                "properties": {
                    "room_id": {"type": "string", "description": "The room ID"},
                    "level": {"type": "number", "description": "Lighting level 0.0 to 1.0"},
                    "reason": {"type": "string", "description": "Why this change is being made"}
                },
                "required": ["room_id", "level", "reason"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "flag_sensor_fault",
            "description": "Flag a sensor reading as potentially faulty and unreliable",
            "parameters": {
                "type": "object",
                "properties": {
                    "room_id": {"type": "string", "description": "The room ID"},
                    "sensor_type": {"type": "string", "description": "Type: temperature, co2, occupancy"},
                    "reason": {"type": "string", "description": "Why this sensor reading seems faulty"}
                },
                "required": ["room_id", "sensor_type", "reason"]
            }
        }
    }
]

def build_prompt(rooms_data, total_energy, baseline_energy):
    comfort_range = BUILDING_CONFIG["comfort_temp_range"]
    co2_max = BUILDING_CONFIG["comfort_co2_max"]

    rooms_summary = ""
    for room in rooms_data:
        temp_status = "OK" if comfort_range[0] <= room["temperature"] <= comfort_range[1] else "WARNING"
        co2_status = "OK" if room["co2"] <= co2_max else "CRITICAL"
        rooms_summary += f"""
        Room: {room['name']} (ID: {room['room_id']})
        - Temperature: {room['temperature']}°C [{temp_status}] (setpoint: {room['ac_setpoint']}°C)
        - CO2: {room['co2']}ppm [{co2_status}] (max: {co2_max}ppm)
        - Occupancy: {room['occupancy']} people
        - Ventilation: {room['ventilation_level']}
        - Lighting: {room['lighting_level']}
        - Energy: {room['energy_consumption']} kWh
        - Outdoor Temp: {room['outdoor_temp']}°C
        """

    return f"""You are an autonomous AI Building Management System.

Your goals in priority order:
1. SAFETY: CO2 must never exceed 1000ppm. Temperature must stay 18-28°C always.
2. COMFORT: Keep temperature 21-24°C in occupied rooms.
3. ENERGY: Minimize energy without sacrificing safety or comfort.

Current building status:
{rooms_summary}

Total Energy: {total_energy} kWh | Baseline: {baseline_energy} kWh | Saved: {round(baseline_energy - total_energy, 2)} kWh

Rules:
- Empty rooms: raise AC setpoint to 26°C, turn off lights
- Server Room: always keep below 24°C
- CO2 > 800ppm: increase ventilation immediately
- Outdoor temp > 35°C: pre-cool occupied rooms
- Sensor reading physically impossible (temp > 40°C indoors, CO2 > 4000ppm): flag as fault
- Always explain reasoning clearly

Analyze and optimize autonomously. Make all necessary tool calls."""

def run_ai_decision(simulator):
    rooms_data = simulator.get_all_rooms_data()
    total_energy = simulator.get_total_energy()
    baseline_energy = BUILDING_CONFIG["baseline_energy_per_hour"]

    prompt = build_prompt(rooms_data, total_energy, baseline_energy)
    messages = [{"role": "user", "content": prompt}]

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
        max_tokens=2000
    )

    decisions_made = []

    if response.choices[0].message.tool_calls:
        for tool_call in response.choices[0].message.tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            energy_before = simulator.get_total_energy()

            if func_name == "set_ac_setpoint":
                simulator.set_ac_setpoint(args["room_id"], args["temperature"])
                action = f"Set AC to {args['temperature']}°C in {args['room_id']}"
            elif func_name == "set_ventilation":
                simulator.set_ventilation(args["room_id"], args["level"])
                action = f"Set ventilation to {args['level']} in {args['room_id']}"
            elif func_name == "set_lighting":
                simulator.set_lighting(args["room_id"], args["level"])
                action = f"Set lighting to {args['level']} in {args['room_id']}"
            elif func_name == "flag_sensor_fault":
                action = f"FAULT DETECTED: {args['sensor_type']} sensor in {args['room_id']}"

            energy_after = simulator.get_total_energy()
            reason = args.get("reason", "No reason provided")
            room_id = args.get("room_id", "building")

            log_ai_decision(room_id, action, reason, energy_before, energy_after)
            decisions_made.append({
                "action": action,
                "reason": reason,
                "room_id": room_id
            })
    else:
        decisions_made.append({
            "action": "No changes needed",
            "reason": response.choices[0].message.content or "Building operating optimally",
            "room_id": "building"
        })

    return decisions_made