import streamlit as st
import pandas as pd

# অ্যাপের টাইটেল এবং ডিজাইন
st.set_page_config(page_title="Meal Manager Pro", layout="centered")
st.title("🏠 Flat Meal Manager")
st.markdown("---")

# ডামি ডাটা (বাস্তবে এটি গুগল শিট থেকে আসবে)
if 'meal_data' not in st.session_state:
    st.session_state.meal_data = pd.DataFrame({
        'User': [f'User {i}' for i in range(1, 11)],
        'Status': ['On'] * 10,
        'Extra': [0] * 10,
        'Total_Month': [0] * 10
    })

df = st.session_state.meal_data

# ইউজার সিলেকশন (লগইন সিস্টেমের বিকল্প)
current_user = st.selectbox("আপনার নাম সিলেক্ট করুন", df['User'])

# মেইন ইন্টারফেস (২টি কলাম)
col1, col2 = st.columns(2)

with col1:
    st.subheader("Manage Meal")
    # অন/অফ সুইচ
    idx = df[df['User'] == current_user].index[0]
    is_on = st.toggle(f"Meal for {current_user}", value=(df.at[idx, 'Status'] == 'On'))
    df.at[idx, 'Status'] = 'On' if is_on else 'Off'
    
    # এক্সট্রা মিল এড
    extra = st.number_input("Extra Meal (Guest)", min_value=0, max_value=10, step=1)
    df.at[idx, 'Extra'] = extra

with col2:
    st.subheader("Live Status")
    total_on = len(df[df['Status'] == 'On'])
    total_extra = df['Extra'].sum()
    
    st.metric("Running Meals", f"{total_on + total_extra}")
    st.write(f"Regular: {total_on} | Extra: {total_extra}")

st.markdown("---")
st.subheader("📊 Monthly Summary (All Members)")
st.table(df)

# ডাটা সেভ বাটন
if st.button("Save Changes"):
    st.success("Data Updated Successfully!")
