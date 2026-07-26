# database.py
import sqlite3
from datetime import datetime
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            room_id TEXT,
            room_name TEXT,
            temperature REAL,
            co2 REAL,
            occupancy INTEGER,
            energy_consumption REAL,
            ac_setpoint REAL,
            ventilation_level REAL,
            lighting_level REAL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS ai_decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            room_id TEXT,
            action TEXT,
            reason TEXT,
            energy_before REAL,
            energy_after REAL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS energy_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            total_energy REAL,
            baseline_energy REAL,
            energy_saved REAL,
            comfort_score REAL
        )
    ''')
    conn.commit()
    conn.close()

def log_sensor_reading(room_data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO sensor_readings
        (timestamp, room_id, room_name, temperature, co2, occupancy, energy_consumption, ac_setpoint, ventilation_level, lighting_level)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        room_data["room_id"],
        room_data["name"],
        room_data["temperature"],
        room_data["co2"],
        room_data["occupancy"],
        room_data["energy_consumption"],
        room_data["ac_setpoint"],
        room_data["ventilation_level"],
        room_data["lighting_level"]
    ))
    conn.commit()
    conn.close()

def log_ai_decision(room_id, action, reason, energy_before, energy_after):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO ai_decisions (timestamp, room_id, action, reason, energy_before, energy_after)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        room_id,
        action,
        reason,
        energy_before,
        energy_after
    ))
    conn.commit()
    conn.close()

def log_energy(total_energy, baseline_energy, comfort_score):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    energy_saved = baseline_energy - total_energy
    c.execute('''
        INSERT INTO energy_log (timestamp, total_energy, baseline_energy, energy_saved, comfort_score)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        total_energy,
        baseline_energy,
        energy_saved,
        comfort_score
    ))
    conn.commit()
    conn.close()

def get_recent_decisions(limit=20):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT timestamp, room_id, action, reason, energy_before, energy_after
        FROM ai_decisions ORDER BY id DESC LIMIT ?
    ''', (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_energy_history(limit=50):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT timestamp, total_energy, baseline_energy, energy_saved, comfort_score
        FROM energy_log ORDER BY id DESC LIMIT ?
    ''', (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_recent_sensor_readings(room_id, limit=10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT timestamp, temperature, co2, occupancy, energy_consumption
        FROM sensor_readings WHERE room_id = ? ORDER BY id DESC LIMIT ?
    ''', (room_id, limit))
    rows = c.fetchall()
    conn.close()
    return rows