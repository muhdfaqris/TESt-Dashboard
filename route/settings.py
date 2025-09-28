import os
import streamlit as st
import pandas as pd
from utils.db import init_db, append_db, total_record, load_db
from utils.ui import hide_streamlit

st.set_page_config(layout="wide")
hide_streamlit()
st.markdown('<div style="font-size: 2rem; font-weight: bold; color: #333; margin-bottom: 1rem;">Settings</div>'
            , unsafe_allow_html=True)

init_db()

# Current database status
record_count = total_record()

if record_count > 0:
    st.success(f"Database: {record_count} records ")
    # Load and show preview
    try:
        df = load_db()
    except Exception as e:
        st.error(f"Error reading database: {str(e)}")

st.subheader(":material/file_upload: Import Data (.csv)")
st.markdown("**Note:** Uploading a new file will overwrite all existing data in the database")

uploaded_file = st.file_uploader(
    "Choose CSV file",
    type=['csv'],
    help="Select a CSV file to import into the database"
)

if uploaded_file is not None:
    try:
        preview_df = pd.read_csv(uploaded_file)
        st.subheader("Upload Preview")
        st.info(f"Records: {len(preview_df)} | Columns: {len(preview_df.columns)}")
        st.dataframe(preview_df.head(5), width='stretch')
        
        if st.button("Confirm Upload & Save to Database"):
            # Reset file pointer
            uploaded_file.seek(0)

            imported_df = pd.read_csv(uploaded_file)
            append_db(imported_df)
            st.success("Data uploaded successfully to database!")
            
            # Update session state with new data
            new_df = load_db()

            st.session_state.df = new_df
            st.cache_data.clear()
            st.rerun()
            
    except Exception as e:
        st.error(f"Error reading uploaded file: {str(e)}")

DB_PATH = 'dashboard.db'
if os.path.exists(DB_PATH):
    file_size = os.path.getsize(DB_PATH) / (1024 * 1024)
    st.markdown(f"**Database Path**: {DB_PATH} ({file_size:.2f} MB)")
