import sqlite3
import json

DATABASE = "parking.db"


def update_slot_status(slot_name, status):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE parking_slots
        SET status = ?
        WHERE slot_name = ?
        """,
        (status, slot_name)
    )

    connection.commit()
    connection.close()


def show_status():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    rows = cursor.execute(
        "SELECT slot_name, status FROM parking_slots"
    ).fetchall()

    connection.close()

    print("\nCURRENT PARKING STATUS")
    print("----------------------")

    for slot_name, status in rows:
        print(f"{slot_name}: {status}")


if __name__ == "__main__":
    show_status()