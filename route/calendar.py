import streamlit as st
from streamlit_calendar import calendar
import pandas as pd
from utils.filters import create_filters, apply_filters
from utils.ui import hide_streamlit_css, container_card_css

st.set_page_config(layout="wide")
hide_streamlit_css()
container_card_css()

st.markdown('<div style="font-size: 2rem; font-weight: bold; color: #333; margin-bottom: 1rem;">Calendar</div>', 
            unsafe_allow_html=True)

if 'calendar_events' not in st.session_state:
    st.session_state.calendar_events = []

if 'df' in st.session_state:
    df = st.session_state.df
    filters = create_filters(df)
    filtered_df = apply_filters(df, filters)
    st.session_state.filtered_df = filtered_df
else:
    st.error("Data not found in session state. Please restart the dashboard.")
    st.stop()

def calendar_events(data):
    """Convert dataframe data to calendar events format"""
    events = []
    if not data.empty:
        for idx, row in data.iterrows():
            if pd.notna(row.get('Notification date')):
                try:
                    event_date = pd.to_datetime(row['Notification date']).date()
                    event = {
                        'title': f"Work Order: {row.get('Work Order Status', 'N/A')}",
                        'start': event_date.isoformat(),
                        'end': event_date.isoformat(),
                        'id': f"event_{idx}",
                        'backgroundColor': '#1f77b4' if row.get('Work Order Status') == 'Open' else '#2ca02c',
                        'borderColor': '#1f77b4' if row.get('Work Order Status') == 'Open' else '#2ca02c',
                    }
                    events.append(event)
                except:
                    continue
    return events

calendar_events = calendar_events(filtered_df)

# Calendar configuration
calendar_options = {
    "selectable": True,
    "navLinks": True,
    "editable": True,
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay,listWeek"
    },
    "initialView": "dayGridMonth",
    "selectMirror": True,
    "dayMaxEvents": True,
    "selectable": True,
}

calendar_events = calendar(
    events=st.session_state.calendar_events + calendar_events,
    options=calendar_options,
    key='calendar'
)

