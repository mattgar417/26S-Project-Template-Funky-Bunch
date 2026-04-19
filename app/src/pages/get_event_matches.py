import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Attendees that Match with Your Event")

API_URL = f"http://api:4000/events/{st.session_state.event_id}/"

response = requests.get(API_URL)

if response.status_code == 200:
    matches = response.json()

    if not matches:
        st.info("No attendees have matched with your events yet.")
        st.stop()

    events = sorted(list(set(match["Event_Name"] for match in matches)))
    skills = sorted(list(set(match["Skill"] for match in matches)))
    statuses = sorted(list(set(match["Status"] for match in matches)))

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_event = st.selectbox("Filter by Event", ["All"] + events)
    with col2:
        selected_skill = st.selectbox("Filter by Skill", ["All"] + skills)
    with col3:
        selected_status = st.selectbox("Filter by Status", ["All"] + statuses)

    filtered_matches = matches
    if selected_event != "All":
        filtered_matches = [m for m in filtered_matches if m["Event_Name"] == selected_event]
    if selected_skill != "All":
        filtered_matches = [m for m in filtered_matches if m["Skill"] == selected_skill]
    if selected_status != "All":
        filtered_matches = [m for m in filtered_matches if m["Status"] == selected_status]

    st.write(f"Found **{len(filtered_matches)}** matched attendee(s)")

    for match in filtered_matches:
        with st.expander(f"{match['Attendee_Name']} → {match['Event_Name']}"):
            info_col, event_col = st.columns(2)

            with info_col:
                st.write("**Attendee Information**")
                st.write(f"**Name:** {match['Attendee_Name']}")
                st.write(f"**Email:** {match['Email']}")
                st.write(f"**Skill:** {match['Skill']}")

            with event_col:
                st.write("**Event Information**")
                st.write(f"**Event:** {match['Event_Name']}")
                st.write(f"**Date:** {match['Event_Date']}")
                st.write(f"**Status:** {match['Status']}")

else:
    st.error("Failed to fetch matched attendees from the API.")