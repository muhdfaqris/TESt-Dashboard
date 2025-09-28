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
    overview = st.Page(
        "route/overview.py", 
        title = "Overview", 
        icon=":material/overview:", 
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
    settings = st.Page(
        "route/settings.py", 
        title = "Settings",
        icon=":material/settings:"
    )
    pg = st.navigation(
        {
            "Dashboard": [overview, data_records, staff],
            "Configurations": [settings]
        }
    )
    pg.run()

if __name__ == "__main__":
    main()