import sqlite3

DATABASE = "parking.db"


def check_parking_permission(
    slot_name,
    authorization="NORMAL"
):
    connection = sqlite3.connect(DATABASE)

    row = connection.execute(
        """
        SELECT slot_type, reserved_for
        FROM parking_slots
        WHERE slot_name = ?
        """,
        (slot_name,)
    ).fetchone()

    connection.close()

    if not row:
        return False, "Parking slot does not exist."

    slot_type, reserved_for = row

    if slot_type == "NORMAL":
        return True, "Normal parking allowed."

    if authorization == reserved_for:
        return True, f"Authorized for {slot_type} parking."

    return (
        False,
        f"Unauthorized use of {slot_type} slot. "
        f"Required: {reserved_for}."
    )


if __name__ == "__main__":
    print("Parking Rules Test")
    print("-------------------")

    tests = [
        ("S1", "NORMAL"),
        ("S1", "VIP"),
        ("S2", "NORMAL"),
        ("S2", "ACCESSIBILITY"),
        ("S3", "NORMAL")
    ]

    for slot_name, authorization in tests:
        allowed, message = check_parking_permission(
            slot_name,
            authorization
        )

        status = "ALLOWED" if allowed else "ALERT"

        print(
            f"{slot_name} | "
            f"{authorization} | "
            f"{status} | "
            f"{message}"
        )