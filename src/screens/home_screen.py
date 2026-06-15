import streamlit as st
from src.components.header import header_home
from src.ui.base_layout import style_base_layout, style_background_home

def home_screen():
    style_base_layout()
    style_background_home()
    header_home()

    st.markdown("""
        <style>
        .block-container {
            max-width: 650px;
            margin: auto;
        }
        .spacer {
            height: 30px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            'Teacher Portal', 
            use_container_width=True, 
            type="primary", 
            key="teacher_btn",
            icon=":material/arrow_outward:",
            icon_position="right"
        ):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

        if st.button(
            'Student Portal', 
            use_container_width=True, 
            type="primary", 
            key="student_btn",
            icon=":material/arrow_outward:",
            icon_position="right"
        ):
            st.session_state['login_type'] = 'student'
            st.rerun()

        # Guest Access Button
        if st.button('Continue as Guest', use_container_width=True, key="guest_btn"):
            # Simulate a logged-in state
            st.session_state['is_logged_in'] = True
            st.session_state['login_type'] = 'teacher'
            
            # Assign a specific "Guest" ID
            st.session_state['current_teacher'] = {
                'teacher_id': 'GUEST_MODE_ID', 
                'name': 'Demo User'
            }
            # add flag
            st.session_state['is_guest'] = True 
            st.rerun()