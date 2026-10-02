import sqlite3
from datetime import datetime

DATABASE = "parking.db"


def add_parking_record(slot_name, vehicle_type="car", plate_number="UNKNOWN"):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Check if this slot already has an active parking record
    existing = cursor.execute(
        """
        SELECT id
        FROM parking_records
        WHERE slot_name = ?
        AND exit_time IS NULL
        """,
        (slot_name,)
    ).fetchone()

    if existing:
        print(f"Active parking record already exists for {slot_name}")
        connection.close()
        return

    entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        INSERT INTO parking_records
        (slot_name, vehicle_type, plate_number, entry_time)
        VALUES (?, ?, ?, ?)
        """,
        (slot_name, vehicle_type, plate_number, entry_time)
    )

    connection.commit()
    connection.close()

    print(f"Parking record created for {slot_name}")
    print(f"Entry time: {entry_time}")


def record_exit(slot_name):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    exit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        UPDATE parking_records
        SET exit_time = ?
        WHERE slot_name = ?
        AND exit_time IS NULL
        """,
        (exit_time, slot_name)
    )

    if cursor.rowcount == 0:
        print(f"No active parking record found for {slot_name}")
    else:
        print(f"Exit recorded for {slot_name}")
        print(f"Exit time: {exit_time}")

    connection.commit()
    connection.close()


if __name__ == "__main__":
    add_parking_record("A1")