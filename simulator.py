# simulator.py
import numpy as np
import requests
from datetime import datetime
from config import BUILDING_CONFIG

class BuildingSimulator:
    def __init__(self):
        self.rooms = {}
        self.outdoor_temp = 32.0
        self.time_step = 0

        for room in BUILDING_CONFIG["rooms"]:
            self.rooms[room["id"]] = {
                "name": room["name"],
                "capacity": room["capacity"],
                "area_sqm": room["area_sqm"],
                "temperature": 22.0,
                "co2": 400.0,
                "occupancy": 0,
                "ac_setpoint": 22.0,
                "ventilation_level": 0.5,
                "lighting_level": 1.0,
                "energy_consumption": 0.0,
            }

    def get_real_outdoor_temp(self):
        try:
            url = "https://api.open-meteo.com/v1/forecast?latitude=23.2599&longitude=77.4126&current=temperature_2m"
            response = requests.get(url, timeout=5)
            data = response.json()
            return data["current"]["temperature_2m"]
        except:
            hour = datetime.now().hour
            return 25 + 8 * np.sin((hour - 6) * np.pi / 12)

    def get_occupancy(self, room_id, hour):
        patterns = {
            "room_1": [0,0,0,0,0,0,0,0,5,15,18,20,10,18,20,15,10,5,2,0,0,0,0,0],
            "room_2": [0,0,0,0,0,0,0,5,20,40,45,50,30,45,50,45,35,20,10,5,0,0,0,0],
            "room_3": [1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1],
            "room_4": [0,0,0,0,0,0,0,10,20,25,20,15,10,15,20,25,20,15,10,5,2,0,0,0],
        }
        base = patterns.get(room_id, [0]*24)[hour]
        noise = np.random.randint(-2, 3)
        return max(0, base + noise)

    def update(self):
        now = datetime.now()
        hour = now.hour
        self.outdoor_temp = self.get_real_outdoor_temp()
        self.time_step += 1

        for room_id, room in self.rooms.items():
            room["occupancy"] = self.get_occupancy(room_id, hour)

            # Newton's Law of Cooling (real thermal physics)
            temp_diff = self.outdoor_temp - room["temperature"]
            ac_effect = (room["ac_setpoint"] - room["temperature"]) * 0.3
            occupancy_heat = room["occupancy"] * 0.01
            room["temperature"] += (temp_diff * 0.02 + ac_effect + occupancy_heat)
            room["temperature"] = round(room["temperature"], 2)

            # CO2 mass balance (ASHRAE 62.1)
            co2_increase = room["occupancy"] * 0.5
            co2_decrease = room["ventilation_level"] * 50
            room["co2"] += co2_increase - co2_decrease
            room["co2"] = max(400, round(room["co2"], 1))

            # Energy (ASHRAE 90.1 standards)
            cooling_load = max(0, room["temperature"] - room["ac_setpoint"]) * 0.36
            ac_energy = cooling_load / 3.5
            lighting_energy = room["lighting_level"] * (10 * room["area_sqm"] / 1000)
            ventilation_energy = room["ventilation_level"] * room["occupancy"] * 0.3 * 0.001
            room["energy_consumption"] = round(ac_energy + lighting_energy + ventilation_energy, 2)

    def get_room_data(self, room_id):
        room = self.rooms[room_id]
        return {
            "room_id": room_id,
            "name": room["name"],
            "temperature": room["temperature"],
            "co2": room["co2"],
            "occupancy": room["occupancy"],
            "ac_setpoint": room["ac_setpoint"],
            "ventilation_level": room["ventilation_level"],
            "lighting_level": room["lighting_level"],
            "energy_consumption": room["energy_consumption"],
            "outdoor_temp": self.outdoor_temp,
            "timestamp": datetime.now().isoformat()
        }

    def get_all_rooms_data(self):
        return [self.get_room_data(room_id) for room_id in self.rooms]

    def set_ac_setpoint(self, room_id, temperature):
        if room_id in self.rooms:
            self.rooms[room_id]["ac_setpoint"] = max(18, min(28, temperature))
            return True
        return False

    def set_ventilation(self, room_id, level):
        if room_id in self.rooms:
            self.rooms[room_id]["ventilation_level"] = max(0.1, min(1.0, level))
            return True
        return False

    def set_lighting(self, room_id, level):
        if room_id in self.rooms:
            self.rooms[room_id]["lighting_level"] = max(0.0, min(1.0, level))
            return True
        return False

    def get_total_energy(self):
        return round(sum(r["energy_consumption"] for r in self.rooms.values()), 2)

    def inject_fault(self, room_id, fault_type):
        if fault_type == "temp_spike":
            self.rooms[room_id]["temperature"] = 45.0
        elif fault_type == "co2_spike":
            self.rooms[room_id]["co2"] = 5000.0
        elif fault_type == "occupancy_surge":
            self.rooms[room_id]["occupancy"] = self.rooms[room_id]["capacity"]

    def apply_scenario(self, scenario):
        if scenario == "heatwave":
            self.outdoor_temp = 42.0
        elif scenario == "power_saving":
            for room in self.rooms.values():
                room["ac_setpoint"] = 26.0
                room["lighting_level"] = 0.5
        elif scenario == "occupancy_surge":
            for room_id in self.rooms:
                self.rooms[room_id]["occupancy"] = self.rooms[room_id]["capacity"]
        elif scenario == "normal":
            self.outdoor_temp = self.get_real_outdoor_temp()
            for room in self.rooms.values():
                room["ac_setpoint"] = 22.0
                room["lighting_level"] = 1.0