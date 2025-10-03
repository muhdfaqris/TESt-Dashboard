import streamlit as st
from utils.db import init_db
from utils.data import preprocess_data

def main():
    st.logo("static/sdgrtest_logo.png",size="large")

    # Initiate and load data from database
    init_db()
    with st.spinner("Loading and processing data..."):
        df = preprocess_data()

    st.session_state.df = df

    # Define pages
    dashboard = st.Page(
        "route/dashboard.py",
        title = "Dashboard",
        icon=":material/dashboard:",
        default=True
    )
    data_records = st.Page(
        "route/data_records.py",
        title = "Data records",
        icon=":material/database:"
    )
    staff = st.Page(
        "route/staff.py",
        title = "Staff",
        icon=":material/people:"
    )
    calendar = st.Page(
        "route/calendar.py",
        title = "Calendar",
        icon=":material/calendar_today:"
    )
    settings = st.Page(
        "route/settings.py",
        title = "Settings",
        icon=":material/settings:"
    )
    
    pg = st.navigation(
        { 
            "Menu": [dashboard, data_records],
            "Management": [staff, calendar],
            "Configurations": [settings]
        }
    )
    pg.run()

if __name__ == "__main__":
    main()