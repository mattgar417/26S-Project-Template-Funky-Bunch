import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Venue Directory")

API_URL = ""

response = requests.get(API_URL)
if response.status_code == 200:
        venues = response.json()

        filtered_response = requests.get(API_URL)
        if filtered_response.status_code == 200:
            filtered_venues = filtered_response.json()

            # Display results count
            st.write(f"Found {len(filtered_venues)} venues")

            # Create expandable rows for each NGO
            for venue in filtered_venues:
                    st.write(f"**Name:** {venue['Name']}")
                    st.write(f"**Capacity:** {venue['Capacity']}")
                    st.write(f"**Location:** {venue['Location']}")
                    st.write(f"**Owner:** {venue['OwnerFirstName']}{venue['OwnerLastName']}")

else:
    st.error("Failed to fetch venue data from the API")