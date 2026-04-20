import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Delete Event")

organizer_id = st.session_state.get('user_id', 1)
BASE_URL = "http://web-api:4000/event/events"

@st.dialog("Event Deleted")
def show_success_dialog(event_name):
    st.markdown(f"### **{event_name}** has been permanently deleted.")
    if st.button("Close", use_container_width=True):
        st.session_state.pop('fetched_event', None)
        st.rerun()

# Fetch organizer's events for selection
events_res = requests.get(f"http://web-api:4000/organizer/organizers/{organizer_id}/events", timeout=5)
if events_res.status_code == 200:
    events = events_res.json()
else:
    events = []

if not events:
    st.info("You have no events to delete.")
    st.stop()

event_options = {f"{e['Name']} (ID {e['EventID']})": e['EventID'] for e in events}
selected_label = st.selectbox("Select an event to delete", list(event_options.keys()))
event_id = event_options[selected_label]

fetch_clicked = st.button("Load Event Details")

if fetch_clicked:
    try:
        response = requests.get(f"{BASE_URL}/{event_id}", timeout=5)
        if response.status_code == 200:
            st.session_state['fetched_event'] = response.json()
        else:
            st.error("Event not found.")
            st.session_state.pop('fetched_event', None)
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {e}")

event = st.session_state.get("fetched_event")

if event:
    st.subheader("Event Details")
    st.write(f"**Name:** {event.get('Name', 'N/A')}")
    st.write(f"**Date:** {event.get('Date', 'N/A')}")
    st.write(f"**Location:** {event.get('Location', 'N/A')}")
    st.write(f"**Description:** {event.get('Description', 'N/A')}")
    st.write(f"**Size:** {event.get('Size', 'N/A')}")
    st.write(f"**Category:** {event.get('Category', 'N/A')}")

    st.warning("This action is permanent and cannot be undone.")
    confirm = st.checkbox("I understand this event will be permanently deleted.")

    if st.button("Delete Event", disabled=not confirm, type="primary"):
        try:
            response = requests.delete(f"{BASE_URL}/{event_id}", timeout=5)
            if response.status_code == 200:
                name = event.get("Name", "Event")
                st.session_state.pop('fetched_event', None)
                show_success_dialog(name)
            else:
                st.error(f"Failed to delete event: {response.json().get('error', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the API: {e}")

if st.button("Return to Organizer Home"):
    st.switch_page("pages/organizer.py")
