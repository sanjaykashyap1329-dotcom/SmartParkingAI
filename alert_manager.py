import sqlite3
from datetime import datetime

DATABASE = "parking.db"

# Demo threshold.
# Change this later from the dashboard/settings.
OVERSTAY_MINUTES = 30


def create_alert(slot_name, alert_type, message):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Prevent duplicate unresolved alerts for the same slot/type
    existing = cursor.execute(
        """
        SELECT id
        FROM alerts
        WHERE slot_name = ?
        AND alert_type = ?
        AND resolved = 0
        """,
        (slot_name, alert_type)
    ).fetchone()

    if existing:
        connection.close()
        return False

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        INSERT INTO alerts
        (
            slot_name,
            alert_type,
            message,
            created_at,
            resolved
        )
        VALUES (?, ?, ?, ?, 0)
        """,
        (
            slot_name,
            alert_type,
            message,
            created_at
        )
    )

    connection.commit()
    connection.close()

    print(f"[ALERT] {message}")

    return True


def check_overstay():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    records = cursor.execute(
        """
        SELECT slot_name, entry_time
        FROM parking_records
        WHERE exit_time IS NULL
        """
    ).fetchall()

    connection.close()

    now = datetime.now()

    for slot_name, entry_time in records:

        entry = datetime.strptime(
            entry_time,
            "%Y-%m-%d %H:%M:%S"
        )

        duration_minutes = (
            now - entry
        ).total_seconds() / 60

        if duration_minutes >= OVERSTAY_MINUTES:

            create_alert(
                slot_name,
                "OVERSTAY",
                f"Vehicle in {slot_name} has exceeded "
                f"the {OVERSTAY_MINUTES}-minute parking limit."
            )


if __name__ == "__main__":

    print("Overstay alert test")

    check_overstay()

    print("Overstay check complete.")