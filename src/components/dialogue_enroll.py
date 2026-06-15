import streamlit as st
import time
from src.database.db import enroll_student_to_subject, supabase

@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.write("Enter the subject code provided by your teacher to enroll.")
    join_code = st.text_input('Subject Code', placeholder='Eg. CS101')

    # Guest
    if st.session_state.get('is_guest', False):
        st.button("Enroll now", disabled=True, use_container_width=True)
        st.info("Guest Mode: Enrollment is disabled.")

    else:

        if st.button('Enroll now', type='primary', use_container_width=True):
            if join_code:
                # 1. Look up the subject
                res = supabase.table('subjects').select('subject_id, name, subject_code').eq('subject_code', join_code).execute()
                
                if res.data:
                    subject = res.data[0]
                    student_id = st.session_state.student_data['student_id']
                    
                    # 2. Check if already enrolled
                    check = supabase.table('subject_students').select('*')\
                        .eq('subject_id', subject['subject_id'])\
                        .eq('student_id', student_id).execute()
                    
                    if check.data:
                        st.warning("You are already enrolled in this subject!")
                    else:
                        # 3. Perform enrollment
                        enroll_student_to_subject(student_id, subject['subject_id'])
                        st.success(f"Successfully enrolled in {subject['name']}!")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.error("Subject code not found. Please check and try again.")
            else:
                st.warning("Please enter a subject code.")