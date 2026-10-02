import sqlite3
import json
import math
import streamlit as st
import pandas as pd

from backend.analytics import get_peak_hours
from backend.predictor import predict_availability
from backend.alert_manager import check_overstay
from backend.ticket_manager import create_ticket
from backend.parking_rules import check_parking_permission

DATABASE = "parking.db"
SLOTS_FILE = "config/slots_webcam.json"

st.set_page_config(
    page_title="AI Smart Parking",
    page_icon="🅿️",
    layout="wide"
)


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

def get_connection():
    return sqlite3.connect(DATABASE)


def get_slot_data():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            slot_name,
            status,
            slot_type,
            reserved_for
        FROM parking_slots
        ORDER BY slot_name
        """
    ).fetchall()

    connection.close()
    return rows


def get_active_alerts():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            slot_name,
            alert_type,
            message,
            created_at
        FROM alerts
        WHERE resolved = 0
        ORDER BY created_at DESC
        """
    ).fetchall()

    connection.close()
    return rows


# --------------------------------------------------
# LED SIMULATOR
# --------------------------------------------------

def get_led_status(status, slot_type):

    if status == "OCCUPIED":
        return "🔴 RED"

    if slot_type == "RESERVED":
        return "🔵 BLUE"

    if slot_type == "ACCESSIBLE":
        return "🩵 CYAN"

    return "🟢 GREEN"


# --------------------------------------------------
# SLOT COORDINATES
# --------------------------------------------------

def get_slot_coordinates():

    try:
        with open(SLOTS_FILE, "r") as file:
            data = json.load(file)

        coordinates = {}

        for slot in data["slots"]:

            center_x = (slot["x1"] + slot["x2"]) / 2
            center_y = (slot["y1"] + slot["y2"]) / 2

            coordinates[slot["id"]] = (center_x, center_y)

        return coordinates

    except Exception:
        return {}


# --------------------------------------------------
# NEAREST SLOT GUIDANCE
# --------------------------------------------------

def find_nearest_slot(authorization):

    connection = get_connection()

    free_slots = connection.execute(
        """
        SELECT
            slot_name,
            slot_type,
            reserved_for
        FROM parking_slots
        WHERE status = 'FREE'
        """
    ).fetchall()

    connection.close()

    coordinates = get_slot_coordinates()

    # Simulated entrance position
    entrance_x = 320
    entrance_y = 20

    candidates = []

    for slot_name, slot_type, reserved_for in free_slots:

        # Normal slots are available to everyone.
        if slot_type == "NORMAL":
            allowed = True

        # Reserved/accessibility slots require authorization.
        elif authorization == reserved_for:
            allowed = True

        else:
            allowed = False

        if not allowed:
            continue

        if slot_name not in coordinates:
            continue

        slot_x, slot_y = coordinates[slot_name]

        distance = math.sqrt(
            (slot_x - entrance_x) ** 2 +
            (slot_y - entrance_y) ** 2
        )

        candidates.append(
            (
                distance,
                slot_name,
                slot_type
            )
        )

    if not candidates:
        return None

    candidates.sort()

    distance, slot_name, slot_type = candidates[0]

    return {
        "slot": slot_name,
        "slot_type": slot_type,
        "distance": round(distance, 2)
    }


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("🅿️ AI Smart Parking Management System")

st.caption(
    "AI-based parking occupancy, intelligent guidance, alerts, "
    "analytics and smart parking management"
)

st.divider()


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

slots = get_slot_data()
active_alerts = get_active_alerts()

total_slots = len(slots)

occupied_slots = sum(
    1 for slot in slots
    if slot[1] == "OCCUPIED"
)

free_slots = total_slots - occupied_slots

alert_count = len(active_alerts)


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Slots", total_slots)

with col2:
    st.metric("Free Slots", free_slots)

with col3:
    st.metric("Occupied Slots", occupied_slots)

with col4:
    st.metric("Active Alerts", alert_count)


st.divider()


# --------------------------------------------------
# PARKING SLOT STATUS
# --------------------------------------------------

st.subheader("🅿️ Live Parking Slots")

columns = st.columns(3)

for index, slot in enumerate(slots):

    slot_name = slot[0]
    status = slot[1]
    slot_type = slot[2]
    reserved_for = slot[3]

    if status == "OCCUPIED":

        indicator = "🔴"
        status_text = "OCCUPIED"

    elif slot_type == "RESERVED":

        indicator = "🔵"
        status_text = "FREE - RESERVED"

    elif slot_type == "ACCESSIBLE":

        indicator = "♿"
        status_text = "FREE - ACCESSIBLE"

    else:

        indicator = "🟢"
        status_text = "FREE"

    with columns[index % 3]:

        st.markdown(
            f"""
            ### {indicator} {slot_name}

            **Status:** {status_text}

            **Type:** {slot_type}

            **Reserved For:** {reserved_for if reserved_for else "None"}
            """
        )

        st.divider()


# --------------------------------------------------
# SMART LED STATUS
# --------------------------------------------------

st.subheader("🚦 Smart LED Indicator")

st.caption(
    "Software simulation of the parking-slot LED indicator system."
)

led_columns = st.columns(3)

for index, slot in enumerate(slots):

    slot_name = slot[0]
    status = slot[1]
    slot_type = slot[2]

    led_status = get_led_status(
        status,
        slot_type
    )

    with led_columns[index % 3]:

        st.markdown(
            f"""
            ### {slot_name}

            **LED:** {led_status}

            **Parking Status:** {status}

            **Slot Type:** {slot_type}
            """
        )


st.divider()


# --------------------------------------------------
# INTELLIGENT NEAREST-SLOT GUIDANCE
# --------------------------------------------------

st.subheader("🧭 Intelligent Nearest-Slot Guidance")

st.write(
    "Select the driver's authorization type. "
    "The system will recommend the nearest suitable free slot."
)

authorization = st.selectbox(
    "Driver Authorization",
    [
        "NORMAL",
        "VIP",
        "ACCESSIBILITY"
    ]
)

if st.button("🔎 Find Nearest Suitable Slot"):

    result = find_nearest_slot(authorization)

    if result:

        st.success(
            f"🅿️ Recommended Slot: **{result['slot']}**"
        )

        guidance_col1, guidance_col2 = st.columns(2)

        with guidance_col1:
            st.metric(
                "Slot Type",
                result["slot_type"]
            )

        with guidance_col2:
            st.metric(
                "Distance from Entrance",
                f"{result['distance']} units"
            )

        st.info(
            f"Authorization: **{authorization}**\n\n"
            f"The system selected **{result['slot']}** "
            f"from the currently available suitable slots."
        )

    else:

        st.warning(
            "⚠️ No suitable free parking slot is currently available "
            "for this authorization type."
        )


st.divider()

# --------------------------------------------------
# PEAK-HOUR ANALYTICS
# --------------------------------------------------

st.subheader("📊 Parking Peak-Hour Analytics")

st.write(
    "Analyze parking entry history to identify the "
    "busiest parking hours."
)

hour_counts = get_peak_hours()

if not hour_counts:

    st.info(
        "📊 No parking history is available yet. "
        "Peak-hour analytics will appear after the "
        "system records parking entries."
    )

else:

    chart_data = pd.DataFrame(
        {
            "Hour": [
                f"{hour:02d}:00"
                for hour in sorted(hour_counts)
            ],
            "Entries": [
                hour_counts[hour]
                for hour in sorted(hour_counts)
            ]
        }
    )

    chart_data = chart_data.set_index("Hour")

    st.bar_chart(chart_data)

    peak_hour = max(
        hour_counts,
        key=hour_counts.get
    )

    st.success(
        f"🔥 Peak parking hour: "
        f"{peak_hour:02d}:00 - {peak_hour:02d}:59 "
        f"with {hour_counts[peak_hour]} entries."
    )

st.divider()

# --------------------------------------------------
# PREDICTIVE PARKING AVAILABILITY
# --------------------------------------------------

st.subheader("🔮 Predictive Parking Availability")

st.write(
    "Estimate the number of free parking slots for a selected hour "
    "using historical parking records."
)

prediction_hour = st.slider(
    "Select Target Hour",
    min_value=0,
    max_value=23,
    value=18,
    step=1
)

if st.button("🔮 Predict Free Slots"):

    predicted_free = predict_availability(prediction_hour)

    if predicted_free is None:

        st.info(
            "Not enough parking history is available yet. "
            "Predictions will become available after parking "
            "activity is recorded."
        )

    else:

        st.success(
            f"Predicted free slots at "
            f"{prediction_hour:02d}:00: {predicted_free}"
        )

st.divider()

# --------------------------------------------------
# SYSTEM INFORMATION
# --------------------------------------------------

st.subheader("⚙️ System Information")

info1, info2, info3 = st.columns(3)

with info1:
    st.info(
        "🤖 **AI Detection**\n\n"
        "YOLO vehicle detection is connected "
        "to the parking system."
    )

with info2:
    st.info(
        "💾 **Database**\n\n"
        "SQLite database stores parking slots, "
        "records and alerts."
    )

with info3:
    st.info(
        "🧭 **Smart Guidance**\n\n"
        "The system identifies a suitable free "
        "slot based on distance and authorization."
    )

# --------------------------------------------------
# PARKING RULES & ACCESS CONTROL
# --------------------------------------------------

st.subheader("♿ Reserved & Accessibility Parking Enforcement")

st.write(
    "Check whether a driver is authorized to use a "
    "reserved or accessibility parking slot."
)

rule_slot = st.selectbox(
    "Select Parking Slot",
    [slot[0] for slot in slots],
    key="rule_slot"
)

rule_authorization = st.selectbox(
    "Driver Authorization",
    [
        "NORMAL",
        "VIP",
        "ACCESSIBILITY"
    ],
    key="rule_authorization"
)

if st.button("🔐 Check Parking Permission"):

    allowed, message = check_parking_permission(
        rule_slot,
        rule_authorization
    )

    if allowed:

        st.success(
            f"✅ ALLOWED\n\n{message}"
        )

    else:

        st.error(
            f"🚨 ACCESS ALERT\n\n{message}"
        )

st.divider()

# --------------------------------------------------
# PARKING TICKET + QR CODE
# --------------------------------------------------

st.subheader("🎫 Parking Ticket & QR Code")

st.write(
    "Create a digital parking ticket with a QR code "
    "for the selected parking slot."
)

ticket_slot = st.selectbox(
    "Select Parking Slot",
    [slot[0] for slot in slots],
    key="ticket_slot"
)

ticket_plate = st.text_input(
    "Vehicle Plate Number",
    value="UNKNOWN",
    key="ticket_plate"
)

ticket_vehicle_type = st.selectbox(
    "Vehicle Type",
    [
        "car",
        "motorcycle",
        "bus",
        "truck"
    ],
    key="ticket_vehicle_type"
)

if st.button("🎫 Generate Parking Ticket"):

    ticket_id = create_ticket(
        ticket_slot,
        ticket_plate,
        ticket_vehicle_type
    )

    st.success(
        f"Parking ticket created successfully: {ticket_id}"
    )

    ticket_file = f"data/tickets/{ticket_id}.png"

    try:

        st.image(
            ticket_file,
            caption=f"QR Code - {ticket_id}",
            width=250
        )

        st.info(
            f"Ticket ID: {ticket_id}\n\n"
            f"Slot: {ticket_slot}\n\n"
            f"Vehicle: {ticket_vehicle_type}\n\n"
            f"Plate: {ticket_plate}"
        )

    except Exception:

        st.warning(
            "Ticket was created, but the QR image "
            "could not be displayed."
        )

st.divider()


# --------------------------------------------------
# OVERSTAY CHECK
# --------------------------------------------------

st.subheader("⏱️ Overstay Monitoring")

st.write(
    "Check active parking records for vehicles that have "
    "exceeded the configured parking time limit."
)

if st.button("🔍 Check for Overstay Vehicles"):

    check_overstay()

    st.success(
        "✅ Overstay check completed. "
        "Refresh the dashboard to view any new alerts."
    )



# --------------------------------------------------
# ALERTS
# --------------------------------------------------

st.subheader("🚨 Active Parking Alerts")

if not active_alerts:

    st.success("✅ No active parking alerts.")

else:

    for slot_name, alert_type, message, created_at in active_alerts:

        st.warning(
            f"**{alert_type} — {slot_name}**\n\n"
            f"{message}\n\n"
            f"Time: {created_at}"
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "AI Smart Parking Management System | "
    "YOLO + OpenCV + SQLite + Streamlit"
)