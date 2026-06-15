import streamlit as st
from src.database.db import create_subject

@st.dialog("Create New Subject")
def create_subject_dialogue(teacher_id):

    st.write("Enter the details of the new subject:")
    sub_id = st.text_input("Subject Code", placeholder="CS101")
    sub_name = st.text_input("Subject Name", placeholder="Introduction to Computer Science")
    sub_section = st.text_input("Section", placeholder="A")

    if st.session_state.get('is_guest', False):
        st.warning("Guest Mode: You cannot create subjects.")
        
    else:
        if st.button("Create Subject Now", type='primary', use_container_width=True):
            if sub_id and sub_name and sub_section:
                try:
                    create_subject(sub_id, sub_name, sub_section, teacher_id)
                    st.success("Subject Created!")
                    # Reset dialog state to close it
                    st.session_state.active_dialog = None
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please fill all the fields")