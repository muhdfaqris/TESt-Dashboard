import streamlit as st
import plotly.express as px
import pandas as pd
from utils.calc import calculate_kpi, calculate_delta, calculate_prev
from utils.filters import create_filters, apply_filters
from utils.db import total_record
from utils.ui import hide_streamlit

st.set_page_config(layout="wide")
hide_streamlit()
st.markdown('<div style="font-size: 2rem; font-weight: bold; color: #333; margin-bottom: 1rem;">Overview</div>'
            , unsafe_allow_html=True)

df = st.session_state.df

if 'df' in st.session_state:
    filters = create_filters(st.session_state.df)
    filtered_df = apply_filters(st.session_state.df, filters)
    st.session_state.filtered_df = filtered_df
else:
    st.error("Data not found in session state. Please restart the dashboard.")
    st.stop()

filtered_df = st.session_state.filtered_df

if filtered_df.empty or total_record() == 0:
    st.warning("Database not available. Please check the **Settings** page.")
    st.stop()

current_kpi = calculate_kpi(filtered_df)

if not filters.get('date_range'):
    filtered_df_copy = filtered_df.copy()
    filtered_df_copy['Notification date'] = pd.to_datetime(filtered_df_copy['Notification date'], errors='coerce')
    valid_dates = filtered_df_copy['Notification date'].dropna()
    
    if not valid_dates.empty:
        date_min = valid_dates.min().date()
        date_max = valid_dates.max().date()
        filters_with_date = filters.copy()
        filters_with_date['date_range'] = (date_min, date_max)
        
        previous_df = calculate_prev(df, filters_with_date)
    else:
        previous_df = pd.DataFrame()
else:
    previous_df = calculate_prev(df, filters)
    
previous_kpi = calculate_kpi(previous_df) if not previous_df.empty else {}
delta_kpi = calculate_delta(current_kpi, previous_kpi, as_percentage=True)

def metric_cards():
    """ Display metric cards """

    column = st.columns(4)

    with column[0]:
        with st.container(border=True):
            st.metric(
                label="Total Work Orders",
                value=current_kpi['total_orders'],
                delta=f"{delta_kpi.get('total_orders', 0):.1f}%" if delta_kpi.get('total_orders') is not None else "0.0%",
                help="Total number of work orders"
            )

    with column[1]:
        with st.container(border=True):
            st.metric(
                label="Completion Rate",
                value=f"{current_kpi['completion_rate']:.1f}%",
                delta=f"{delta_kpi.get('completion_rate', 0):.1f}%" if delta_kpi.get('completion_rate') is not None else "0.0%",
                help="Percentage of completed work orders"
            )

    with column[2]:
        with st.container(border=True):
            st.metric(
                label="Avg MTTR (hrs)",
                value=f"{current_kpi['avg_mttr']:.2f}",
                delta=f"{delta_kpi.get('avg_mttr', 0):.1f}%" if delta_kpi.get('avg_mttr') is not None else "0.0%",
                help="Average Mean Time To Repair"
            )

    with column[3]:
        with st.container(border=True):
            st.metric(
                label="Avg Duration (hrs)",
                value=f"{current_kpi['avg_duration']:.2f}",
                delta=f"{delta_kpi.get('avg_duration', 0):.1f}%" if delta_kpi.get('avg_duration') is not None else "0.0%",
                help="Average activity duration"
            )

def workOrder_statusDist():
    """ Work Order status distribution pie chart """

    if not filtered_df.empty:
        status_counts = filtered_df['Work Order Status'].value_counts()
        
        fig_status_pie = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Work Order Status Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_status_pie.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig_status_pie, use_container_width=True)
    else:
        st.info("No status data available")

def workOrder_status():  
    """ Work Order status by notification type stacked bar chart """

    if not filtered_df.empty:
        # Create crosstab for status by type
        status_type_df = pd.crosstab(
            filtered_df['Notification type'], 
            filtered_df['Work Order Status'], 
            margins=False
        ).reset_index()
        
        # Melt for plotly
        status_melted = status_type_df.melt(
            id_vars=['Notification type'], 
            var_name='Status', 
            value_name='Count'
        )
        
        # Create stacked bar chart
        fig_status = px.bar(
            status_melted,
            x='Notification type',
            y='Count',
            color='Status',
            title="Work Order Status by Type",
            labels={'Count': 'Number of Work Orders', 'Notification type': 'Type'},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_status.update_layout(
            height=400,
            xaxis_tickangle=-45,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_status, use_container_width=True)
    else:
        st.info("No data available for status composition")

def workOrder_trend():
    """ Work Order volume trend over time """

    weekly_df = filtered_df.copy()
    weekly_df['Notification date'] = pd.to_datetime(weekly_df['Notification date'], errors='coerce')
    weekly_df = weekly_df.dropna(subset=['Notification date'])

    if not weekly_df.empty:
        weekly_df['Week'] = weekly_df['Notification date'].dt.to_period('W').dt.start_time
        
        # Group by week and notification type
        weekly_trend = weekly_df.groupby([
            'Week', 
            'Notification type'
        ]).size().reset_index(name='Count')
        
        fig_weekly = px.bar(
            weekly_trend, 
            x='Week', 
            y='Count', 
            color='Notification type',
            title="Work Order Volume Trend",
            labels={'Count': 'Number of Work Orders', 'Week': 'Week'},
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_weekly.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_weekly, use_container_width=True)
    else:
        st.info("No data available for weekly trend analysis")


def StationMachine_top():
    """ Top 10 Stations/Machines by work order volume """

    if not filtered_df.empty:

        station_machine_df = filtered_df.copy()
        
        station_machine_df['Station_Machine'] = (
            station_machine_df['StationList'].fillna('Unknown') + 
            ' - ' + 
            station_machine_df['MachineList'].fillna('No Machine')
        )
        
        top_stations = station_machine_df['Station_Machine'].value_counts().head(10).reset_index()
        top_stations.columns = ['Station_Machine', 'Count']
    
        fig_stations = px.bar(
            top_stations.sort_values('Count'),
            x='Count',
            y='Station_Machine',
            orientation='h',
            title="Top 10 Stations/Machines by Work Orders",
            labels={'Count': 'Number of Work Orders', 'Station_Machine': 'Station - Machine'},
            color='Count',
            color_continuous_scale='Blues'
        )
        fig_stations.update_layout(
            height=400,
            showlegend=False,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig_stations, use_container_width=True)
    else:
        st.info("No data available for station/machine analysis")

metric_cards()
column = st.columns([1, 1])
with column[0]:
        with st.container(border=True):
            workOrder_statusDist()
with column[1]:
    with st.container(border=True):
            workOrder_status()

with st.container(border=True):
    workOrder_trend()

