import sqlite3
from collections import Counter
from datetime import datetime

DATABASE = "parking.db"


def get_peak_hours():
    connection = sqlite3.connect(DATABASE)

    rows = connection.execute(
        """
        SELECT entry_time
        FROM parking_records
        WHERE entry_time IS NOT NULL
        """
    ).fetchall()

    connection.close()

    hour_counts = Counter()

    for (entry_time,) in rows:
        try:
            time_value = datetime.strptime(
                entry_time,
                "%Y-%m-%d %H:%M:%S"
            )

            hour_counts[time_value.hour] += 1

        except ValueError:
            continue

    return hour_counts


def show_peak_hours():
    hour_counts = get_peak_hours()

    print()
    print("PARKING PEAK-HOUR ANALYTICS")
    print("---------------------------")

    if not hour_counts:
        print("No parking records available.")
        return

    for hour in sorted(hour_counts):
        print(
            f"{hour:02d}:00 - "
            f"{hour:02d}:59 : "
            f"{hour_counts[hour]} entries"
        )

    peak_hour = max(
        hour_counts,
        key=hour_counts.get
    )

    print()
    print(
        f"Peak hour: {peak_hour:02d}:00 - "
        f"{peak_hour:02d}:59"
    )
    print(
        f"Entries: {hour_counts[peak_hour]}"
    )


if __name__ == "__main__":
    show_peak_hours()