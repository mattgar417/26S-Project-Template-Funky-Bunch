import streamlit as st
import requests

st.set_page_config(layout='wide')

VENUE_ID = 1
BASE_URL = "http://api:4000/venue"
org_id = st.session_state.get('selected_org_id', 1)

st.title("👤 Organizer Profile")

# --- DATA FETCHING WITH FALLBACK ---
try:
    response = requests.get(f"{BASE_URL}/organizers/{org_id}/history", timeout=2)
    if response.status_code == 200:
        data = response.json()
        org_info = data['organizer']
        history = data['history']
    else:
        raise Exception("API Error")
except:
    st.warning("⚠️ Running in Preview Mode (API not reachable)")
    org_info = {"FirstName": "Sarah", "LastName": "Evently", "Email": "sarah@events.com"}
    history = [
        {"RequestName": "Summer Jam 2025", "Status": "Approved", "Date": "2025-07-15"},
        {"RequestName": "Winter Gala", "Status": "Approved", "Date": "2025-12-01"}
    ]

# --- UI LAYOUT ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Contact Info")
    st.write(f"**Name:** {org_info['FirstName']} {org_info['LastName']}")
    st.write(f"**Email:** {org_info['Email']}")
    
    if st.button("⬅️ Back to Dashboard"):
        st.session_state['menu_choice'] = "Manage Requests"
        st.switch_page("venue_owner.py")

with col2:
    st.subheader("Booking History at Your Venue")
    if history:
        for event in history:
            with st.expander(f"📅 {event['RequestName']}"):
                st.write(f"**Date:** {event.get('Date', 'N/A')}")
                st.write(f"**Status:** {event.get('Status', 'Unknown')}")
    else:
        st.info("No past bookings found for this organizer.")