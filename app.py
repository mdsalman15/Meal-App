import streamlit as st
import pandas as pd

# Page Setup - Professional Look
st.set_page_config(page_title="Meal Manager Admin", layout="centered")

# Custom UI Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stButton>button { width: 100%; background-color: #000; color: #fff; border-radius: 5px; height: 45px; }
    .main-title { font-size: 32px; font-weight: 600; text-align: center; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">Meal Management System</div>', unsafe_allow_html=True)

# --- GOOGLE SHEET CONFIG ---
# আপনার গুগল শিটের URL থেকে ID টুকু এখানে বসান
SHEET_ID = "1Iq5vC1jJxUsDEhCXp_0ZyyE8Lw3Wd7-3tnaqfaOmC4s" # উদাহরণ: ১W-৭_...
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

@st.cache_data(ttl=5) # প্রতি ৫ সেকেন্ড পর নতুন ডাটা চেক করবে
def load_data():
    return pd.read_csv(SHEET_URL)

try:
    df = load_data()
    
    # Live Summary Cards
    total_on = len(df[df['Status'] == 'On'])
    total_extra = df['Extra_Meals'].sum()
    
    c1, c2 = st.columns(2)
    c1.metric("Current Total Meals", int(total_on + total_extra))
    c2.metric("Extra/Guest Meals", int(total_extra))

    st.divider()

    # Member Control Section
    names = df['Name'].tolist()
    selected_name = st.selectbox("আপনার নাম সিলেক্ট করুন", names)
    
    idx = df[df['Name'] == selected_name].index[0]
    
    col_a, col_b = st.columns(2)
    with col_a:
        current_status = True if df.at[idx, 'Status'] == 'On' else False
        new_status = st.toggle("Meal Status", value=current_status)
    with col_b:
        new_extra = st.number_input("Extra Meal", min_value=0, value=int(df.at[idx, 'Extra_Meals']))

    if st.button("Update and Sync"):
        # যেহেতু সরাসরি রাইট করা জটিল, আমরা আপডেট করা ডাটা নিচে দেখাবো
        df.at[idx, 'Status'] = 'On' if new_status else 'Off'
        df.at[idx, 'Extra_Meals'] = new_extra
        st.success(f"Status updated for {selected_name}! Please refresh after manual sheet sync.")
        st.dataframe(df[['Name', 'Status', 'Extra_Meals', 'Total_Month_Meals']], use_container_width=True)
        
        # গুগল শিট ওপেন করার বাটন
        st.link_button("Open Google Sheet to Save Permanently", f"https://docs.google.com/spreadsheets/d/{SHEET_ID}")

except Exception as e:
    st.error("Google Sheet কানেক্ট করা যাচ্ছে না। দয়া করে SHEET_ID চেক করুন এবং শিটটি 'Anyone with the link' এ 'Editor' মুডে শেয়ার করুন।")
