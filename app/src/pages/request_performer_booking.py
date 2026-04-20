import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Book a Performer")

performer_id = st.session_state.get('selected_performer_id')
performer_name = st.session_state.get('selected_performer_name', 'Selected Performer')
organizer_id = st.session_state.get('user_id', 1)

if not performer_id:
    st.warning("No performer selected. Please go back and choose one.")
    if st.button("Back to Performer Directory"):
        st.switch_page("pages/get_performers.py")
    st.stop()

st.subheader(f"Sending booking request to: **{performer_name}**")

@st.dialog("Booking Sent!")
def show_success_dialog(name):
    st.markdown(f"### Your booking request to **{name}** was submitted successfully!")
    if st.button("Book Another Performer", use_container_width=True):
        st.session_state.pop('selected_performer_id', None)
        st.session_state.pop('selected_performer_name', None)
        st.rerun()

if 'booking_success' not in st.session_state:
    st.session_state['booking_success'] = False

with st.form("booking_form"):
    compensation = st.number_input("Compensation Offer ($)", min_value=0.0, step=50.0, format="%.2f")
    submitted = st.form_submit_button("Send Booking Request")

    if submitted:
        if compensation <= 0:
            st.error("Please enter a compensation amount greater than $0.")
        else:
            payload = {
                "organizer_id": organizer_id,
                "compensation": compensation,
                "status": "Pending"
            }
            try:
                url = f"http://web-api:4000/performer/performers/{performer_id}/bookings"
                response = requests.post(url, json=payload)
                if response.status_code == 201:
                    st.session_state['booking_success'] = True
                    st.rerun()
                else:
                    st.error(f"Failed to send request: {response.json().get('error', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API: {str(e)}")

if st.session_state['booking_success']:
    show_success_dialog(performer_name)

if st.button("Back to Performer Directory"):
    st.switch_page("pages/get_performers.py")
