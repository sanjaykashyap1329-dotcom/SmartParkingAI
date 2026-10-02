import sqlite3

DATABASE = "parking.db"


def connect_db():
    return sqlite3.connect(DATABASE)


def create_tables():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS parking_slots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slot_name TEXT UNIQUE NOT NULL,
        status TEXT NOT NULL,
        slot_type TEXT DEFAULT 'NORMAL',
        reserved_for TEXT DEFAULT NULL
    )
""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_name TEXT NOT NULL,
            vehicle_type TEXT,
            plate_number TEXT,
            entry_time TEXT,
            exit_time TEXT
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_tables()
    print("Database created successfully!")