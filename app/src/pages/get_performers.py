import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Performer Directory")

BASE_URL = "http://web-api:4000/performer/performers"

genre_filter = st.text_input("Filter by Genre (optional)")

params = {}
if genre_filter:
    params["genre"] = genre_filter

response = requests.get(BASE_URL, params=params)
if response.status_code == 200:
    performers = response.json()

    st.write(f"Found {len(performers)} performers")

    for performer in performers:
        with st.expander(f"**{performer['FName']} {performer['LName']}** — {performer['Genre']}"):
            st.write(f"**Genre:** {performer['Genre']}")
            st.write(f"**Biography:** {performer['Bio']}")
            st.write(f"**Media Links:** {performer['MediaLinks']}")
            st.write(f"**Availability:** {performer['Availability']}")
            st.write(f"**Views:** {performer['Views']}")
            st.write(f"**Ranking:** {performer['Ranking']}")
            if st.button("Book this Performer", key=f"book_{performer['PerformerID']}"):
                st.session_state['selected_performer_id'] = performer['PerformerID']
                st.session_state['selected_performer_name'] = f"{performer['FName']} {performer['LName']}"
                st.switch_page("pages/request_performer_booking.py")
else:
    st.error("Failed to fetch performers from the API")
