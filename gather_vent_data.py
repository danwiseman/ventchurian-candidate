python
from typing import List, Dict, Any
from _flair import getRooms, getVentData
from room_interfaces import RoomVents
import asyncio


async def extract_vent_data(id: str) -> Dict[str, Any]:
    vent_readings = await getVentData(id)

    return {
        "ductPressure": vent_readings["attributes"]["duct-pressure"],
        "ductTemperatureC": vent_readings["attributes"]["duct-temperature-c"],
        "id": id,
        "percentOpen": vent_readings["attributes"]["percent-open"],
        "systemVoltage": vent_readings["attributes"]["system-voltage"],
    }

# Function to extract the desired properties from the data
async def extract_room_data() -> List[RoomVents]:
    data = await getRooms()

    room_vents_data: List[RoomVents] = []

    for item in data:
        vents_data = await asyncio.gather(
            *[extract_vent_data(vent["id"]) for vent in item["relationships"]["vents"]["data"]]
        )

        room_vents_data.append({
            "currentTemperatureC": item["attributes"]["current-temperature-c"],
            "setPointC": item["attributes"]["set-point-c"],
            "vents": vents_data,
        })

    return room_vents_data