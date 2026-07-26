
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
BUILDING_CONFIG = {
    "rooms": [
        {"id": "room_1", "name": "Conference Room A", "capacity": 20, "area_sqm": 60},
        {"id": "room_2", "name": "Open Office",        "capacity": 50, "area_sqm": 200},
        {"id": "room_3", "name": "Server Room",        "capacity": 2,  "area_sqm": 30},
        {"id": "room_4", "name": "Lobby",              "capacity": 30, "area_sqm": 100},
    ],
    "operating_hours": {"start": 8, "end": 20},
    "comfort_temp_range": (21, 24),
    "comfort_co2_max": 1000,
    "baseline_energy_per_hour": 50.0
}

# GROQ_MODEL = "llama-3.3-70b-versatile"



GROQ_MODEL = "llama-3.1-8b-instant"

DB_PATH = "building_data.db"
LOOP_INTERVAL_SECONDS = 30