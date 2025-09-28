import streamlit as st
import pandas as pd
from utils.filters import apply_filters

@st.cache_data
def calculate_kpi(df):
    """ Calculate KPI from the dataframe """

    if df.empty:
        return {
            'total_orders': 0,
            'completed_orders': 0,
            'completion_rate': 0,
            'avg_mttr': 0,
            'avg_duration': 0
        }
    
    total_orders = len(df)
    completed_orders = len(df[df['Work Order Status'] == 'Completed'])
    completion_rate = (completed_orders / total_orders * 100) if total_orders > 0 else 0

    avg_mttr = float(df['MTTR'].mean()) if not df['MTTR'].empty else 0.0
    avg_duration = float(df['Activity Duration'].mean()) if not df['Activity Duration'].empty else 0.0
    
    return {
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'completion_rate': completion_rate,
        'avg_mttr': avg_mttr,
        'avg_duration': avg_duration
    }

def calculate_delta(current_kpi, previous_kpi, as_percentage=False):
    """ Calculate percentage difference between current and previous KPI """

    if not previous_kpi:
        return {}
    
    delta = {}
    for key in current_kpi:
        if key in previous_kpi and previous_kpi[key] is not None:
            if as_percentage:
                if previous_kpi[key] != 0:
                    delta[key] = ((current_kpi[key] - previous_kpi[key]) / previous_kpi[key]) * 100
                else:
                    # Handle division by zero
                    delta[key] = 0 if current_kpi[key] == 0 else float('inf')
            else:
                delta[key] = current_kpi[key] - previous_kpi[key]
        else:
            delta[key] = 0
    
    return delta

def calculate_prev(df, filters=None):
    """ Get previous dataframe based on current filters """
    
    # Create a copy of filters for the previous period
    previous_filters = filters.copy() if filters else {}
    
    # Adjust date range to previous month
    if filters and filters.get('date_range') and len(filters['date_range']) == 2:
        # Get current date range
        current_start = pd.Timestamp(filters['date_range'][0])
        current_end = pd.Timestamp(filters['date_range'][1])
        
        # Calculate previous month range 
        previous_start = current_start - pd.Timedelta(days=30)
        previous_end = current_end - pd.Timedelta(days=30)
        
        # Update filters with previous date range
        previous_filters['date_range'] = (previous_start.date(), previous_end.date())
    elif not filters or filters.get('date_range') is None:

        df_copy = df.copy()
        df_copy['Notification date'] = pd.to_datetime(df_copy['Notification date'], errors='coerce')
        
        # Get the most recent date in the dataset
        max_date = df_copy['Notification date'].max()
        
        # Calculate previous month range
        if pd.notna(max_date):
            previous_end = max_date - pd.Timedelta(days=30)
            previous_start = previous_end - pd.Timedelta(days=30)
            
            # Update filters with previous date range
            previous_filters['date_range'] = (previous_start.date(), previous_end.date())
    
    # Apply filters to get previous period data
    return apply_filters(df, previous_filters)