import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetConnection

# Professional Page Setup
st.set_page_config(page_title="Meal Manager Admin", layout="wide")

# Official UI Styling (No Emojis, Clean Look)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #ffffff; }
    div[data-testid="stMetricValue"] { font-size: 36px; font-weight: 600; color: #1a1a1a; }
    .stButton>button { 
        background-color: #000000; color: #ffffff; 
        border-radius: 4px; border: none; font-weight: 600;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #333333; border: none; color: #ffffff; }
    .status-card {
        padding: 20px; border-radius: 8px; border: 1px solid #e0e0e0; background-color: #fcfcfc;
    }
    </style>
    """, unsafe_allow_html=True)

# Google Sheet Link (Replace with your link)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Iq5vC1jJxUsDEhCXp_0ZyyE8Lw3Wd7-3tnaqfaOmC4s/edit?usp=sharing"

# Data Connection
try:
    conn = st.connection("gsheets", type=GSheetConnection)
    # TTL=0 ensures the app fetches fresh data every time it runs
    df = conn.read(spreadsheet=SHEET_URL, ttl=0)
except Exception as e:
    st.error("Connection Error. Please check Spreadsheet URL and Editor permissions.")
    st.stop()

# Dashboard Header
st.title("Meal Management System")
st.text("Official Portal for Resident Management")
st.divider()

# Top Metrics Row
total_on_members = len(df[df['Status'] == 'On'])
total_extra_meals = pd.to_numeric(df['Extra_Meals']).sum()
total_running = total_on_members + total_extra_meals

m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Running Meals Today", int(total_running))
with m2:
    st.metric("Base Meals (On)", int(total_on_members))
with m3:
    st.metric("Guest/Extra Meals", int(total_extra_meals))

st.markdown("<br>", unsafe_allow_html=True)

# Main Interaction Area
left, right = st.columns([1, 2], gap="large")

with left:
    st.markdown("### Member Control")
    user_list = df['Name'].tolist()
    selected_user = st.selectbox("Select Your Name", user_list)
    
    # Get current index and data
    idx = df[df['Name'] == selected_user].index[0]
    
    # Interaction Widgets
    current_status = True if df.at[idx, 'Status'] == 'On' else False
    new_status = st.toggle("Enable My Meal", value=current_status)
    
    new_extra = st.number_input("Add Extra Meals", min_value=0, max_value=50, value=int(df.at[idx, 'Extra_Meals']))

    if st.button("Update Status"):
        # Update logic
        df.at[idx, 'Status'] = 'On' if new_status else 'Off'
        df.at[idx, 'Extra_Meals'] = new_extra
        
        # Monthly count logic: Meal 'On' thakle +1 hobe prothibar update e
        if new_status:
            df.at[idx, 'Total_Month_Meals'] = int(df.at[idx, 'Total_Month_Meals']) + 1
        
        # Sync to Google Sheets
        conn.update(spreadsheet=SHEET_URL, data=df)
        st.success(f"Record updated for {selected_user}")
        st.rerun()

with right:
    st.markdown("### Global Summary")
    # Clean display of the data
    display_df = df[['Name', 'Status', 'Extra_Meals', 'Total_Month_Meals']]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

st.divider()
st.caption("System Status: Operational | Data synced with Google Cloud")
