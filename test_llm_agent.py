from simulator import BuildingSimulator
from database import init_db
from llm_agent import run_ai_decision

init_db()

sim = BuildingSimulator()

# Simulate a problem scenario
sim.rooms["room_2"]["co2"] = 1200.0
sim.rooms["room_2"]["occupancy"] = 45
sim.rooms["room_1"]["occupancy"] = 0
sim.rooms["room_3"]["temperature"] = 27.0

print("Running AI decision...")
decisions = run_ai_decision(sim)

print("\nAI Decisions:")
for d in decisions:
    print(f"  Action: {d['action']}")
    print(f"  Reason: {d['reason']}")
    print()