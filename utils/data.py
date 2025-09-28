import streamlit as st
import pandas as pd
from utils.db import load_db

@st.cache_data
def preprocess_data():
    """ Load and preprocess data from database """
    
    df = load_db()
    
    if df.empty:
        return df
    
    # Data preprocessing
    columns = [
        'Notification date', 
        'Malfunction Start Date', 
        'Malfunction Stop Date',
        'Activity Start Date',
        'Activity Stop Date'
        ]
    try:
        df[columns] = df[columns].apply(pd.to_datetime, format='%m/%d/%Y %H:%M')
    except Exception:
        df[columns] = df[columns].apply(pd.to_datetime, errors='coerce')

    # Fill missing values
    columns = [
        'StationList', 
        'MachineList', 
        'Equipment Part', 
        'Problem type', 
        'Activity by 1'
        ]
    df[columns] = df[columns].fillna('Unknown')

    # Convert numeric columns
    num_columns = [
        'MTTR', 
        'Activity Duration', 
        'Breakdown Hour', 
        'ActivityCount'
        ]
    df[num_columns] = df[num_columns].apply(pd.to_numeric, errors='coerce').fillna(0)

    return df

