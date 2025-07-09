# frontend.py
import streamlit as st
import requests
from datetime import datetime, timedelta

# ✅ Removed /api/v1 since endpoints are now directly under root
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Hall Booking System", layout="centered")
st.title("🏛️ Hall Booking System")

# Get available time slots
def fetch_slots():
    try:
        response = requests.get(f"{API_URL}/available-slots")
        if response.status_code == 200 and "available_slots" in response.json():
            return response.json()["available_slots"]
        else:
            st.error("No available slots or failed to fetch them.")
            return []
    except Exception as e:
        st.error(f"Error fetching slots: {e}")
        return []

# Register a new user
def register_user(username, email, password):
    payload = {
        "username": username,
        "email": email,
        "password": password
    }
    try:
        response = requests.post(f"{API_URL}/users/", json=payload)
        return response
    except Exception as e:
        st.error(f"Error during registration: {e}")
        return None

# Book a slot
def book_slot(start_time, user_id):
    start_dt = datetime.fromisoformat(start_time)
    end_dt = start_dt + timedelta(hours=1)
    payload = {
        "start_time": start_dt.isoformat(),
        "end_time": end_dt.isoformat()
    }
    try:
        response = requests.post(f"{API_URL}/bookings/?user_id={user_id}", json=payload)
        return response
    except Exception as e:
        st.error(f"Error during booking: {e}")
        return None

# Sidebar for user registration
st.sidebar.header("🔐 Register User")
username = st.sidebar.text_input("Username")
email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Register"):
    res = register_user(username, email, password)
    if res and res.status_code == 200:
        st.sidebar.success("User registered successfully!")
    else:
        st.sidebar.error("Registration failed. Try a different username/email.")

st.header("📅 Book a Slot")

slots = fetch_slots()
if slots:
    selected_slot = st.selectbox("Select an available time slot", slots)
    user_id = st.number_input("Enter your user ID", min_value=1, step=1)
    if st.button("Book Slot"):
        res = book_slot(selected_slot, user_id)
        if res and res.status_code == 200:
            st.success("Slot booked successfully!")
        else:
            try:
                st.error(f"Failed to book slot: {res.json().get('detail', 'Unknown error')}")
            except:
                st.error("Failed to book slot.")
