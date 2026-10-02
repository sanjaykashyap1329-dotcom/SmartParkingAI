import sqlite3

DATABASE = "parking.db"


def get_led_status(slot_name):
    connection = sqlite3.connect(DATABASE)

    row = connection.execute(
        """
        SELECT status, slot_type
        FROM parking_slots
        WHERE slot_name = ?
        """,
        (slot_name,)
    ).fetchone()

    connection.close()

    if not row:
        return "UNKNOWN"

    status, slot_type = row

    if status == "OCCUPIED":
        return "RED"

    if slot_type == "RESERVED":
        return "BLUE"

    if slot_type == "ACCESSIBLE":
        return "CYAN"

    return "GREEN"


def show_led_status():
    connection = sqlite3.connect(DATABASE)

    rows = connection.execute(
        """
        SELECT slot_name
        FROM parking_slots
        ORDER BY slot_name
        """
    ).fetchall()

    connection.close()

    print()
    print("SMART PARKING LED SIMULATOR")
    print("---------------------------")

    for (slot_name,) in rows:
        led = get_led_status(slot_name)

        print(
            f"{slot_name}: LED = {led}"
        )


if __name__ == "__main__":
    show_led_status()