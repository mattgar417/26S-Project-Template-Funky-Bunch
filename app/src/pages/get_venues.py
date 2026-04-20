import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Venue Directory")

location_filter = st.text_input("Filter by location (optional)")
capacity_filter = st.number_input("Minimum capacity (optional)", min_value=0, value=0)

params = {}
if location_filter:
    params["location"] = location_filter
if capacity_filter > 0:
    params["min_capacity"] = capacity_filter

try:
    response = requests.get("http://web-api:4000/venue/venues", params=params, timeout=5)
    if response.status_code == 200:
        venues = response.json()
    else:
        st.error(f"Failed to fetch venue data (status {response.status_code})")
        venues = []
except Exception as e:
    st.error(f"Error connecting to API: {e}")
    venues = []

if venues:
    st.write(f"Found **{len(venues)}** venue(s)")
    for venue in venues:
        with st.expander(f"{venue.get('Name', 'Unnamed')} — {venue.get('Location', '')}"):
            st.write(f"**Capacity:** {venue.get('Capacity', 'N/A')}")
            st.write(f"**Location:** {venue.get('Location', 'N/A')}")
            st.write(f"**Owner:** {venue.get('OwnerFirstName', '')} {venue.get('OwnerLastName', '')}")
else:
    st.info("No venues found.")

st.divider()
if st.button("Make a venue request", type="primary", use_container_width=True):
    st.switch_page("pages/post_venue_request.py")
