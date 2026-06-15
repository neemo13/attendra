import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase

@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):
    # Retrieve student context from session
    student_data = st.session_state.get('student_data')
    
    # GUEST CHECK: Guests shouldn't be enrolling in classes
    if st.session_state.get('is_guest', False):
        st.warning("🔒 Guest Mode: Enrollment is disabled.")
        if st.button('Close'):
            st.session_state.pop("pending_join_code", None)
            st.rerun()
        return

    if not student_data:
        st.error("Student session lost. Please log in again.")
        return

    student_id = student_data['student_id']

    # 1. Fetch Subject
    res = supabase.table('subjects').select('subject_id, name').eq('subject_code', subject_code).execute()
    
    if not res.data:
        st.error('Subject Code not found!')
        if st.button('Close'):
            st.session_state.pop("pending_join_code", None)
            st.rerun()
        return

    subject = res.data[0]
    subject_id = subject['subject_id']

    # 2. Check existing enrollment
    check = supabase.table('subject_students').select('*').eq('subject_id', subject_id).eq('student_id', student_id).execute()
    
    if check.data:
        st.info('You are already enrolled in this subject!')
        if st.button('Got it!'):
            st.session_state.pop("pending_join_code", None)
            st.rerun()
        return

    # 3. Confirmation UI
    st.markdown(f'### Enroll in {subject["name"]}?')
    st.write(f"Would you like to enroll in **{subject['name']}** ({subject_code})?")

    col1, col2 = st.columns(2)
    with col1:
        if st.button('No', use_container_width=True):
            st.session_state.pop("pending_join_code", None)
            st.rerun()
    with col2:
        # The logic here is protected by the 'is_guest' check at the top
        if st.button('Yes, Enroll Me!', type="primary", use_container_width=True):
            enroll_student_to_subject(student_id, subject_id)
            st.success("Successfully enrolled!")
            st.session_state.pop("pending_join_code", None)
            st.rerun()