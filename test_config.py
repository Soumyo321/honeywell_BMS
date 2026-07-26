from config import GROQ_API_KEY, BUILDING_CONFIG

print("Config OK")
print(f"Rooms: {len(BUILDING_CONFIG['rooms'])}")
print(f"API Key set: {bool(GROQ_API_KEY)}")