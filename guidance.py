import sqlite3
import json
import math

DATABASE = "parking.db"
SLOTS_FILE = "config/slots_webcam.json"


def get_free_slots():
    connection = sqlite3.connect(DATABASE)

    rows = connection.execute(
        """
        SELECT slot_name, slot_type, reserved_for
        FROM parking_slots
        WHERE status = 'FREE'
        """
    ).fetchall()

    connection.close()

    return rows


def get_slot_coordinates():
    with open(SLOTS_FILE, "r") as file:
        data = json.load(file)

    return {
        slot["id"]: (
            (slot["x1"] + slot["x2"]) / 2,
            (slot["y1"] + slot["y2"]) / 2
        )
        for slot in data["slots"]
    }


def find_nearest_slot(
    entrance_x=320,
    entrance_y=20,
    authorization="NORMAL"
):
    free_slots = get_free_slots()
    coordinates = get_slot_coordinates()

    candidates = []

    for slot_name, slot_type, reserved_for in free_slots:

        if slot_type != "NORMAL":
            if authorization != reserved_for:
                continue

        if slot_name not in coordinates:
            continue

        slot_x, slot_y = coordinates[slot_name]

        distance = math.sqrt(
            (slot_x - entrance_x) ** 2
            +
            (slot_y - entrance_y) ** 2
        )

        candidates.append(
            (
                distance,
                slot_name,
                slot_type
            )
        )

    if not candidates:
        return None

    candidates.sort()

    distance, slot_name, slot_type = candidates[0]

    return {
        "slot": slot_name,
        "slot_type": slot_type,
        "distance": round(distance, 2)
    }


if __name__ == "__main__":
    print("Nearest Slot Guidance Test")
    print("--------------------------")

    result = find_nearest_slot()

    if result:
        print(
            f"Recommended slot: {result['slot']}"
        )
        print(
            f"Slot type: {result['slot_type']}"
        )
        print(
            f"Distance: {result['distance']}"
        )
    else:
        print("No suitable free slot available.")