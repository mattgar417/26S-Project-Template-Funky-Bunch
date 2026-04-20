import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
<<<<<<< HEAD

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
=======
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide', page_title="Venue Owner Dashboard")

SideBarLinks()

if 'menu_choice' not in st.session_state:
    st.session_state['menu_choice'] = "Dashboard Home"

st.sidebar.title("Owner Controls")
menu_options = ["Dashboard Home", "Manage Requests", "Venue Calendar", "Venue Revenue"]

menu_choice = st.sidebar.selectbox(
    "Select a View",
    menu_options,
    key='menu_choice'
)

owner_id = st.session_state.get('user_id', 1)
BASE_URL = "http://web-api:4000"

# --- PAGE: DASHBOARD HOME ---
if menu_choice == "Dashboard Home":
    first_name = st.session_state.get('first_name', 'Owner')
    st.title(f"Welcome back, {first_name}!")
    st.write("This is your main management overview.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Status", "Active")
    col2.metric("Owner ID", owner_id)
    col3.metric("Pending Tasks", st.session_state.get('requests_count', "—"))

# --- PAGE: MANAGE REQUESTS ---
elif menu_choice == "Manage Requests":
    st.title("Booking Requests & Conflict Check")

    try:
        req_res = requests.get(f"{BASE_URL}/owner/owners/{owner_id}/requests", timeout=5)
        cal_res = requests.get(f"{BASE_URL}/owner/owners/{owner_id}/calendar", timeout=5)

        if req_res.status_code == 200:
            requests_data = req_res.json()
            booked_dates = []
            if cal_res.status_code == 200:
                booked_dates = [str(event.get('Date', '')).split(' ')[0] for event in cal_res.json()]

            if not requests_data:
                st.info("No booking requests found.")
            else:
                h1, h2, h3, h4, h5 = st.columns([2, 2, 2, 1.5, 2.5])
                h1.write("**Organizer**")
                h2.write("**Event Name**")
                h3.write("**Date**")
                h4.write("**Conflict?**")
                h5.write("**Actions**")
                st.divider()

                for req in requests_data:
                    r_id = req['RequestID']
                    event_date = str(req.get('Date', '')).split(' ')[0]
                    org_name = f"{req.get('OrganizerFirstName', 'Unknown')} {req.get('OrganizerLastName', '')}"

                    c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 1.5, 2.5])

                    if c1.button(org_name, key=f"org_{r_id}"):
                        st.session_state['selected_org_id'] = req.get('OrganizerID', 1)
                        st.switch_page("pages/organizer_profile.py")

                    c2.write(req.get('RequestName', 'Unnamed Event'))
                    c3.write(f"📅 {event_date}" if event_date else "—")

                    if event_date and event_date in booked_dates:
                        c4.error("⚠️ Conflict")
                    else:
                        c4.success("✅ Clear")

                    b1, b2 = c5.columns(2)
                    if b1.button("✅ Accept", key=f"acc_{r_id}"):
                        requests.put(f"{BASE_URL}/owner/requests/{r_id}/status", json={"status": "Approved"})
                        st.rerun()
                    if b2.button("❌ Reject", key=f"rej_{r_id}"):
                        requests.put(f"{BASE_URL}/owner/requests/{r_id}/status", json={"status": "Rejected"})
                        st.rerun()
        else:
            st.error(f"Could not load requests (status {req_res.status_code}).")
    except Exception as e:
        st.error(f"API error: {e}")

# --- PAGE: VENUE CALENDAR ---
elif menu_choice == "Venue Calendar":
    st.title("Venue Schedule")

    try:
        res = requests.get(f"{BASE_URL}/owner/owners/{owner_id}/calendar", timeout=5)
        if res.status_code == 200:
            cal_data = res.json()
        else:
            st.error(f"Could not load calendar (status {res.status_code}).")
            cal_data = []
    except Exception as e:
        st.error(f"API error: {e}")
        cal_data = []

    if cal_data:
        for event in cal_data:
            raw_date = str(event.get('Date', '2026-01-01')).split(' ')[0]
            date_parts = raw_date.split('-')
            if len(date_parts) != 3:
                date_parts = ["2026", "01", "01"]

            with st.container():
                col_date, col_info = st.columns([1, 5])
                with col_date:
                    st.markdown(f"""
                        <div style="text-align: center; border: 2px solid #ff4b4b; border-radius: 10px; padding: 5px; width: 80px;">
                            <div style="background-color: #ff4b4b; color: white; font-weight: bold; border-radius: 5px 5px 0 0; font-size: 14px;">{date_parts[1]}</div>
                            <div style="font-size: 28px; font-weight: bold; line-height: 1;">{date_parts[2]}</div>
                            <div style="font-size: 12px; color: gray;">{date_parts[0]}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with col_info:
                    st.subheader(event.get('RequestName', 'Untitled Event'))
                    st.divider()
    else:
        st.success("Your calendar is currently clear!")

# --- PAGE: REVENUE ---
elif menu_choice == "Venue Revenue":
    st.title("Earnings Overview")
    st.write("Financial performance based on approved bookings.")

    try:
        rev_res = requests.get(f"{BASE_URL}/owner/owners/{owner_id}/revenue", timeout=5)
        if rev_res.status_code == 200:
            revenue_data = rev_res.json()
            df = pd.DataFrame(revenue_data)
            if not df.empty and 'WeeklyRevenue' in df.columns:
                df = df.rename(columns={'WeeklyRevenue': 'amount', 'Week': 'week'})
                df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
                total_rev = df['amount'].sum()
                avg_rev = df['amount'].mean()
            else:
                raise ValueError("Unexpected response format")
        else:
            raise Exception(f"API returned status {rev_res.status_code}")
    except Exception as e:
        st.warning(f"Could not load revenue data: {e}")
        df = pd.DataFrame({
            'week': ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
            'amount': [1200, 1500, 1100, 1900, 2200]
        })
        total_rev = df['amount'].sum()
        avg_rev = df['amount'].mean()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Revenue", f"${total_rev:,.2f}")
    with col2:
        st.metric("Average per Event", f"${avg_rev:,.2f}")

    st.write("### Weekly Breakdown")
    st.line_chart(data=df, x='week', y='amount')
    with st.expander("See Raw Transaction Data"):
        st.table(df)
>>>>>>> 6d53a672f8871fd3d7f75b4f742516614d89906e
