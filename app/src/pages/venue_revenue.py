import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

# Page Setup
st.set_page_config(layout='wide', page_title="Venue Revenue")

SideBarLinks()

st.title("💰 Earnings Overview")
st.write("Real-time financial performance based on approved bookings.")

#  Configuration
# Note: Using session state for ID is better than hardcoding
OWNER_ID = st.session_state.get('id', 1) 
BASE_URL = "http://api:4000/owner"

#  Data Fetching Logic
try:
    rev_res = requests.get(f"{BASE_URL}/venues/1/revenue", timeout=2)
    
    if rev_res.status_code == 200:
        revenue_data = rev_res.json()
        df = pd.DataFrame(revenue_data)
    
        total_rev = df['amount'].sum()
        avg_rev = df['amount'].mean()
    else:
        raise Exception("API Error")

except Exception as e:
    st.warning("⚠️ Showing Simulated Revenue Data (API Offline or route mismatch)")
    # Fallback data so the UI doesn't break
    df = pd.DataFrame({
        'week': ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
        'amount': [1200, 1500, 1100, 1900, 2200]
    })
    total_rev = df['amount'].sum()
    avg_rev = df['amount'].mean()

# UI Layout
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Revenue", f"${total_rev:,.2f}", "+12% vs last month")
with col2:
    st.metric("Average per Event", f"${avg_rev:,.2f}")

st.write("### Weekly Breakdown")
# Create chart
st.line_chart(data=df, x='week', y='amount')
with st.expander("See Raw Transaction Data"):
    st.table(df)

if st.button('Back to Dashboard', type='secondary'):
    st.switch_page('pages/Venue_Owner_Home.py')
