import sqlite3
import json
from ultralytics import YOLO
import cv2

DATABASE = "parking.db"
IMAGE_PATH = "data/cars.jpg"


def update_database(slot_name, status):
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


# Load image
image = cv2.imread(IMAGE_PATH)

# Load slots
with open("config/slots.json", "r") as file:
    slots = json.load(file)["slots"]

# Load YOLO
model = YOLO("yolo11n.pt")

# Detect vehicles
results = model(image, imgsz=1280, conf=0.15)

vehicles = []

for result in results:
    for box in result.boxes:
        class_id = int(box.cls[0])

        if class_id in [2, 3, 5, 7]:
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            vehicles.append((center_x, center_y))


# Check every slot
for slot in slots:

    occupied = False

    for vx, vy in vehicles:

        if (
            slot["x1"] <= vx <= slot["x2"]
            and
            slot["y1"] <= vy <= slot["y2"]
        ):
            occupied = True
            break

    if occupied:
        status = "OCCUPIED"
    else:
        status = "FREE"

    update_database(slot["id"], status)

    print(f"{slot['id']}: {status}")


print()
print("Database updated successfully!")