    # control_loop.py
    import time
    from datetime import datetime
    from simulator import BuildingSimulator
    from database import init_db, log_sensor_reading, log_energy
    from llm_agent import run_ai_decision
    from config import BUILDING_CONFIG, LOOP_INTERVAL_SECONDS

    simulator = BuildingSimulator()
    is_running = False

    def calculate_comfort_score(rooms_data):
        scores = []
        temp_min, temp_max = BUILDING_CONFIG["comfort_temp_range"]
        co2_max = BUILDING_CONFIG["comfort_co2_max"]

        for room in rooms_data:
            if room["occupancy"] == 0:
                continue
            temp_score = 100 if temp_min <= room["temperature"] <= temp_max else max(0, 100 - abs(room["temperature"] - 22) * 10)
            co2_score = 100 if room["co2"] <= co2_max else max(0, 100 - (room["co2"] - co2_max) * 0.1)
            scores.append((temp_score + co2_score) / 2)

        return round(sum(scores) / len(scores), 1) if scores else 100.0

    def run_single_cycle():
        simulator.update()
        rooms_data = simulator.get_all_rooms_data()

        for room in rooms_data:
            log_sensor_reading(room)

        total_energy = simulator.get_total_energy()
        baseline_energy = BUILDING_CONFIG["baseline_energy_per_hour"]
        comfort_score = calculate_comfort_score(rooms_data)

        log_energy(total_energy, baseline_energy, comfort_score)
        decisions = run_ai_decision(simulator)

        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Cycle complete")
        print(f"  Energy: {total_energy} kWh | Saved: {round(baseline_energy - total_energy, 2)} kWh")
        print(f"  Comfort: {comfort_score}% | Outdoor: {simulator.outdoor_temp}°C")
        print(f"  AI made {len(decisions)} decision(s)")

        return {
            "rooms_data": rooms_data,
            "total_energy": total_energy,
            "baseline_energy": baseline_energy,
            "comfort_score": comfort_score,
            "decisions": decisions
        }

    def start_loop():
        global is_running
        is_running = True
        init_db()
        print("Smart Building AI started...")
        while is_running:
            try:
                run_single_cycle()
                time.sleep(LOOP_INTERVAL_SECONDS)
            except KeyboardInterrupt:
                print("\nStopping...")
                is_running = False
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(5)

    def stop_loop():
        global is_running
        is_running = False

    if __name__ == "__main__":
        start_loop()