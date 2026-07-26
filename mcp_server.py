# mcp_server.py
"""
MCP-style tool server for Building Management System.
Exposes building control capabilities as tools for the LLM.
"""

from energyplus_real_bridge import get_sensor_data, send_setpoint
import json

class BuildingMCPServer:
    """Implements MCP tool pattern for building control"""
    
    def __init__(self):
        self.tools = [
            {
                "name": "get_building_state",
                "description": "Read current building sensor data: temperature, setpoints",
                "parameters": {}
            },
            {
                "name": "set_hvac_setpoints",
                "description": "Update HVAC heating and cooling setpoints",
                "parameters": {
                    "heating_setpoint": "float (18-23°C)",
                    "cooling_setpoint": "float (23-28°C)"
                }
            },
            {
                "name": "calculate_comfort_score",
                "description": "Calculate comfort score based on current conditions",
                "parameters": {}
            }
        ]
    
    def get_tools(self):
        """Return available tools"""
        return self.tools
    
    def execute_tool(self, tool_name, params):
        """Execute MCP tool"""
        if tool_name == "get_building_state":
            return self._get_building_state()
        elif tool_name == "set_hvac_setpoints":
            return self._set_hvac_setpoints(params)
        elif tool_name == "calculate_comfort_score":
            return self._calculate_comfort_score()
        else:
            return {"error": f"Unknown tool: {tool_name}"}
    
    def _get_building_state(self):
        """Read real EnergyPlus data"""
        data = get_sensor_data()
        return {
            "status": "success",
            "indoor_temperature": data["temp"],
            "heating_setpoint": data["heating_sp"],
            "cooling_setpoint": data["cooling_sp"],
            "timestamp": str(data["time"])
        }
    
    def _set_hvac_setpoints(self, params):
        """Write new setpoints to EnergyPlus"""
        heating = float(params.get("heating_setpoint", 21.0))
        cooling = float(params.get("cooling_setpoint", 24.0))
        
        if heating >= cooling:
            return {"error": "Heating setpoint must be < cooling setpoint"}
        if heating < 18 or heating > 23:
            return {"error": "Heating setpoint must be 18-23°C"}
        if cooling < 23 or cooling > 28:
            return {"error": "Cooling setpoint must be 23-28°C"}
        
        send_setpoint(heating, cooling)
        
        return {
            "status": "success",
            "message": f"Setpoints updated: Heating={heating}°C, Cooling={cooling}°C"
        }
    
    def _calculate_comfort_score(self):
        """ASHRAE comfort scoring"""
        data = get_sensor_data()
        temp = data["temp"]
        
        # Simple ASHRAE scoring: 21-24°C is optimal
        if 21 <= temp <= 24:
            score = 100
        elif 20 <= temp < 21 or 24 < temp <= 25:
            score = 90
        elif 19 <= temp < 20 or 25 < temp <= 26:
            score = 70
        else:
            score = 50
        
        return {
            "status": "success",
            "comfort_score": score,
            "temperature": temp
        }