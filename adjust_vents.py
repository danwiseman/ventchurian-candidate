from typing import List, Literal, TypedDict

Mode = Literal['heat', 'ac']

FULLY_OPEN = 100
FULLY_CLOSED = 0
HALF_OPEN = 50
MOSTLY_OPEN = 75
MOSTLY_CLOSED = 25

class RoomTemperature(TypedDict):
    room: str
    temperature: float


class VentControl:
    def open_vent(self, room: str) -> None:
        self.set_vent_percentage(room, FULLY_OPEN)


    def close_vent(self, room: str) -> None:
        self.set_vent_percentage(room, FULLY_CLOSED)

    def set_vent_percentage(self, room: str, percentage: float) -> None:
        # TODO document why this method is empty
        pass


def adjust_vents(room_temperatures: List[RoomTemperature], goal_temperature: float, mode: Mode, vent_control: VentControl) -> None:
    # First, open any vent that is in a room that is on the wrong side of the goal temp
    for rt in room_temperatures:
        if (mode == 'heat' and rt['temperature'] < goal_temperature) or (mode == 'ac' and rt['temperature'] > goal_temperature):
            vent_control.open_vent(rt['room'])

    # Find rooms that are on the desired side of the goal temp
    desired_side_rooms = [rt for rt in room_temperatures if
                        (mode == 'heat' and rt['temperature'] >= goal_temperature) or
                        (mode == 'ac' and rt['temperature'] <= goal_temperature)]

    # Sort the rooms by their distance to the goal temp
    sorted_desired_side_rooms = sorted(desired_side_rooms, key=lambda x: abs(x['temperature'] - goal_temperature))

    # If all vents are on the desired side of the goal temp for two of the rooms
    # that are closest to the goal temp, set those vents to 50%
    if len(sorted_desired_side_rooms) == len(room_temperatures) and len(sorted_desired_side_rooms) >= 2:
        vent_control.set_vent_percentage(sorted_desired_side_rooms[0]['room'], HALF_OPEN)
        vent_control.set_vent_percentage(sorted_desired_side_rooms[1]['room'], HALF_OPEN)
        sorted_desired_side_rooms = sorted_desired_side_rooms[2:]

    for rt in sorted_desired_side_rooms:
        vent_control.close_vent(rt['room'])