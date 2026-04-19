import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout='wide', page_title="Jason's Venue Dashboard")


if 'menu_choice' not in st.session_state:
    st.session_state['menu_choice'] = "Dashboard Home"


st.sidebar.title("Owner Controls")
menu_options = ["Dashboard Home", "Manage Requests", "Venue Calendar", "Venue Revenue", "Organizer Profile"]

current_index = menu_options.index(st.session_state['menu_choice'])
choice = st.sidebar.selectbox(
    "Select a View", 
    menu_options,
    index=current_index
)

# Sync the choice back to session state
st.session_state['menu_choice'] = choice
menu_choice = st.session_state['menu_choice']
# 3. Setup
VENUE_ID = 1
BASE_URL = "http://api:4000/venue"

# --- PAGE: DASHBOARD HOME ---
if menu_choice == "Dashboard Home":
    st.title(f"🏟️ Welcome back, Jason!")
    st.write("This is your main management overview.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Status", "Active")
    col2.metric("Venue ID", VENUE_ID)
    col3.metric("System Health", "Operational")

# --- PAGE: MANAGE REQUESTS ---
elif menu_choice == "Manage Requests":
    st.title("📝 Booking Requests & Conflict Check")
    
    # 1. Fetch data
    req_res = requests.get(f"{BASE_URL}/venues/{VENUE_ID}/requests")
    
    if req_res.status_code == 200:
        all_requests = req_res.json()
        
        # Get dates already booked (Status is Approved) to check for conflicts
        # Using .get() and string conversion to prevent split errors
        booked_dates = [str(e.get('Date', '')).split(' ')[0] for e in all_requests if e['Status'] == 'Approved']

        # 2. Filter for Pending only
        pending = [r for r in all_requests if r['Status'] == 'Pending']
        
        if not pending:
            st.success("No more pending requests!")
        else:
            # Header Row
            h1, h2, h3, h4, h5 = st.columns([2, 2, 2, 1.5, 2.5])
            h1.write("**Organizer**")
            h2.write("**Event Name**")
            h3.write("**Requested Date**")
            h4.write("**Conflict?**")
            h5.write("**Action**")
            st.divider()

            for req in pending:
                r_id = req['RequestID']
                # Safe date parsing
                raw_date = req.get('Date', 'TBD')
                event_date = str(raw_date).replace(" 00:00:00", "")
                
                c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 1.5, 2.5])
                if c1.button(f"👤 {req['OrganizerFirstName']} {req['OrganizerLastName']}", key=f"org_{r_id}"):
                   st.session_state['selected_org_id'] = req['OrganizerID']    
                   st.session_state['menu_choice'] = "Organizer Profile"
                   st.rerun()
                c2.write(req['RequestName'])
                c3.write(f"📅 {event_date}")
                
                # Check for Conflict
                if event_date in booked_dates:
                    c4.error("⚠️ Conflict")
                else:
                    c4.success("✅ Clear")

                # Action Button to CONFIRM
                if c5.button("Confirm Event", key=f"acc_{r_id}"):
                    # Sends PUT request to update status to 'Approved'
                    requests.put(f"{BASE_URL}/venues/{VENUE_ID}/requests/{r_id}", json={"status": "Approved"})
                    st.toast(f"Confirmed {req['RequestName']}!")
                    st.rerun()

# --- PAGE: VENUE CALENDAR ---
elif menu_choice == "Venue Calendar":
    st.title("📅 Venue Schedule")
    st.write("Confirmed events currently hosted at this venue.")
    
    cal_res = requests.get(f"{BASE_URL}/venues/{VENUE_ID}/calendar")
    
    if cal_res.status_code == 200:
        events = cal_res.json()
        if not events:
            st.info("No confirmed events found in the schedule.")
        else:
            df_cal = pd.DataFrame(events)
            if 'Date' in df_cal.columns:
                df_cal['Date'] = df_cal['Date'].apply(lambda x: str(x).replace(" 00:00:00", ""))
            st.table(df_cal)
    else:
        st.error("Could not load calendar data.")
                    
# --- PAGE: REVENUE ---
elif menu_choice == "Venue Revenue":
    st.title("💰 Earnings Overview")
    st.write("Real-time financial performance based on approved bookings.")

    try:
        rev_res = requests.get(f"{BASE_URL}/venues/{VENUE_ID}/revenue", timeout=2)
        
        if rev_res.status_code == 200:
            revenue_data = rev_res.json()
            if revenue_data:
                df = pd.DataFrame(revenue_data)
                total_rev = df['amount'].sum()
                avg_rev = df['amount'].mean()
            else:
                # Fallback if the list is empty
                df = pd.DataFrame({'week': [], 'amount': []})
                total_rev, avg_rev = 0, 0
        else:
            raise Exception("API Error")

    except:
<<<<<<< HEAD
<<<<<<< HEAD
        # 2. FALLBACK: Mock Data if SQL/API is unreachable
=======
>>>>>>> 2b3c715 (Integrated Venue Owner and Organizer UI pages)
        st.warning("⚠️ Showing Simulated Revenue Data")
=======
        st.warning("⚠️ Showing Simulated Revenue Data (API Unreachable)")
>>>>>>> 91b855d (Merge remote changes)
        df = pd.DataFrame({
            'week': ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
            'amount': [1200, 1500, 1100, 1900, 2200]
        })
        total_rev = df['amount'].sum()
        avg_rev = df['amount'].mean()

    # --- UI LAYOUT ---
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Revenue", f"${total_rev:,.2f}", "+12% vs last month")
    with col2:
        st.metric("Average per Event", f"${avg_rev:,.2f}")

    st.write("### Weekly Breakdown")
<<<<<<< HEAD
    # Display the line chart using the dataframe
    st.line_chart(data=df, x='week', y='amount')
<<<<<<< HEAD

    # Display the raw data table for transparency
=======
>>>>>>> 2b3c715 (Integrated Venue Owner and Organizer UI pages)
    with st.expander("See Raw Transaction Data"):
        st.table(df)
=======
    if not df.empty:
        st.line_chart(data=df, x='week', y='amount')
        with st.expander("See Raw Transaction Data"):
            st.table(df)
    else:
        st.info("No revenue data available yet.")
>>>>>>> 91b855d (Merge remote changes)
