import streamlit as st
from utils.ui import hide_streamlit

st.set_page_config(layout="wide")
hide_streamlit()
st.markdown('<div style="font-size: 2rem; font-weight: bold; color: #333; margin-bottom: 1rem;">Staff</div>'
            , unsafe_allow_html=True)

df = st.session_state.df

# Employee data
employees = {
    "manager": {
        "name": "Mohd Shafril Bin Baharudin",
        "title": "Head Mill Research",
        "avatar": "static/exec3.jpg"
    },
    "exec1": {
        "name": "Amirul Faizi Bin Abdu Rahman",
        "title": "Senior Engineer",
        "avatar": "static/exec1.jpg"
    },
    "exec2": {
        "name": "Muhammad Hisham Bin Hussain",
        "title": "Senior Engineer",
        "avatar": "static/exec2.jpg"
    },
    "staff1": {
        "name": "Muhammad Adam Bin Abdul Ghani",
        "title": "Technical Supervisor (TS3)",
        "avatar": "static/staff1.jpg"
    },
    "staff2": {
        "name": "Nor Hafiz Bin Nor Basri",
        "title": "Technical Supervisor (TS2)",
        "avatar": "static/staff2.jpg"
    },
    "staff3": {
        "name": "Muhammad Syazwan Bin Mohd Sa`ad",
        "title": "Technical Supervisor (TS3)",
        "avatar": "static/staff3.jpg"
    },
    "staff4": {
        "name": "Mohammad Haziq Syazwan Bin Rosman",
        "title": "Technical Supervisor (TS4)",
        "avatar": "static/staff4.jpg"
    },
    "staff5": {
        "name": "Mohd Yusof Bin Abd Kadir",
        "title": "Technical Supervisor (TS2)",
        "avatar": "static/staff5.jpg"
    },
    "staff6": {
        "name": "Muhammad Faqris Bin Kamaruzaman",
        "title": "Protege",
        "avatar": "static/protege1.jpg"
    },
    "staff7": {
        "name": "Asreen Dzaqwan Bin Mohamad Safuri",
        "title": "Protege",
        "avatar": "static/protege2.jpg"
    }
}

columns = st.columns(3)

for i, exec_key in enumerate(employees):
    emp = employees[exec_key]
    with columns[i % 3]:  
        with st.container(border=True):
            column = st.columns(2)
            with column[0]:
                st.image(emp['avatar'], width=80)
            with column[1]:
                st.markdown(f"**{emp['name']}**", width="stretch")
                st.caption(emp['title'])
            with st.popover("", width="stretch"):
                #col_img, col_info = st.columns([1, 2])
                # with col_img:
                #     st.image(emp['avatar'], width=80)
                #with col_info:
                st.markdown(f"**{emp['name']}**")
                st.caption(emp['title'])
