import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome venue owner, {st.session_state['first_name']}.")
st.write('### Dashboard:')

if st.button('View all events',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/view_events.py')

if st.button('View all requests',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/view_requests.py')

if st.button('Look at your bookings calendar',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/view_bookings_calendar.py')

if st.button('Look at your revenue',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/view_revenue.py')