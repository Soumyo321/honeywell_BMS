from database import init_db, log_sensor_reading, log_ai_decision, log_energy, get_recent_decisions, get_energy_history

init_db()

log_sensor_reading({
    "room_id": "room_1",
    "name": "Conference Room A",
    "temperature": 22.5,
    "co2": 650.0,
    "occupancy": 10,
    "energy_consumption": 2.5,
    "ac_setpoint": 22.0,
    "ventilation_level": 0.5,
    "lighting_level": 1.0
})

log_ai_decision("room_1", "Reduced AC setpoint to 23°C", "Occupancy low, saving energy", 2.5, 2.1)
log_energy(8.5, 12.0, 94.5)

print("Database OK")
print("Recent decisions:", get_recent_decisions())
print("Energy history:", get_energy_history())