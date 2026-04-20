import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

st.session_state['authenticated'] = False

SideBarLinks(show_home=True)

logger.info("Loading the Home page of the app")
st.title('communevent')
st.write('#### Hi! As which user would you like to log in?')

if st.button("Act as Sarah, an attendee",
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'attendee'
    st.session_state['first_name'] = 'Sarah'
    logger.info("Logging in as an attendee")
    st.switch_page('pages/attendee.py')

if st.button('Act as Jason, a venue owner',
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'venue_owner'
    st.session_state['first_name'] = 'Jason'
    st.switch_page('pages/venue_owner.py')

if st.button('Act as Ron, an event organizer',
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'organizer'
    st.session_state['first_name'] = 'Ron'
    st.switch_page('pages/organizer.py')

if st.button('Act as Caleb, a performer',
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'performer'
    st.session_state['first_name'] = 'Mohammad'
    st.switch_page('pages/40_performer_home.py')