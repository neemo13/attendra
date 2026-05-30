import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

st.set_page_config(
    page_title="ATTENDRA",
    layout="centered"
)

from src.screens.home_screen import home_screen
from src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_screen

def main():
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()

        case 'student':
            student_screen()

        case None:
            home_screen()

if __name__ == "__main__":
    main()