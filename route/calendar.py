import streamlit as st
from streamlit_calendar import calendar
import pandas as pd
from utils.filters import create_filters, apply_filters
from utils.ui import hide_streamlit_css, container_card_css, metric_card_css

# Page configuration
st.set_page_config(layout="wide")
hide_streamlit_css()
container_card_css()

# Page title
st.markdown(
    '<div style="font-size: 2rem; font-weight: bold; color: #333; margin-bottom: 1rem;">Calendar</div>', 
    unsafe_allow_html=True
)

if 'df' not in st.session_state:
    st.error("⚠️ Data not found in session state. Please restart the dashboard.")
    st.stop()

df = st.session_state.df

# Status color mapping
STATUS_COLORS = {
    'Completed': '#2ca02c',
    'Open': '#1f77b4',
    'On Hold': '#ff7f0e',
    'In Progress': '#9467bd',
    'Cancelled': '#d62728'
}

def prepare_calendar_events(data):
    """Convert dataframe to calendar events with detailed work order information"""
    events = []
    
    if data.empty:
        return events
    
    for idx, row in data.iterrows():
        if pd.isna(row.get('Notification date')):
            continue
            
        try:
            event_date = pd.to_datetime(row['Notification date'])
            status = row.get('Work Order Status', 'Unknown')
            color = STATUS_COLORS.get(status, '#808080')
            
            # Build event title with key info
            notification_type = row.get('Notification type', 'Work Order')
            station = row.get('StationList', 'N/A')
            machine = row.get('MachineList', 'N/A')
            
            # Create event object with extended properties
            event = {
                'title': f"{notification_type} - {station}",
                'start': event_date.strftime('%Y-%m-%d'),
                'end': event_date.strftime('%Y-%m-%d'),
                'id': f"event_{idx}",
                'backgroundColor': color,
                'borderColor': color,
                'extendedProps': {
                    # Basic Info
                    'status': status,
                    'notification_type': notification_type,
                    'notification_date': event_date.strftime('%Y-%m-%d %H:%M'),
                    
                    # Equipment Info
                    'station': station,
                    'machine': machine,
                    'equipment_part': row.get('Equipment Part', 'N/A'),
                    
                    # Problem Details
                    'problem_type': row.get('Problem type', 'N/A'),
                    'description': row.get('Description', 'No description'),
                    
                    # Activity Info
                    'activity_by': row.get('Activity by 1', 'N/A'),
                    'activity_duration': row.get('Activity Duration', 0),
                    'activity_count': row.get('ActivityCount', 0),
                    
                    # Breakdown Info
                    'breakdown_hour': row.get('Breakdown Hour', 0),
                    'mttr': row.get('MTTR', 0),
                    
                    # Dates
                    'malfunction_start': pd.to_datetime(row.get('Malfunction Start Date')).strftime('%Y-%m-%d %H:%M') if pd.notna(row.get('Malfunction Start Date')) else 'N/A',
                    'malfunction_stop': pd.to_datetime(row.get('Malfunction Stop Date')).strftime('%Y-%m-%d %H:%M') if pd.notna(row.get('Malfunction Stop Date')) else 'N/A',
                }
            }
            events.append(event)
            
        except Exception as e:
            continue
    
    return events

# Generate calendar events
calendar_events = prepare_calendar_events(df)

# Calendar configuration
calendar_options = {
    "editable": False,
    "selectable": True,
    "navLinks": True,
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "dayGridMonth,dayGridWeek,listWeek"
    },
    "initialView": "dayGridMonth",
    "dayMaxEvents": 3,
    "height": "auto",
    "eventDisplay": "block",
    "displayEventTime": False,
}

# Custom CSS
custom_css = """
.fc-event-past {
    opacity: 0.7;
}
.fc-event-title {
    font-weight: 600;
    font-size: 0.85rem;
}
.fc-toolbar-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #2c3e50;
}
"""
    
if calendar_events:
    state = calendar(
        events=calendar_events,
        options=calendar_options,
        custom_css=custom_css,
        key='work_order_calendar'
    )
    
    # Display event details when clicked
    if state.get("eventClick"):
        event_data = state["eventClick"]["event"]
        props = event_data.get('extendedProps', {})
        
        st.markdown("---")
        st.markdown("### Event Details")
        
        # Create detailed information display
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Basic Information")
            st.write(f"**Status:** {props.get('status', 'N/A')}")
            st.write(f"**Type:** {props.get('notification_type', 'N/A')}")
            st.write(f"**Notification Date:** {props.get('notification_date', 'N/A')}")
            
            st.markdown("#### Equipment Information")
            st.write(f"**Station:** {props.get('station', 'N/A')}")
            st.write(f"**Machine:** {props.get('machine', 'N/A')}")
            st.write(f"**Equipment Part:** {props.get('equipment_part', 'N/A')}")
            
            st.markdown("#### Problem Details")
            st.write(f"**Problem Type:** {props.get('problem_type', 'N/A')}")
            st.write(f"**Description:** {props.get('description', 'N/A')}")
        
        with col2:
            st.markdown("#### Activity Information")
            st.write(f"**Activity By:** {props.get('activity_by', 'N/A')}")
            st.write(f"**Activity Duration:** {props.get('activity_duration', 0):.1f} hours")
            st.write(f"**Activity Count:** {int(props.get('activity_count', 0))}")
            
            st.markdown("#### Breakdown Metrics")
            st.write(f"**MTTR:** {props.get('mttr', 0):.2f} hours")
            st.write(f"**Breakdown Hours:** {props.get('breakdown_hour', 0):.2f}")
            
            st.markdown("#### Timeline")
            st.write(f"**Malfunction Start:** {props.get('malfunction_start', 'N/A')}")
            st.write(f"**Malfunction Stop:** {props.get('malfunction_stop', 'N/A')}")
else:
    st.info("No events to display for the selected filters.")

