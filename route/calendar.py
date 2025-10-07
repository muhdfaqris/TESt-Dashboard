import streamlit as st
from streamlit_calendar import calendar
import pandas as pd
from utils.ui import hide_streamlit_css

st.set_page_config(layout="wide")
hide_streamlit_css()

st.markdown(
    '<div style="font-size: 2rem; font-weight: bold; color: #333; margin-bottom: 1rem;">Calendar</div>', 
    unsafe_allow_html=True
)

if 'df' not in st.session_state:
    st.error("Data not found in session state. Please restart the dashboard.")
    st.stop()

STATUS_COLORS = {
    'Completed': '#2ca02c',
    'Open': "#e7e41b",
    'On Hold': '#ff7f0e',
    'In Progress': '#9467bd',
    'Cancelled': '#d62728'
}

@st.cache_data
def prepare_calendar_events(data):
    """Convert dataframe to calendar events"""
    events = []
    
    if data.empty:
        return events
    
    valid_data = data[data['Notification date'].notna()].copy()
    
    for idx, row in valid_data.iterrows():
        try:
            event_date = pd.to_datetime(row['Notification date'])
            status = row.get('Work Order Status', 'Unknown')
            color = STATUS_COLORS.get(status, '#808080')
            
            notification_type = row.get('Notification type', 'Work Order')
            station = row.get('StationList', 'N/A')
            
            event = {
                'title': f"{notification_type} - {station}",
                'start': event_date.strftime('%Y-%m-%d'),
                'end': event_date.strftime('%Y-%m-%d'),
                'id': f"event_{idx}",
                'backgroundColor': color,
                'borderColor': color,
            }
            events.append(event)
        except Exception:
            continue
    
    return events

calendar_events = prepare_calendar_events(st.session_state.df)

CALENDAR_OPTIONS = {
    "editable": False,
    "selectable": True,
    "navLinks": True,
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,listWeek"
    },
    "initialView": "dayGridMonth",
    "dayMaxEvents": 3,
    "height": "auto",  # Auto height
    "contentHeight": "auto",  # Auto content height
    "aspectRatio": 1.5,  # Maintain aspect ratio
    "eventDisplay": "block",
    "displayEventTime": False,
    "moreLinkClick": "popover",
}

CUSTOM_CSS = """
/* Calendar Container - Auto Resize */
.fc {
    height: auto !important;
    min-height: 600px !important;
}

.fc-view-harness {
    height: auto !important;
    overflow: visible !important;
}

.fc-daygrid-body {
    height: auto !important;
    overflow: visible !important;
}

/* ===== FIX EVENT CUTOFF - EXPAND CELLS ===== */

/* Allow cells to expand fully */
.fc-daygrid-day-frame {
    min-height: 150px !important;  /* Increased from 120px */
    height: auto !important;
    max-height: none !important;  /* Remove height limit */
    display: flex !important;
    flex-direction: column !important;
    overflow: visible !important;
}

.fc-daygrid-day-top {
    flex-shrink: 0 !important;
}

.fc-daygrid-day-events {
    flex-grow: 1 !important;
    overflow: visible !important;
    margin: 0 !important;
    min-height: fit-content !important;
}

.fc-daygrid-day-bottom {
    flex-shrink: 0 !important;
    margin-top: auto !important;
}

/* Week rows auto expand */
.fc-daygrid-body tr {
    height: auto !important;
}

/* Event harness should not clip */
.fc-daygrid-event-harness {
    overflow: visible !important;
    margin-bottom: 1px !important;
}

/* ===== REMOVE ALL SCROLLBARS ===== */
.fc-scroller {
    overflow: visible !important;
}

.fc-scroller-liquid-absolute {
    overflow: visible !important;
}

.fc-scroller-harness {
    overflow: visible !important;
}

.fc-scroller-harness-liquid {
    overflow: visible !important;
}

/* Hide scrollbar in header */
.fc-col-header {
    overflow: hidden !important;
}

.fc-scrollgrid-section-header {
    overflow: hidden !important;
}

.fc-scrollgrid-section-header .fc-scroller {
    overflow: hidden !important;
}

/* Force full width */
.fc-scrollgrid {
    border-collapse: collapse !important;
    width: 100% !important;
}

.fc-scrollgrid-sync-table {
    width: 100% !important;
}

.fc-daygrid {
    width: 100% !important;
}

/* Equal column widths */
.fc-col-header-cell,
.fc-daygrid-day {
    width: 14.285% !important;
}

.fc-daygrid-day {
    background-color: #ffffff;
    border-color: #e0e0e0 !important;
    vertical-align: top !important;  /* Align content to top */
}

.fc-daygrid-day:hover {
    background-color: #f8f9fa;
}

.fc-day-today {
    background-color: #e3f2fd !important;
}

.fc-daygrid-day-number {
    font-weight: 600;
    color: #2c3e50;
    padding: 6px 8px;
    font-size: 0.9rem;
}

/* Event Display */
.fc-event {
    border-radius: 6px !important;
    padding: 3px 6px !important;
    margin: 1px 2px !important;
    border: none !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
    transition: all 0.2s ease !important;
    min-height: 22px !important;
    height: auto !important;
    overflow: visible !important;
    cursor: pointer !important;
}

.fc-event:hover {
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.2) !important;
    transform: translateY(-2px) scale(1.02);
    z-index: 100 !important;
}

.fc-event-main {
    padding: 0 !important;
    overflow: visible !important;
}

.fc-event-title {
    font-weight: 600;
    font-size: 0.75rem;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
    line-height: 1.3;
    word-break: break-word;
}

.fc-daygrid-event {
    white-space: normal !important;
    height: auto !important;
    margin-bottom: 1px !important;
    overflow: visible !important;
}

/* More Link */
.fc-daygrid-more-link {
    background-color: #e8e8e8 !important;
    border-radius: 4px !important;
    padding: 3px 8px !important;
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    color: #2c3e50 !important;
    margin: 2px !important;
    border: 1px solid #d0d0d0 !important;
}

.fc-daygrid-more-link:hover {
    background-color: #d0d0d0 !important;
}

/* Toolbar */
.fc-toolbar-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #2c3e50;
}

.fc-header-toolbar {
    padding: 12px 0;
    margin-bottom: 20px !important;
}

/* Buttons - Pill Theme */
.fc-button-group {
    background-color: #e8e8e8;
    border-radius: 8px;
    padding: 4px;
    gap: 4px;
}

.fc-button {
    background-color: transparent !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 6px 16px !important;
    color: #6b7280 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    margin: 0 !important;
    box-shadow: none !important;
}

.fc-button:hover {
    background-color: rgba(255, 255, 255, 0.5) !important;
    transform: scale(1.02);
}

.fc-button-active {
    background-color: #ffffff !important;
    color: #1f2937 !important;
    font-weight: 700 !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
}

.fc-button:focus {
    box-shadow: none !important;
    outline: none !important;
}

/* Column Headers */
.fc-col-header-cell {
    background-color: #f5f5f5;
    font-weight: 700;
    color: #34495e;
    border-color: #e0e0e0 !important;
    padding: 10px;
}

/* Popover */
.fc-popover {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    z-index: 1000 !important;
    max-width: 350px;
}

.fc-popover-header {
    background-color: #f5f5f5;
    border-bottom: 1px solid #e0e0e0;
    padding: 10px 12px;
    font-weight: 700;
    border-radius: 8px 8px 0 0;
}

.fc-popover-body {
    padding: 8px;
    max-height: 400px;
    overflow-y: auto;
}

/* Past Events */
.fc-event-past {
    opacity: 0.7;
}

/* List View */
.fc-list-event:hover {
    background-color: #f8f9fa !important;
}
"""

# Render calendar
if calendar_events:
    calendar_key = f"calendar_{len(calendar_events)}"
    
    state = calendar(
        events=calendar_events,
        options=CALENDAR_OPTIONS,
        custom_css=CUSTOM_CSS,
        key=calendar_key
    )
else:
    st.info("No events to display.")
