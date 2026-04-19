import streamlist as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("Browse Events")

API_BASE = "http://web-api:4000"
attendee_id = st.session_state.get("attendee_id", 1)

col1, col2, col3 = st.columns(3)
with col1:
    category = st.text_input("Category (e.g. Music, Food)")
with col2:
    location = st.text_input("Location contains")
with col3:
    date = st.date_input("Date", value=None)

params = []
if category:
    params["category"] = category
if location:
    params["location"] = location
if date:
    params["date"] = date.isoformat()

try:
    response = requests.get(f"{API_BASE}/event/events", params=params)
    if response.status_code == 200:
        events = response.json()
        st.write(f"Found {len(events)} events")

        for event in events:
            with st.expander(f"{event['Name']} - {event['Date']}"):
                st.write(f"**Category:** {event['Category']}")
                st.write(f"**Location:** {event['Location']}")
                st.write(f"**Description:** {event['Description']}")
                st.write(f"**Size:** {event['Size']}")

                b1, b2 = st.columns(2)
                with b1:
                    if st.button("RSVP", key=f"rsvp_{event['EventID']}"):
                        r = requests.post(f"{API_BASE}/attendee/attendees/{attendee_id}/rsvps", json={"EventID": event["EventID"], "status": "Going"},
                        )
                        