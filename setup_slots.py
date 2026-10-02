import json
from database import connect_db

# Load parking slots
with open("config/slots.json", "r") as file:
    data = json.load(file)

slots = data["slots"]

# Connect to database
connection = connect_db()
cursor = connection.cursor()

# Add slots
for slot in slots:
    cursor.execute(
        """
        INSERT OR IGNORE INTO parking_slots (slot_name, status)
        VALUES (?, ?)
        """,
        (slot["id"], "FREE")
    )

connection.commit()
connection.close()

print(f"{len(slots)} parking slots added to database!")