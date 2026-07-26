from simulator import BuildingSimulator

sim = BuildingSimulator()
sim.update()

print("Simulator OK")
for room in sim.get_all_rooms_data():
    print(f"{room['name']}: Temp={room['temperature']}°C, CO2={room['co2']}ppm, Occupancy={room['occupancy']}, Energy={room['energy_consumption']}kWh")

print(f"Total Energy: {sim.get_total_energy()} kWh")