import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Add New Request")

organizer_id = st.session_state.get('user_id', 1)

# Load venues for the dropdown
try:
    venues_res = requests.get("http://web-api:4000/venue/venues", timeout=5)
    venues = venues_res.json() if venues_res.status_code == 200 else []
except Exception:
    venues = []

if not venues:
    st.error("Could not load venues. Please try again later.")
    st.stop()

venue_options = {f"{v['Name']} — {v['Location']} (cap. {v['Capacity']})": v['VenueID'] for v in venues}

with st.form("post_venue_request_form"):
    st.subheader("Request Information")
    request_name = st.text_input("Request Name *")
    selected_venue_label = st.selectbox("Select Venue *", list(venue_options.keys()))

    submitted = st.form_submit_button("Submit Request", type="primary")

    if submitted:
        if not request_name:
            st.error("Please enter a request name.")
        else:
            venue_id = venue_options[selected_venue_label]
            payload = {"request_name": request_name, "venue_id": venue_id}
            try:
                response = requests.post(
                    f"http://web-api:4000/organizer/organizers/{organizer_id}/venue-requests",
                    json=payload,
                    timeout=5
                )
                if response.status_code == 201:
                    st.success(f"Request **{request_name}** submitted successfully!")
                else:
                    st.error(f"Failed to submit request: {response.json().get('error', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API: {e}")

if st.button("Return to Venue Directory"):
    st.switch_page("pages/get_venues.py")
