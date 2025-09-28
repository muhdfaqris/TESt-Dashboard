import streamlit as st
import pandas as pd

def create_filters(df):
    """ Create sidebar filters """

    if df.empty:
        return {
            'date_range': None,
            'status': 'All',
            'stations': [],
            'types': [],
            'staff': [],
        }
    
    # Ensure proper data types
    df = df.copy()
    df['Notification date'] = pd.to_datetime(df['Notification date'], errors='coerce')
    
    valid_dates = df['Notification date'].dropna()
    if not valid_dates.empty:
        date_min = valid_dates.min().date()
        date_max = valid_dates.max().date()
        
        col = st.sidebar.columns(2)
        with col[0]:
            date_range1 = st.sidebar.date_input(
                "Date Start",
                value=date_min,
                min_value=date_min,
            )
        with col[1]:
            date_range2 = st.sidebar.date_input(
                "Date End",
                value=date_max,
                max_value=date_max
            )
    else:
        date_range = None

    status_options = ['All'] + list(df['Work Order Status'].unique())
    selected_status = st.sidebar.multiselect("Work Order Status", status_options, default=['All'])
    station_options = ['All'] + list(df['StationList'].unique())
    selected_stations = st.sidebar.multiselect("Station", station_options, default=['All'])
    type_options = ['All'] + list(df['Notification type'].unique())
    selected_types = st.sidebar.multiselect("Notification Type", type_options, default=['All'])
    staff_options = ['All'] + list(df['Activity by 1'].unique())
    selected_staff = st.sidebar.multiselect("Staff", staff_options, default=['All'])

    date_range = (date_range1, date_range2)
    return {
        'date_range': date_range,
        'status': selected_status,
        'stations': selected_stations,
        'types': selected_types,
        'staff': selected_staff,
    }

@st.cache_data
def apply_filters(df, filters):
    """ Apply filters to dataframe """

    if df.empty:
        return df
        
    filtered_df = df.copy()
    
    # Date filter 
    if filters['date_range'] and len(filters['date_range']) == 2:
        filtered_df['Notification date'] = pd.to_datetime(filtered_df['Notification date'], errors='coerce')
        
        start_date = pd.Timestamp(filters['date_range'][0])
        end_date = pd.Timestamp(filters['date_range'][1]) + pd.Timedelta(days=1)
        
        # Filter only valid dates 
        filtered_df = filtered_df[
            (filtered_df['Notification date'].notna()) &
            (filtered_df['Notification date'] >= start_date) & 
            (filtered_df['Notification date'] < end_date)
        ]
    
    if 'All' not in filters['status'] and filters['status']:
        filtered_df = filtered_df[filtered_df['Work Order Status'].isin(filters['status'])]
    if 'All' not in filters['stations'] and filters['stations']:
        filtered_df = filtered_df[filtered_df['StationList'].isin(filters['stations'])]
    if 'All' not in filters['types'] and filters['types']:
        filtered_df = filtered_df[filtered_df['Notification type'].isin(filters['types'])]
    if 'All' not in filters['staff'] and filters['staff']:
        filtered_df = filtered_df[filtered_df['Activity by 1'].isin(filters['staff'])]

    return filtered_df
