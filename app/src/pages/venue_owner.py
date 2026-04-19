import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout='wide', page_title="Jason's Venue Dashboard")

# 1. Initialize session state
if 'menu_choice' not in st.session_state:
    st.session_state['menu_choice'] = "Dashboard Home"

# 2. Sidebar Navigation
st.sidebar.title("Owner Controls")
menu_options = ["Dashboard Home", "Manage Requests", "Venue Calendar", "Venue Revenue"]

menu_choice = st.sidebar.selectbox(
    "Select a View", 
    menu_options,
    key='menu_choice' 
)

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
    col3.metric("Pending Tasks", st.session_state.get('requests_count', "5"))

# --- PAGE: MANAGE REQUESTS ---
elif menu_choice == "Manage Requests":
    st.title("📝 Booking Requests & Conflict Check")
    
    try:
        req_res = requests.get(f"{BASE_URL}/venues/{VENUE_ID}/requests", timeout=2)
        cal_res = requests.get(f"{BASE_URL}/venues/{VENUE_ID}/calendar", timeout=2)
        
        if req_res.status_code == 200:
            requests_data = req_res.json()
            booked_dates = [str(event['Date']).split(' ')[0] for event in cal_res.json()] if cal_res.status_code == 200 else []

            h1, h2, h3, h4, h5 = st.columns([2, 2, 2, 1.5, 2.5])
            h1.write("**Organizer**")
            h2.write("**Event Name**")
            h3.write("**Date**")
            h4.write("**Conflict?**")
            h5.write("**Actions**")
            st.divider()

            for req in requests_data:
                r_id = req['RequestID']
                event_date = req.get('Date', '2026-05-12') 
                org_name = f"{req.get('OrganizerFirstName', 'Unknown')} {req.get('OrganizerLastName', '')}"
                
                c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 1.5, 2.5])
                
                if c1.button(org_name, key=f"org_{r_id}"):
                    st.session_state['selected_org_id'] = req.get('OrganizerID', 1)
                    st.switch_page("pages/organizer_profile.py")

                c2.write(req.get('RequestName', 'Unnamed Event'))
                c3.write(f"📅 {event_date}")

                if event_date in booked_dates:
                    c4.error("⚠️ Conflict")
                else:
                    c4.success("✅ Clear")

                b1, b2 = c5.columns(2)
                if b1.button("✅ Accept", key=f"acc_{r_id}"):
                    requests.put(f"{BASE_URL}/venues/{VENUE_ID}/requests/{r_id}", json={"status": "Approved"})
                    st.rerun()
                if b2.button("❌ Reject", key=f"rej_{r_id}"):
                    requests.put(f"{BASE_URL}/venues/{VENUE_ID}/requests/{r_id}", json={"status": "Rejected"})
                    st.rerun()
        else:
            st.info("No requests found.")
    except:
        st.warning("🚨 API Offline: Showing placeholder data.")
        st.info("Example: Sarah Evently | Summer Gala | 2026-06-15 | ✅ Clear")

# --- PAGE: VENUE CALENDAR ---
elif menu_choice == "Venue Calendar":
    st.title("📅 Venue Schedule")
    
    try:
        res = requests.get(f"{BASE_URL}/venues/{VENUE_ID}/calendar", timeout=2)
        cal_data = res.json() if res.status_code == 200 else []
    except:
        st.warning("⚠️ Running in Preview Mode")
        cal_data = [
            {"Date": "2026-05-12", "RequestName": "Tech Conference"},
            {"Date": "2026-06-20", "RequestName": "Wedding: Smith & Jones"},
            {"Date": "2026-07-04", "RequestName": "July 4th Bash"}
        ]

    if cal_data:
        for event in cal_data:
            # SAFETY CHECK: Ensure the date can be split correctly
            raw_date = str(event.get('Date', '2026-01-01')).split(' ')[0]
            date_parts = raw_date.split('-')
            
            # If date format is wrong (not 3 parts), use fallback values
            if len(date_parts) != 3:
                date_parts = ["2026", "01", "01"]

            with st.container():
                col_date, col_info = st.columns([1, 5])
                with col_date:
                    # Fancy Calendar Tile UI
                    st.markdown(f"""
                        <div style="text-align: center; border: 2px solid #ff4b4b; border-radius: 10px; padding: 5px; width: 80px;">
                            <div style="background-color: #ff4b4b; color: white; font-weight: bold; border-radius: 5px 5px 0 0; font-size: 14px;">{date_parts[1]}</div>
                            <div style="font-size: 28px; font-weight: bold; line-height: 1;">{date_parts[2]}</div>
                            <div style="font-size: 12px; color: gray;">{date_parts[0]}</div>
                        </div>
                    """, unsafe_allow_html=True) # Changed from value to html
                
                with col_info:
                    st.subheader(event.get('RequestName', 'Untitled Event'))
                    st.write(f"🏟️ Venue ID: {VENUE_ID}")
                    st.divider()
    else:
        st.success("Your calendar is currently clear!")

# --- PAGE: REVENUE ---
elif menu_choice == "Venue Revenue":
    st.title("💰 Earnings Overview")
    st.write("Real-time financial performance based on approved bookings.")

    try:
        # 1. Fetch data from API
        rev_res = requests.get(f"{BASE_URL}/venues/{VENUE_ID}/revenue", timeout=2)
        
        if rev_res.status_code == 200:
            revenue_data = rev_res.json()
            # Convert JSON list to a Pandas DataFrame for the chart
            df = pd.DataFrame(revenue_data)
            total_rev = df['amount'].sum()
            avg_rev = df['amount'].mean()
        else:
            raise Exception("API Error")

    except:
        st.warning("⚠️ Showing Simulated Revenue Data")
        df = pd.DataFrame({
            'week': ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
            'amount': [1200, 1500, 1100, 1900, 2200]
        })
        total_rev = 7900
        avg_rev = 1580

    # --- UI LAYOUT ---
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Revenue", f"${total_rev:,.2f}", "+12% vs last month")
    with col2:
        st.metric("Average per Event", f"${avg_rev:,.2f}")

    st.write("### Weekly Breakdown")
    # Display the line chart using the dataframe
    st.line_chart(data=df, x='week', y='amount')
    with st.expander("See Raw Transaction Data"):
        st.table(df)