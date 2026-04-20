import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Update Event")

organizer_id = st.session_state.get('user_id', 1)
BASE_URL = "http://web-api:4000/event/events"

# Fetch organizer's events for selection
events_res = requests.get(f"http://web-api:4000/organizer/organizers/{organizer_id}/events", timeout=5)
if events_res.status_code == 200:
    events = events_res.json()
else:
    events = []

if not events:
    st.info("You have no events to update.")
    st.stop()

event_options = {f"{e['Name']} (ID {e['EventID']})": e['EventID'] for e in events}
selected_label = st.selectbox("Select an event to update", list(event_options.keys()))
event_id = event_options[selected_label]

# Load current event data
if st.button("Load Event Details"):
    try:
        res = requests.get(f"{BASE_URL}/{event_id}", timeout=5)
        if res.status_code == 200:
            st.session_state['edit_event'] = res.json()
            st.success("Event loaded. Edit the fields below.")
        else:
            st.error("Could not load event details.")
    except Exception as e:
        st.error(f"API error: {e}")

event = st.session_state.get('edit_event', {})

with st.form("update_event_form"):
    st.subheader("Edit Event Details")
    name = st.text_input("Name", value=event.get('Name', ''))
    date = st.text_input("Date (YYYY-MM-DD HH:MM:SS)", value=str(event.get('Date', '')))
    location = st.text_input("Location", value=event.get('Location', ''))
    description = st.text_area("Description", value=event.get('Description', ''))
    size = st.number_input("Size", min_value=1, value=int(event.get('Size', 1)))
    category = st.text_input("Category", value=event.get('Category', ''))

    submitted = st.form_submit_button("Save Changes")

    if submitted:
        if not all([name, date, location, description, category]):
            st.error("Please fill in all required fields.")
        else:
            payload = {
                "Name": name,
                "Date": date,
                "Location": location,
                "Description": description,
                "Size": size,
                "Category": category
            }
            try:
                response = requests.put(f"{BASE_URL}/{event_id}", json=payload, timeout=5)
                if response.status_code == 200:
                    st.success(f"Event **{name}** updated successfully!")
                    st.session_state.pop('edit_event', None)
                else:
                    st.error(f"Failed to update event: {response.json().get('error', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API: {e}")

if st.button("Return to Organizer Home"):
    st.switch_page("pages/organizer.py")
