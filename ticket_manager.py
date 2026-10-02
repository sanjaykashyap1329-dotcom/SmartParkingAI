import sys
sys.path.append(".")

import sqlite3
from datetime import datetime

from utils.qr_generator import generate_qr


DATABASE = "parking.db"


def create_ticket(
    slot_name,
    plate_number="UNKNOWN",
    vehicle_type="car"
):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    entry_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute(
        """
        INSERT INTO parking_records
        (
            slot_name,
            vehicle_type,
            plate_number,
            entry_time
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            slot_name,
            vehicle_type,
            plate_number,
            entry_time
        )
    )

    ticket_id = cursor.lastrowid

    connection.commit()
    connection.close()

    ticket_code = f"TICKET{ticket_id:04d}"

    qr_path = generate_qr(
        ticket_code,
        slot_name,
        plate_number,
        entry_time
    )

    print()
    print("PARKING TICKET CREATED")
    print("----------------------")
    print(f"Ticket ID: {ticket_code}")
    print(f"Slot: {slot_name}")
    print(f"Plate: {plate_number}")
    print(f"Entry Time: {entry_time}")
    print(f"QR File: {qr_path}")

    return ticket_code


if __name__ == "__main__":
    create_ticket(
        "S1",
        "UNKNOWN",
        "car"
    )