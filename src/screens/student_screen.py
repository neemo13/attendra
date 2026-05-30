import streamlit as st
from src.ui.base_layout import style_base_layout, style_base_dashboard
from src.components.header import header_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import verify_student
from src.database.db import get_student_by_id

def student_screen():
    style_base_dashboard()
    style_base_layout()
    header_dashboard(role="Student")

    st.markdown("""
        <style>
            div[data-testid="stTabs"] button p { color: #000000 !important; font-weight: bold !important; }
            h1, h2, h3 { color: #000000 !important; }
        </style>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Face ID Login", "Manual ID Login"])

    with tab1:
        st.header("Login using FACEID")
        
        if st.session_state.get("is_logged_in"):
            st.success("Successfully Logged In!")
        else:
            status_box = st.empty()
            img_file = st.camera_input("Capture face", key="face_cam")
            
            if img_file:
                status_box.info("Verifying...")
                img_np = np.array(Image.open(img_file).convert("RGB"))
                student = verify_student(img_np)
                
                if student:
                    status_box.success("Face recognized!")
                    st.session_state.update({"is_logged_in": True, "student_data": student})
                    st.rerun() 
                else:
                    status_box.error("Face not recognized.")

    with tab2:
        st.header("Manual Student Login")
        manual_id = st.text_input("Enter Student ID")
        if st.button("Login", type="primary"):
            student = get_student_by_id(manual_id)
            if student:
                st.session_state.update({"is_logged_in": True, "student_data": student})
                st.rerun()
            else:
                st.error("Invalid Student ID")