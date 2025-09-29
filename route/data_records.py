import streamlit as st 
import pandas as pd
from utils.ui import hide_streamlit_css

st.set_page_config(layout="wide")
hide_streamlit_css()
st.markdown('<div style="font-size: 2rem; font-weight: bold; color: #333; margin-bottom: 1rem;">Data Records</div>'
            , unsafe_allow_html=True)

df = st.session_state.df

col1, col2 = st.columns([6, 0.5])

with col1:
    search_term = st.text_input(
        "search_input",
        placeholder="Search by any field...",
        help="Enter keywords to filter the table. Search is case-insensitive.",
        label_visibility="collapsed",
        key="my_search"
    )

with col2:
    search_clicked = st.button(
        ":material/search:",
        type="primary",
        help="Apply search filter",
        width='stretch'
    )

display_df = df.copy()

if search_term:
    search_columns = [
        'ID', 'Activity', 'StationList', 'MachineList', 'EquipmentList', 
        'Equipment Group', 'Equipment Part', 'Problem type', 'Problem Cause',
        'Notify by', 'Activity by 1', 'Vendor Name', 'Work Order Status',
        'Notification type', 'Breakdown Type', 'Message'
    ]
    
    # Create search mask
    search_mask = pd.Series([False] * len(display_df))
    
    for col in search_columns:
        if col in display_df.columns:
            # Convert to string and search case-insensitively
            col_mask = display_df[col].astype(str).str.contains(
                search_term, case=False, na=False, regex=False
            )
            search_mask = search_mask | col_mask
    
    display_df = display_df[search_mask]
    
    # Show search results count
    search_results = len(display_df)
    if search_results > 0:
        st.info(f"Found {search_results} records matching '{search_term}'")
    else:
        st.warning(f"No records found matching '{search_term}'")

# Select columns to display in table
table_columns = [
    'ID', 
    'Work Order Status',
    'Notification type',
    'Notification date',
    'StationList',
    'MachineList', 
    'EquipmentList',
    'Equipment Group',
    'Equipment Part',
    'MTTR',
    'Activity Duration',
    'Problem type',
    'Problem Cause',
    'Activity',
    'Activity by 1',
    'Vendor Name',
    'Malfunction Start Date',
    'Mulfunction Stop Date',
    'Activity Start Date',
    'Activity Stop Date',
    'Modified',
    'Modified By'
]

# Filter columns that exist in dataframe
available_columns = [col for col in table_columns if col in display_df.columns]

if not display_df.empty:
    st.dataframe(
        display_df[available_columns],
        width='stretch',
        height=600,
        column_config={
            "ID": st.column_config.NumberColumn(
                "Work Order ID",
                help="Unique work order identifier",
                format="%d"
            ),
            "MTTR": st.column_config.NumberColumn(
                "MTTR (hrs)",
                help="Mean Time To Repair in hours",
                format="%.2f"
            ),
            "Activity Duration": st.column_config.NumberColumn(
                "Duration (hrs)", 
                help="Activity duration in hours",
                format="%.2f"
            ),
            "Notification date": st.column_config.DatetimeColumn(
                "Notification Date",
                help="Date when work order was created"
            ),
            "Work Order Status": st.column_config.TextColumn(
                "Status",
                help="Current status of work order"
            ),
            "StationList": st.column_config.TextColumn(
                "Station",
                help="Station where work was performed"
            ),
            "MachineList": st.column_config.TextColumn(
                "Machine", 
                help="Machine involved in work order"
            ),
            "EquipmentList": st.column_config.TextColumn(
                "Equipment",
                help="Equipment involved in work order"
            )
        },
        hide_index=True
    )
    
    st.download_button(
        label="Export to CSV",
        data=display_df[available_columns].to_csv(index=False),
        file_name=f"work_orders_filtered_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        help="Download the currently displayed data as CSV file"
    )
    
else:
    st.warning("No records to display")
