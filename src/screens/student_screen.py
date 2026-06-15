import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd

from src.ui.base_layout import style_base_layout, style_base_dashboard
from src.components.header import header_dashboard
from src.components.dialogue_enroll import enroll_dialog
from src.pipelines.face_pipeline import verify_student, get_face_embedding
from src.database.db import (
    get_student_subjects,
    get_student_attendance,
    unenroll_student_from_subject,
    create_student,
    get_student_by_name, 
    verify_password
)
from src.components.account_settings import account_settings_ui

def clear_camera_state():
    """Wipe camera buffers when switching modes."""
    for key in ["face_cam_login", "reg_cam_register"]:
        if key in st.session_state:
            del st.session_state[key]

def student_screen():
    style_base_dashboard()
    style_base_layout()
    header_dashboard(role="student")

    # --- DASHBOARD (Strictly separated) ---
    if st.session_state.get("is_logged_in"):
        account_settings_ui(st.session_state["student_data"], role="student")
        
        student = st.session_state["student_data"]
        st.header(f"Welcome, {student['name']} 👋")
        
        c1, c2 = st.columns([4, 1])
        with c1:
            st.subheader("📚 Your Enrolled Subjects")

        with c2:
            if st.button("➕ Enroll", type="primary"):
                st.session_state.show_enroll_dialog = True
        if st.session_state.get("show_enroll_dialog"): enroll_dialog(); st.session_state.show_enroll_dialog = False

        subjects = get_student_subjects(student["student_id"])
        logs = get_student_attendance(student["student_id"])
        
        # Stats calculation
        stats_map = {sub['subject_id']: {"total": 0, "attended": 0} for sub in subjects}
        for log in logs:
            sid = log["subject_id"]
            if sid in stats_map:
                stats_map[sid]["total"] += 1
                if log.get("is_present"): stats_map[sid]["attended"] += 1

        if subjects:
            total_possible = sum(s['total'] for s in stats_map.values())
            total_attended = sum(s['attended'] for s in stats_map.values())
            overall_perc = (total_attended / total_possible * 100) if total_possible > 0 else 0
            
            # Dynamic feedback based on the 75% threshold
            msg = f"**Overall Attendance:** {total_attended}/{total_possible} classes attended ({overall_perc:.1f}%)"
            
            if overall_perc < 75:
                st.error(f"⚠️ {msg}")
            else:
                st.success(f"✅ {msg}")

            cols = st.columns(2)
            for i, sub in enumerate(subjects):
                sid = sub["subject_id"]
                stats = stats_map.get(sid, {"total": 0, "attended": 0})
                perc = (stats["attended"] / stats["total"] * 100) if stats["total"] > 0 else 0
                with cols[i % 2]:
                    st.markdown(f"""
                        <div style="border: 2px solid #D8B4FE; border-radius: 16px; padding: 15px; margin-bottom: 10px;">
                            <h4 style="margin: 0;">📖 {sub['name']}</h4>
                            <p style="margin: 5px 0;">Code: {sub['subject_code']}</p>
                            <div style="font-weight: bold; color: #7c3aed;">Attendance: {stats['attended']}/{stats['total']} ({perc:.0f}%)</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"🚫 Unenroll {sub['subject_code']}", key=f"un_{sid}"):
                        unenroll_student_from_subject(student["student_id"], sid); st.rerun()
        else: st.info("No subjects enrolled.")

        st.divider()
        st.subheader("📅 Attendance History")
        if logs:
            df = pd.DataFrame(logs)
            df['Status'] = df['is_present'].map({True: '✅ Present', False: '❌ Absent'})
            # Map subject names
            sub_map = {s['subject_id']: s['name'] for s in subjects}
            df['Subject Name'] = df['subject_id'].map(sub_map)
            df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')
            df['date'] = df['timestamp'].dt.date

            view = st.radio("View by:", ["All Records", "Sorted by Date", "Subject-wise"], horizontal=True)

            if view == "All Records":
                st.dataframe(df, use_container_width=True)
            elif view == "Sorted by Date":
                st.dataframe(df.sort_values('timestamp', ascending=False), use_container_width=True)
            elif view == "Subject-wise":
                # Grouping by subject_id to show expanders
                for sub_id in df['subject_id'].unique():
                    sub_name = sub_map.get(sub_id, "Unknown Subject")
                    with st.expander(f"📚 {sub_name}"):
                        # Filter for this subject and display
                        st.dataframe(df[df['subject_id'] == sub_id].sort_values('timestamp', ascending=False), use_container_width=True)
        else:
            st.info("No attendance records.")
        return

    # --- AUTHENTICATION FLOW ---
    if "reg_mode_trigger" not in st.session_state:
        st.session_state.reg_mode_trigger = False

    mode = st.radio(
        "Choose:", ["Login", "Register"], 
        index=1 if st.session_state.reg_mode_trigger else 0, 
        horizontal=True, key="auth_mode_radio",
        on_change=clear_camera_state
    )
    st.session_state.reg_mode_trigger = (mode == "Register")

    if not st.session_state.reg_mode_trigger:
        st.header("Login using FACEID")
        img_file = st.camera_input("Capture face", key="face_cam_login")

        if img_file and st.button("Verify Identity"):
            with st.spinner("Verifying..."):
                img_np = np.array(Image.open(img_file).convert("RGB"))
                result = verify_student(img_np)

                if result == "MULTIPLE_FACES":
                    st.error("Login failed: Multiple people detected. Please stand alone.")
                elif result:
                    st.session_state.update({"is_logged_in": True, "student_data": result})
                    st.rerun()
                else: 
                    st.error("Face not recognized. Register!")
    else:
        st.header("Student Registration")
        student_name = st.text_input("Full Name", placeholder="Enter name")
        if student_name and get_student_by_name(student_name):
            st.warning("✅ You are registered in our database. Please proceed to Login.")
        else:
            password = st.text_input("Password", type="password", placeholder= "Enter password")
            img_file = st.camera_input("Capture face for registration", key="reg_cam_register")
            st.subheader("🎙️ Voice Registration (Optional)")
            audio_file = st.audio_input("Record your voice")
            
            if st.button("Complete Registration"):
                if not student_name or not password or not img_file:
                    st.error("All fields required.")
                else:
                    with st.spinner("Processing..."):
                        img_np = np.array(Image.open(img_file).convert("RGB"))
                        emb = get_face_embedding(img_np)

                    if emb is None:
                        st.error(
                            "Registration failed: No face detected."
                        )

                    elif emb == "MULTIPLE_FACES":
                        st.error(
                            "Registration failed: Multiple faces detected. Please ensure exactly one clear face is captured."
                        )

                    else:
                        voice_emb = [0.0] * 128 if audio_file else None

                        if create_student(
                            student_name,
                            password,
                            emb.tolist(),
                            voice_emb
                        ):
                            st.success("Registered successfully!")
                            st.balloons()
                            st.session_state.reg_mode_trigger = False
                            st.rerun()
                        else:
                            st.error("Registration failed. Please try again.")