\# AI-Based Smart Parking Management and Intelligent Slot Guidance System



\## 1. Project Overview



This project is a software-based smart parking management system that uses computer vision, OCR, a database, and a web dashboard to monitor and manage parking spaces.



The current prototype is configured for \*\*3 webcam-based parking slots\*\*:



\* S1 — VIP Reserved

\* S2 — Accessibility Reserved

\* S3 — Normal Parking



The system can detect vehicles from a webcam, determine vehicle type, monitor parking occupancy, recognize number plates when visible, record entry and exit times, generate QR parking tickets, enforce parking rules, provide nearest-slot guidance, and display analytics.



\---



\## 2. Main Features



\* Real-time vehicle detection using YOLO

\* Automatic vehicle-type detection

\* Webcam-based parking-slot monitoring

\* Stable occupancy detection using consecutive-frame confirmation

\* Automatic parking entry and exit recording

\* Number plate recognition using EasyOCR

\* SQLite database

\* Persistent application logging

\* Overstay detection and alerts

\* VIP/reserved parking enforcement

\* Accessibility parking enforcement

\* Nearest available slot guidance

\* Simulated LED status system

\* QR-based parking ticket generation

\* Peak-hour analytics

\* Historical availability estimation

\* Streamlit web dashboard

\* Dynamic webcam slot calibration



\---



\## 3. Technology Stack



\### Programming Language



\* Python 3.11



\### Computer Vision



\* OpenCV

\* Ultralytics YOLO



\### OCR



\* EasyOCR



\### Database



\* SQLite3



\### Dashboard



\* Streamlit



\### Data Analysis



\* Pandas

\* Matplotlib



\### QR Generation



\* qrcode



\### Logging



\* Python logging



\---



\## 4. System Architecture



```text

&#x20;                   WEBCAM

&#x20;                      |

&#x20;                      v

&#x20;            +-------------------+

&#x20;            | YOLO Vehicle      |

&#x20;            | Detection          |

&#x20;            +---------+---------+

&#x20;                      |

&#x20;            +---------+---------+

&#x20;            |                   |

&#x20;            v                   v

&#x20;     Vehicle Type        Slot Occupancy

&#x20;      Detection            Detection

&#x20;            |                   |

&#x20;            +---------+---------+

&#x20;                      |

&#x20;                      v

&#x20;             Vehicle Region

&#x20;                      |

&#x20;                      v

&#x20;             EasyOCR Plate

&#x20;             Recognition

&#x20;                      |

&#x20;                      v

&#x20;         +-----------------------+

&#x20;         | Parking Management    |

&#x20;         | Engine                |

&#x20;         +-----------+-----------+

&#x20;                     |

&#x20;      +--------------+--------------+

&#x20;      |              |              |

&#x20;      v              v              v

&#x20;   SQLite         Alerts        Parking Rules

&#x20;   Database

&#x20;      |

&#x20;      +--------------+--------------+

&#x20;                     |

&#x20;         +-----------+-----------+

&#x20;         |                       |

&#x20;         v                       v

&#x20;     Analytics              Slot Guidance

&#x20;         |                       |

&#x20;         +-----------+-----------+

&#x20;                     |

&#x20;                     v

&#x20;            Streamlit Dashboard

```



\---



\## 5. Current Parking Configuration



The prototype currently uses three calibrated webcam parking slots.



| Slot | Type       | Authorization |

| ---- | ---------- | ------------- |

| S1   | Reserved   | VIP           |

| S2   | Accessible | ACCESSIBILITY |

| S3   | Normal     | NORMAL        |



The active webcam slot coordinates are stored in:



```text

config/slots\_webcam.json

```



Current slot configuration:



```text

S1 → VIP Reserved

S2 → Accessibility Reserved

S3 → Normal Parking

```



\---



\## 6. Project Structure



```text

SMART\_PARKING\_AI/

│

├── app.py

├── requirements.txt

├── README.md

├── parking.db

├── yolo11n.pt

│

├── backend/

│   ├── database.py

│   ├── parking\_manager.py

│   ├── parking\_records.py

│   ├── parking\_engine.py

│   ├── setup\_slots.py

│   ├── update\_status.py

│   ├── ticket\_manager.py

│   ├── alert\_manager.py

│   ├── parking\_rules.py

│   ├── guidance.py

│   ├── led\_simulator.py

│   ├── analytics.py

│   └── predictor.py

│

├── config/

│   ├── settings.py

│   ├── slots.json

│   ├── slots\_webcam.json

│   └── slots\_backup.json

│

├── vision/

│   ├── detector.py

│   ├── slot\_detector.py

│   ├── calibration.py

│   ├── plate\_reader.py

│   └── video\_processor.py

│

├── utils/

│   ├── logger.py

│   ├── qr\_generator.py

│   └── helpers.py

│

├── data/

│   ├── sample\_images/

│   └── tickets/

│

├── logs/

│   └── parking.log

│

└── models/

```



\---



\## 7. Installation



Create the Python virtual environment:



```bat

py -3.11 -m venv venv

```



Activate it:



```bat

venv\\Scripts\\activate

```



Install the project dependencies:



```bat

pip install -r requirements.txt

```



\---



\## 8. Running the Dashboard



Start the Streamlit dashboard:



```bat

streamlit run app.py

```



The dashboard provides access to the main parking-management features.



\---



\## 9. Running Live AI Parking Detection



Run the webcam-based AI detection system:



```bat

python vision\\video\_processor.py

```



The system uses the webcam to:



1\. Detect vehicles.

2\. Identify vehicle types.

3\. Check parking-slot occupancy.

4\. Record vehicle entry.

5\. Attempt number-plate recognition.

6\. Record vehicle exit.

7\. Check overstay conditions.

8\. Update the parking database.

9\. Display the parking status.



Press \*\*Q\*\* to stop the live detection window.



\---



\## 10. Webcam Slot Calibration



The project includes a dynamic slot-calibration system.



Run:



```bat

python vision\\calibration.py

```



The calibration interface allows parking-slot coordinates to be selected directly from the webcam image.



Controls:



```text

S = Save

R = Reset

Q = Quit

```



The calibrated slots are saved to:



```text

config/slots\_webcam.json

```



This makes the system easier to adapt to a different camera position or parking layout without manually calculating screen coordinates.



\---



\## 11. Vehicle Detection



The system uses the Ultralytics YOLO model:



```text

yolo11n.pt

```



The detector identifies supported vehicle classes including:



\* Car

\* Motorcycle

\* Bus

\* Truck



The detected vehicle type is stored with the parking record.



\---



\## 12. Parking Slot Occupancy



The webcam image is divided into calibrated parking-slot regions.



For each detected vehicle, the system checks whether the vehicle center is inside a parking slot.



To reduce false status changes, the system uses consecutive-frame confirmation before changing a slot between:



```text

FREE

OCCUPIED

```



The current prototype contains three active webcam slots.



\---



\## 13. Number Plate Recognition



Number-plate recognition uses \*\*EasyOCR\*\*.



The detected vehicle region is passed to the OCR system.



The OCR pipeline:



```text

Vehicle Detection

&#x20;      |

&#x20;      v

Vehicle Region

&#x20;      |

&#x20;      v

Image Preprocessing

&#x20;      |

&#x20;      v

EasyOCR

&#x20;      |

&#x20;      v

Text Cleaning

&#x20;      |

&#x20;      v

Plate Number

```



If a readable plate cannot be obtained, the system stores:



```text

UNKNOWN

```



OCR performance depends on:



\* Camera resolution

\* Lighting

\* Vehicle angle

\* Plate visibility

\* Image quality



\---



\## 14. Database



The project uses SQLite3.



The database file is:



```text

parking.db

```



The database stores information including:



\* Parking slots

\* Slot status

\* Slot type

\* Authorization requirements

\* Parking records

\* Vehicle type

\* Number plate

\* Entry time

\* Exit time

\* Parking alerts



The database allows the system to maintain parking history without requiring an external database server.



\---



\## 15. Parking Rules and Authorization



The prototype contains three slot types.



\### S1 — VIP Reserved



Authorization:



```text

VIP

```



Normal vehicles are not authorized to use this slot.



\### S2 — Accessibility Reserved



Authorization:



```text

ACCESSIBILITY

```



Only vehicles with the appropriate accessibility authorization are permitted.



\### S3 — Normal Parking



Authorization:



```text

NORMAL

```



Normal parking is permitted.



The system generates an alert when an unauthorized parking attempt is detected.



\---



\## 16. Intelligent Nearest-Slot Guidance



The system includes a software-based parking guidance module.



It considers:



\* Available slots

\* Slot type

\* Driver authorization

\* Slot location

\* Distance from the entrance



For example, a normal driver will normally be directed toward an available normal slot rather than a restricted VIP or accessibility slot.



The current prototype uses the calibrated webcam slot coordinates to estimate slot distance.



\---



\## 17. Smart LED Simulation



The project includes a software simulation of parking-slot LED indicators.



The simulated states are:



| LED   | Meaning               |

| ----- | --------------------- |

| GREEN | Normal slot available |

| BLUE  | VIP reserved slot     |

| CYAN  | Accessibility slot    |

| RED   | Occupied slot         |



This feature demonstrates how the software could communicate parking status to physical LEDs in a future hardware version.



No physical LED hardware is required for the current prototype.



\---



\## 18. QR Parking Ticket



The project can generate a virtual QR parking ticket.



A ticket contains information such as:



```text

Ticket ID

Slot

Number Plate

Entry Time

```



QR ticket files are stored in:



```text

data/tickets/

```



The ticket-generation workflow is:



```text

```



