import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

# 1. Page Config
st.set_page_config(layout='wide', page_title="Venue Owner Dashboard")
SideBarLinks()

# --- BACKEND FETCHING LOGIC ---

def get_venue_info(venue_id):
    """Fetch specific venue details like Name and Capacity"""
    try:
        # Note: We use http://api:4000/owner/venues 
        # then filter for Jason's specific ID
        response = requests.get(f"http://api:4000/owner/venues", timeout=2)
        if response.status_code == 200:
            venues = response.json()
            for v in venues:
                if v.get('VenueID') == venue_id:
                    return v
        return None
    except Exception as e:
        logger.error(f"Error fetching venue info: {e}")
        return None

def get_pending_count(venue_id):
    """Fetch and count pending requests for this venue"""
    try:
        response = requests.get(f"http://api:4000/owner/venues/{venue_id}/requests", timeout=2)
        if response.status_code == 200:
            all_requests = response.json()
            pending = [r for r in all_requests if r.get('Status') == 'Pending']
            return len(pending)
        return 0
    except Exception as e:
        logger.error(f"Error fetching requests: {e}")
        return "?"


VENUE_ID = 1
venue_data = get_venue_info(VENUE_ID)
pending_val = get_pending_count(VENUE_ID)

venue_name = venue_data.get('Name', 'Your Venue') if venue_data else 'Jason\'s Jazz Hall'

# --- UI LAYOUT ---
st.title(f"🏟️ Welcome back, {st.session_state.get('first_name', 'Jason')}!")
st.subheader(f"Managing: {venue_name}")

# --- QUICK STATS BAR ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("System Status", "🟢 Online")
with col2:
    st.metric("Venue ID", VENUE_ID)
with col3:
    # Shows real count from the 'Requests' table
    st.metric("Pending Requests", pending_val, delta="New" if pending_val > 0 else None)
with col4:
    # This could be linked to your ReceivedBooking table later
    st.metric("Monthly Revenue", "$1,450") 

st.divider()

# --- MAIN ACTION TILES ---
st.write('### 🛠️ Venue Management Actions')
col_a, col_b, col_c = st.columns(3)

# Custom Styling for bigger buttons
st.markdown("""
    <style>
    div.stButton > button:first-child {
        height: 150px;
        font-size: 24px;
        border-radius: 15px;
    }
    </style>""", unsafe_allow_html=True)

with col_a:
    if st.button('📬\n\nManage Booking Requests', use_container_width=True):

        st.switch_page('venue_manage_requests.py')

with col_b:
    if st.button('📅\n\nView Venue Calendar', use_container_width=True):
        st.switch_page('pages/venue_calendar.py')

with col_c:
    if st.button('📈\n\nView Revenue Analytics', use_container_width=True):
        st.switch_page('pages/venue_revenue.py')

# --- DATA OVERVIEW ---
if venue_data:
    with st.expander("📍 Venue Details"):
        st.write(f"**Location:** {venue_data.get('Location')}")
        st.write(f"**Capacity:** {venue_data.get('Capacity')} guests")