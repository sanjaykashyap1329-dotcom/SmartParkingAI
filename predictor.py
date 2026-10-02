import sqlite3
from datetime import datetime

DATABASE = "parking.db"


def predict_availability(target_hour):
    connection = sqlite3.connect(DATABASE)

    rows = connection.execute(
        """
        SELECT entry_time, exit_time
        FROM parking_records
        WHERE entry_time IS NOT NULL
        """
    ).fetchall()

    connection.close()

    if not rows:
        return None

    total_slots = connection_total_slots()

    if total_slots == 0:
        return None

    occupancy_samples = []

    for entry_time, exit_time in rows:
        try:
            entry = datetime.strptime(
                entry_time,
                "%Y-%m-%d %H:%M:%S"
            )

            if exit_time:
                exit_value = datetime.strptime(
                    exit_time,
                    "%Y-%m-%d %H:%M:%S"
                )
            else:
                exit_value = datetime.now()

            # Count this record if the vehicle was present
            # during the requested hour.
            if entry.hour <= target_hour <= exit_value.hour:
                occupancy_samples.append(1)

        except ValueError:
            continue

    if not occupancy_samples:
        return total_slots

    estimated_occupied = min(
        int(
            sum(occupancy_samples)
            /
            len(occupancy_samples)
            *
            total_slots
        ),
        total_slots
    )

    predicted_free = total_slots - estimated_occupied

    return predicted_free


def connection_total_slots():
    connection = sqlite3.connect(DATABASE)

    count = connection.execute(
        """
        SELECT COUNT(*)
        FROM parking_slots
        """
    ).fetchone()[0]

    connection.close()

    return count


if __name__ == "__main__":
    target_hour = 18

    result = predict_availability(
        target_hour
    )

    print()
    print("PREDICTIVE PARKING AVAILABILITY")
    print("-------------------------------")

    if result is None:
        print("Not enough parking history.")
    else:
        print(
            f"Predicted free slots at "
            f"{target_hour:02d}:00: {result}"
        )