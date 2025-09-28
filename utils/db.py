import os
import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = os.path.join('.', 'database', 'TESt_dashboard.db')
TABLE_1 = 'PM_data'
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

@st.cache_resource
def init_db():
    """ Initiate database and create tables """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_1} (
            ID INTEGER,
            Notification_date TEXT,
            Notify_by TEXT,
            Work_Order_Status TEXT,
            Notification_type TEXT,
            StationList TEXT,
            MachineList TEXT,
            EquipmentList TEXT,
            Equipment_Group TEXT,
            Equipment_Part TEXT,
            Malfunction_Start_Date TEXT,
            Mulfunction_Stop_Date TEXT,
            MTTR REAL,
            Breakdown_Type TEXT,
            Problem_type TEXT,
            Problem_Cause TEXT,
            Activity_Code TEXT,
            Activity TEXT,
            Activity_by_1 TEXT,
            Activity_by_Vendor TEXT,
            Activity_by_3 TEXT,
            Activity_by_4 TEXT,
            Activity_Start_Date TEXT,
            Activity_Stop_Date TEXT,
            Activity_Duration REAL,
            Breakdown_Hour REAL,
            __PowerAppsId__ TEXT,
            Creator_Email TEXT,
            Modified TEXT,
            Modified_By TEXT,
            LOTO TEXT,
            LOTO_Date_Time_Start TEXT,
            LOTO_Date_Time_End TEXT,
            ActivityCount INTEGER,
            Vendor_Name TEXT,
            Message TEXT,
            Plan_Date_Time_Start TEXT,
            Plan_Date_Time_End TEXT,
            Item_Type TEXT,
            Path TEXT
        )
    ''')
    conn.commit()
    conn.close()

def append_db(df):
    """ Append data to database """

    if df.empty:
        return
    
    conn = sqlite3.connect(DB_PATH)
    
    # Rename columns to match database schema 
    df_clean = df.copy()
    df_clean.columns = [col.replace(' ', '_').replace('/', '_').replace('?', '') for col in df_clean.columns]
    
    # Replace data
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM {TABLE_1}')
    conn.commit()
    
    df_clean.to_sql(TABLE_1, conn, if_exists='append', index=False)
    conn.close()

def load_db():
    """ Load data from database """

    if not os.path.exists(DB_PATH):
        return pd.DataFrame()
    
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(f'SELECT * FROM {TABLE_1}', conn)
    except:
        df = pd.DataFrame()
    conn.close()
    
    if df.empty:
        return df
    
    # Rename columns back to original format 
    column_mapping = {
        'Notification_date': 'Notification date',
        'Notify_by': 'Notify by',
        'Work_Order_Status': 'Work Order Status',
        'Notification_type': 'Notification type',
        'Equipment_Part': 'Equipment Part',
        'Problem_type': 'Problem type',
        'Problem_Cause': 'Problem Cause',
        'Activity_by_1': 'Activity by 1',
        'Activity_Duration': 'Activity Duration',
        'Activity_Code': 'Activity Code',
        'Breakdown_Type': 'Breakdown Type',
        'Breakdown_Hour': 'Breakdown Hour',
        'Creator_Email': 'Creator Email',
        'Modified_By': 'Modified By',
        'Activity_by_Vendor': 'Activity by Vendor',
        'Activity_by_3': 'Activity by 3',
        'Activity_by_4': 'Activity by 4',
        'Vendor_Name': 'Vendor Name',
        'Plan_Date_Time_Start': 'Plan Date/Time Start',
        'Plan_Date_Time_End': 'Plan Date/Time End',
        'Item_Type': 'Item Type',
        'LOTO_Date_Time_Start': 'LOTO Date_Time Start',
        'LOTO_Date_Time_End': 'LOTO Date_Time End',
        'Malfunction_Start_Date': 'Malfunction Start Date',
        'Mulfunction_Stop_Date': 'Malfunction Stop Date',
        'Activity_Start_Date': 'Activity Start Date',
        'Activity_Stop_Date': 'Activity Stop Date'
    }
    
    df = df.rename(columns=column_mapping)
    return df

def total_record():
    """ Get total record count from database """
    
    if not os.path.exists(DB_PATH):
        return 0
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(f'SELECT COUNT(*) FROM {TABLE_1}')
        count = cursor.fetchone()[0]
    except:
        count = 0
    conn.close()
    return count
