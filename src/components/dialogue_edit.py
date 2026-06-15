import streamlit as st
import pandas as pd
from datetime import datetime
from src.database.db import get_attendance_for_subject_by_date, create_attendance

@st.dialog("Adjust Attendance Record")
def edit_attendance_dialog(subject):
    st.subheader(f"✏️ Adjust Attendance: {subject['name']}")
    
    # 1. Select Date
    selected_date = st.date_input("Select Date to Audit")
    
    # 2. Fetch records
    records = get_attendance_for_subject_by_date(subject['subject_id'], selected_date.isoformat())
    
    if not records:
        st.info("No attendance records found for this date.")
    else:
        # 3. Present as editable dataframe
        df = pd.DataFrame(records)
        # We only want to show relevant columns for editing
        edit_df = st.data_editor(
            df[['student_id', 'is_present']], 
            column_config={
                "is_present": st.column_config.CheckboxColumn("Present?", default=False)
            },
            hide_index=True
        )
        
        if st.button("Save Manual Override", type="primary"):
            # 4. Process as 'Override' (Append as new history)
            overrides = []
            for _, row in edit_df.iterrows():
                overrides.append({
                    "student_id": row['student_id'],
                    "subject_id": subject['subject_id'],
                    "is_present": bool(row['is_present']),
                    "source": "Teacher-Manual-Override",
                    "timestamp": datetime.now().isoformat()
                })
            
            create_attendance(overrides)
            st.success("Adjustment saved successfully!")
            st.session_state.active_dialog = None
            st.rerun()

    if st.button("Close"):
        st.session_state.active_dialog = None
        st.rerun()