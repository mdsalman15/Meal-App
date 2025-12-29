import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetConnection

# পেজ কনফিগারেশন
st.set_page_config(page_title="Meal Manager Pro", layout="centered")
st.title("Flat Meal Manager")

# গুগল শিট কানেকশন (এখানে আপনার শিটের ইউআরএল দিন)
sheet_url = "https://docs.google.com/spreadsheets/d/1Iq5vC1jJxUsDEhCXp_0ZyyE8Lw3Wd7-3tnaqfaOmC4s/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetConnection)

# ডাটা রিড করা
df = conn.read(spreadsheet=sheet_url)

# ইউজার সিলেকশন
names = df['Name'].tolist()
current_user = st.selectbox("আপনার নাম সিলেক্ট করুন", names)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Manage Meal")
    idx = df[df['Name'] == current_user].index[0]
    
    # মিল অন/অফ
    status_val = True if df.at[idx, 'Status'] == 'On' else False
    is_on = st.toggle(f"Meal for {current_user}", value=status_val)
    
    # এক্সট্রা মিল
    extra = st.number_input("Extra Meal (Guest)", min_value=0, max_value=10, value=int(df.at[idx, 'Extra']))

if st.button("Save Changes"):
    # ডাটা আপডেট
    df.at[idx, 'Status'] = 'On' if is_on else 'Off'
    df.at[idx, 'Extra'] = extra
    conn.update(spreadsheet=sheet_url, data=df)
    st.success("হিসাব আপডেট হয়েছে!")
    st.rerun()

st.markdown("---")
with col2:
    st.subheader("Live Status")
    total_on = len(df[df['Status'] == 'On'])
    total_extra = df['Extra'].sum()
    st.metric("Total Meals Today", f"{total_on + total_extra}")

st.subheader("Monthly Summary")
st.dataframe(df, use_container_width=True)
