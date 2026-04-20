import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("📅 Venue Schedule")

res = requests.get(f"{BASE_URL}/venues/{VENUE_ID}/calendar", timeout=2)
cal_data = res.json() if res.status_code == 200 else []
if not cal_data:
    st.warning("⚠️ Running in Preview Mode")
    cal_data = [
            {"Date": "2026-05-12", "RequestName": "Tech Conference"},
            {"Date": "2026-06-20", "RequestName": "Wedding: Smith & Jones"},
            {"Date": "2026-07-04", "RequestName": "July 4th Bash"}]

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