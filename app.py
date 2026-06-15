import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import streamlit as st

st.set_page_config(page_title="ATTENDRA", layout="centered", page_icon= "src/ui/logo.jpg")

def init_session_state():
    defaults = {
        "attendance_images": [],
        "attendance_results_df": None,
        "attendance_logs": None,
        "voice_attendance_results": None,
        "open_photo_dialog": False,
        "login_type": None,
        "is_logged_in": False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def main():
    init_session_state()
    

    # 1. IMMEDIATE PARAMETER CAPTURE
    if "join" in st.query_params:
        st.session_state["pending_join_code"] = st.query_params["join"]
        st.session_state["login_type"] = 'student'
        st.query_params.clear()
        st.rerun()

    login_type = st.session_state.get('login_type')

    # Force student mode if a join code was captured
    if st.session_state.get("pending_join_code") and login_type != 'student':
        st.session_state["login_type"] = 'student'
        st.rerun()

    if login_type != 'teacher':
        st.session_state.pop("teacher_mode", None)

    # 2. LAZY LOAD SCREENS (Imports happen only when needed)
    if login_type == 'teacher':
        from src.screens.teacher_screen import teacher_screen
        teacher_screen()
        
    elif login_type == 'student':
        from src.screens.student_screen import student_screen
        from src.components.dialogue_auto_enroll import auto_enroll_dialog
        
        if st.session_state.get("is_logged_in") and st.session_state.get("pending_join_code"):
            auto_enroll_dialog(st.session_state["pending_join_code"])
        else:
            student_screen()
            
    else:
        from src.screens.home_screen import home_screen
        home_screen()

if __name__ == "__main__":
    main()