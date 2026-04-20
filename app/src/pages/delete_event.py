import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Delete Event")

@st.dialog("Success")
def show_success_dialog(event_name):
    st.markdown(f"### {event_name} has been successfully deleted!")

    if st.button("Close", use_container_width=True):
        st.session_state.show_success_modal = False
        st.session_state.success_event_name = ""
        st.rerun()

API_URL = f"http://api:4000/events/{st.session_state.event_id}"

event_id = st.number_input("Enter Event ID to Delete", min_value=1, step=1)
fetch_clicked = st.button("Fetch Event Details")

if fetch_clicked:
    try:
        response = requests.get(f"{API_URL}/{event_id}")
        if response.status_code == 200:
            st.session_state.fetched_event = response.json()
            st.success("Event found! Review the details below before deleting.")
        else:
            st.error("Event not found. Please check the ID and try again.")
            st.session_state.fetched_event = None
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")
        st.session_state.fetched_event = None

event = st.session_state.get("fetched_event")

# --- Display event details for review ---
if event:
    st.subheader("Event Details")
    st.write(f"**Name:** {event.get('Name', 'N/A')}")
    st.write(f"**Date:** {event.get('Date', 'N/A')}")
    st.write(f"**Location:** {event.get('Location', 'N/A')}")
    st.write(f"**Description:** {event.get('Description', 'N/A')}")
    st.write(f"**Size:** {event.get('Size', 'N/A')}")
    st.write(f"**Category:** {event.get('Category', 'N/A')}")

    st.warning("This action is permanent and cannot be undone.")

    # Two-step confirmation to prevent accidental deletion
    confirm = st.checkbox("I understand this event will be permanently deleted.")

    if st.button("Delete Event", disabled=not confirm, type="primary"):
        try:
            response = requests.delete(f"{API_URL}/{event_id}")

            if response.status_code == 200:
                st.session_state.show_success_modal = True
                st.session_state.success_event_name = event.get("Name", "Event")
                st.session_state.fetched_event = None
                st.rerun()
            else:
                st.error(
                    f"Failed to delete event: {response.json().get('error', 'Unknown error')}"
                )

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the API: {str(e)}")
            st.info("Please ensure the API server is running.")

if st.session_state.get("show_success_modal"):
    show_success_dialog(st.session_state.get("success_event_name", "Event"))

if st.button("Return to Organizer Page"):
    st.switch_page("pages/organizer.py")