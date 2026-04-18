import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Performer Directory")

API_URL = ""

response = requests.get(API_URL)
if response.status_code == 200:
        performers = response.json()

        filtered_response = requests.get(API_URL)
        if filtered_response.status_code == 200:
            filtered_performers = filtered_response.json()

            # Display results count
            st.write(f"Found {len(filtered_performers)} performers")

            # Create expandable rows for each NGO
            for performer in filtered_performers:
                    st.write(f"**Name:** {performer['FName']} {performer['LName']}")
                    st.write(f"**Genre:** {performer['Genre']}")
                    st.write(f"**Biography:** {performer['Bio']}")
                    st.write(f"**Media Links:** {performer['MediaLinks']}")
                    st.write(f"**Availability:** {performer['Genre']}")
                    st.write(f"**Views:** {performer['Views']}")
                    st.write(f"**Ranking:** {performer['Ranking']}")

else:
    st.error("Failed to fetch venue data from the API")