import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide', page_title="Manage Requests")
SideBarLinks()

st.title("📝 Booking Requests & Conflict Check")

# Configuration
VENUE_ID = 1
BASE_URL = "http://api:4000/owner"

# --- HELPER FUNCTIONS ---
def update_status(request_id, new_status):
    try:
        # Matches your route: @venue_routes.route("/venues/<int:venue_id>/requests/<int:request_id>", methods=["PUT"])
        url = f"{BASE_URL}/venues/{VENUE_ID}/requests/{request_id}"
        resp = requests.put(url, json={"status": new_status})
        if resp.status_code == 200:
            st.success(f"Request {new_status}!")
            st.rerun()
        else:
            st.error(f"Failed to update: {resp.text}")
    except Exception as e:
        st.error(f"Error: {e}")

# --- DATA FETCHING ---
try:
    # 1. Fetch all requests for this venue
    req_res = requests.get(f"{BASE_URL}/venues/{VENUE_ID}/requests", timeout=2)
    
    if req_res.status_code == 200:
        requests_data = req_res.json()
        
        if not requests_data:
            st.info("No booking requests found for this venue.")
        else:
            # 2. Pre-calculate approved dates to check for conflicts
            approved_dates = [r.get('Date') for r in requests_data if r.get('Status') == 'Approved']

            # 3. UI Table Header
            header_col1, header_col2, header_col3, header_col4, header_col5 = st.columns([2, 2, 1.5, 2, 2])
            header_col1.subheader("Event Name")
            header_col2.subheader("Organizer")
            header_col3.subheader("Date")
            header_col4.subheader("Conflict?")
            header_col5.subheader("Actions")
            st.divider()

            # 4. Loop through requests
            for req in requests_data:
                # We usually only want to manage 'Pending' requests on this page
                if req.get('Status') == 'Pending':
                    r_id = req['RequestID']
                    r_date = req.get('Date')
                    
                    col1, col2, col3, col4, col5 = st.columns([2, 2, 1.5, 2, 2])
                    
                    # Col 1: Event Name
                    col1.write(f"**{req.get('RequestName')}**")
                    
                    # Col 2: Organizer Name (Linked from your SQL JOIN)
                    org_name = f"{req.get('OrganizerFirstName', 'Unknown')} {req.get('OrganizerLastName', '')}"
                    col2.write(org_name)
                    
                    # Col 3: Date
                    col3.write(f"📅 {r_date}")
                    
                    # Col 4: Conflict Logic
                    if r_date in approved_dates:
                        col4.error("⚠️ Date Occupied")
                        has_conflict = True
                    else:
                        col4.success("✅ Clear")
                        has_conflict = False
                    
                    # Col 5: Buttons
                    btn_col1, btn_col2 = col5.columns(2)
                    
                    # Accept Button (Disabled if there is a conflict)
                    if btn_col1.button("Accept", key=f"acc_{r_id}", use_container_width=True, disabled=has_conflict):
                        update_status(r_id, "Approved")
                    
                    # Reject Button
                    if btn_col2.button("Reject", key=f"rej_{r_id}", use_container_width=True, type="secondary"):
                        update_status(r_id, "Rejected")
                    
                    st.divider()
                    
    else:
        st.error(f"API returned error: {req_res.status_code}")

except Exception as e:
    st.error(f"Could not connect to API: {e}")
    st.info("Ensure your Docker containers are running and the database is populated.")