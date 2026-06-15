import streamlit as st
from src.database.db import create_attendance

# 1. This is the logic that renders the table and buttons.
# No decorator here so it can be called inside other dialogs.
def show_attendance_result(df, logs):
    st.write('Please review attendance before confirming.')
    st.dataframe(df, hide_index=True, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:

        if st.button('Discard', use_container_width=True):
            st.session_state.voice_attendance_results = None
            st.session_state.attendance_results_df = None
            st.session_state.attendance_logs = None      
            st.rerun()
            
    with col2:
        if st.button('Confirm & Save', use_container_width=True, type='primary'):
            try:
                create_attendance(logs)
                st.toast("Attendance saved successfully!")
                st.session_state.voice_attendance_results = None
                st.session_state.attendance_results_df = None 
                st.session_state.attendance_logs = None       
                st.rerun()
                
            except Exception as e:
                st.error(f'Sync failed: {e}')

# 2. This is the wrapper that your other files expect.
# It acts as a standalone popup when called from the main screen.
@st.dialog("Attendance Reports")
def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs)