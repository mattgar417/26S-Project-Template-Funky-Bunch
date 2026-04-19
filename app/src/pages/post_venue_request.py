import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Add New Request")

@st.dialog("Success")
def show_success_dialog(request_name):
    st.markdown(f"### {request_name} has been successfully added to the system!")
    
    if st.button("Add Another Request", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_request_name = ""
            st.session_state.reset_form = True
            st.rerun()

if st.session_state.reset_form:
    st.session_state.form_key_counter += 1
    st.session_state.reset_form = False

API_URL = f"http://api:4000/organizers/{st.session_state.organizer_id}/venue-requests"

with st.form(f"add_request_form_{st.session_state.form_key_counter}"):
    st.subheader("Request Information")

    # Required fields
    name = st.text_input("Name")

    submitted = st.form_submit_button("Add Request")

    if submitted:
        if not all([name]):
            st.error("Please fill in all required fields marked with *")
        else:
            request_data = {
                "Name": name,
            }

            try:
                response = requests.post(API_URL, json=request_data)

                if response.status_code == 201:
                    st.session_state.show_success_modal = True
                    st.session_state.success_ngo_name = name
                    st.rerun()
                else:
                    st.error(
                        f"Failed to add request: {response.json().get('error', 'Unknown error')}"
                    )

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API: {str(e)}")
                st.info("Please ensure the API server is running")

if st.session_state.show_success_modal:
    show_success_dialog(st.session_state.success_request_name)

if st.button("Return to Venue Directory"):
    st.switch_page("pages/get_venues.py")