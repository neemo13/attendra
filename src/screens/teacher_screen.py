import streamlit as st
import time
import numpy as np
import pandas as pd
from datetime import datetime

# UI & Database imports
from src.ui.base_layout import style_base_layout, style_base_dashboard
from src.components.header import header_dashboard
from src.components.subject_card import subject_card
from src.database.db import (
    check_teacher_exist, create_teacher, teacher_login, 
    get_teacher_subjects, get_attendance_for_teacher, get_students_for_subject,
    create_attendance, format_attendance_log, get_student_name, 
    get_subject_student_matrix
)
from src.components.account_settings import account_settings_ui
from src.components.dialogue_add_photo import add_photos_dialog
from src.components.dialogue_voice_assistance import voice_attendance_dialog
from src.components.dialogue_edit import edit_attendance_dialog

from src.components.dialogue_create_subject import create_subject_dialogue
from src.components.dialogue_share_subject import share_subject_dialogue

# --- Helper Function for Analysis ---
def run_attendance_analysis(selected_sub):
    
    # 1. GUEST MODE MOCKING
    if st.session_state.get('is_guest'):
        with st.spinner("Analyzing photos (Demo Mode)..."):
            # Simulate a delay to make it feel real
            time.sleep(2)
            
            # Create a mock student entry
            mock_entries = [
                format_attendance_log("123", selected_sub['subject_id'], True, 'Face'),
                format_attendance_log("456", selected_sub['subject_id'], True, 'Face')
            ]
            st.session_state.attendance_master_queue.extend(mock_entries)
            st.toast("Demo scan finished! Found 2 students.")
        return

    from src.pipelines.group_face import process_group_photo

    with st.spinner("Analyzing photos..."):
        sids, matrix = get_subject_student_matrix(selected_sub['subject_id'])
        
        if matrix.size == 0:
            st.error("No valid 512-dim student embeddings found for this subject.")
            return

        new_entries = []
        for img in st.session_state.attendance_images:
            # 1. Ensure RGB and then convert to standard uint8 numpy array
            img_np = np.array(img.convert('RGB'))
            
            # 2. Diagnostic: Log data characteristics
            print(f"DEBUG: Image processing - Shape: {img_np.shape}, Range: {img_np.min()}-{img_np.max()}")
            
            # 3. Force valid range: If image was normalized (0-1), scale to 0-255
            if img_np.max() <= 1.0:
                img_np = (img_np * 255).astype(np.uint8)
            else:
                img_np = img_np.astype(np.uint8)
            
            # 4. Run Analysis
            found_ids = process_group_photo(img_np, sids, matrix)
            print(f"DEBUG: found_ids from process_group_photo: {found_ids}")
            
            # 5. Update Queue
            for sid in found_ids:
                if not any(item['student_id'] == sid for item in st.session_state.attendance_master_queue):
                    new_entries.append(format_attendance_log(sid, selected_sub['subject_id'], True, 'Face'))
        
        st.session_state.attendance_master_queue.extend(new_entries)
    
    st.toast("Scan finished!")

def teacher_screen():
    style_base_dashboard()
    style_base_layout()
    header_dashboard(role="teacher")

    # FIX: Initialize mode based on guest status immediately
    if "teacher_mode" not in st.session_state:
        if st.session_state.get("is_guest"):
            st.session_state["teacher_mode"] = "dashboard"
        else:
            st.session_state["teacher_mode"] = "login"

    # Ensure account settings only appear if NOT a guest
    if st.session_state.get("is_logged_in") and not st.session_state.get("is_guest"):
        account_settings_ui(
            st.session_state["current_teacher"],
            role="teacher"
        )

    # Routing
    views = {
        "register": teacher_screen_register,
        "login": teacher_screen_login,
        "dashboard": teacher_dashboard
    }
    
    view_func = views.get(st.session_state["teacher_mode"], teacher_screen_login)
    view_func()

# --- Auth Screens ---
def teacher_screen_register():
    st.markdown("## Register your teacher profile")
    with st.container(border=True):
        with st.form("teacher_register_form"):
            username = st.text_input("Username / Email Address", key="reg_user", placeholder="Enter username")
            name = st.text_input("Full Name", key="reg_name", placeholder="Enter name")
            p1 = st.text_input("Password", type="password", key="reg_p1", placeholder="Enter password")
            p2 = st.text_input("Confirm Password", type="password", key="reg_p2", placeholder="Enter password again")
            register = st.form_submit_button("Register Now", type="primary", use_container_width=True)

        if register:
            if not (username and name and p1 and p2): st.error("Fill all fields.")
            elif p1 != p2: st.error("Passwords do not match.")
            elif check_teacher_exist(username): st.error("User exists.")
            else:
                create_teacher(username, p1, name)
                st.session_state["teacher_mode"] = "login"
                st.rerun()
                
    st.markdown("<p style='text-align: center; margin-top: 10px;'>Already have an account?</p>", unsafe_allow_html=True)
    if st.button("Login Instead", type="secondary", use_container_width=True, icon=':material/login:'):
        st.session_state["teacher_mode"] = "login"
        st.rerun()

def teacher_screen_login():
    st.markdown("## Teacher Login")
    with st.container(border=True):
        with st.form("teacher_login_form"):
            email = st.text_input("Email", key="log_user", placeholder="Enter username/email")
            password = st.text_input("Password", type="password", key="log_p1", placeholder="Enter password")
            submit = st.form_submit_button("Login", type="primary", use_container_width=True)

        if submit:
            profile = teacher_login(email, password)
            if profile:
                st.session_state.update({
                    "current_teacher": profile,
                    "teacher_mode": "dashboard",
                    "is_logged_in": True
                })
                st.rerun()
            else: st.error("Invalid credentials.")

        st.markdown("<p style='text-align: center;'>New to Attendra?</p>", unsafe_allow_html=True)
        if st.button("Create Account", use_container_width=True):
            st.session_state["teacher_mode"] = "register"
            st.rerun()

# --- Dashboard & Tabs ---
def teacher_dashboard():
    teacher_data = st.session_state.get("current_teacher")

    if not teacher_data:
        st.error("Session expired.")
        st.session_state["teacher_mode"] = "login"
        st.rerun()

    if st.sidebar.button("Log Out", icon=':material/logout:'):
        st.session_state.pop("current_teacher", None)
        st.session_state.pop("is_guest", None)
        st.session_state.pop("is_logged_in", None)
        st.session_state["teacher_mode"] = "login"
        st.session_state["login_type"] = None # Reset to home
        st.rerun()

    st.header(f"Welcome, {teacher_data.get('name', 'Guest')}!")
    
    if "tab" not in st.session_state: st.session_state.tab = 'take_attendance'
    
    tabs = st.columns(3)
    tab_map = {
        "take_attendance": ("Take Attendance", ':material/ar_on_you:', teacher_tab_take_attendance),
        "manage_subjects": ("Manage Subjects", ':material/book_ribbon:', teacher_tab_manage_subjects),
        "attendance_records": ("Records", ':material/cards_stack:', teacher_tab_attendance_records)
    }

    for i, (key, (label, icon, func)) in enumerate(tab_map.items()):
        if tabs[i].button(label, type="primary" if st.session_state.tab == key else "tertiary", use_container_width=True, icon=icon):
            st.session_state.tab = key
            st.rerun()

    st.divider()
    tab_map[st.session_state.tab][2]()

def teacher_tab_take_attendance():
    if 'attendance_master_queue' not in st.session_state: st.session_state.attendance_master_queue = []
    if 'attendance_images' not in st.session_state: st.session_state.attendance_images = []
    if 'active_dialog' not in st.session_state: st.session_state.active_dialog = None
    
    teacher_id = st.session_state.current_teacher['teacher_id']
    subjects = get_teacher_subjects(teacher_id)
    if not subjects:  
        st.info("No subjects found.")
        return

    sub_opts = {f"{s['name']} ({s['subject_code']})": s for s in subjects}
    selected_sub = sub_opts[st.selectbox("Select Subject", list(sub_opts.keys()))]

    photo_count = len(st.session_state.attendance_images)
    photo_badge = f" ({photo_count})" if photo_count > 0 else ""

    c1, c2, c3 = st.columns(3)
    if c1.button(f"📷 Add Photos{photo_badge}", use_container_width=True):
        st.session_state.active_dialog = "photo"
        st.rerun()
    
    if c2.button("Run Face Analysis", type="primary", use_container_width=True, disabled=(photo_count == 0)):
        run_attendance_analysis(selected_sub)
        st.rerun()

    if c3.button("🎤 Voice Assistant", use_container_width=True):
        st.session_state.active_dialog = "voice"
        st.rerun()

    if st.session_state.attendance_master_queue:
        st.divider()
        st.subheader("📋 Session Attendance Queue")
        
        df = pd.DataFrame(st.session_state.attendance_master_queue)
        df['Name'] = df['student_id'].apply(get_student_name)
        df['Status'] = df['is_present'].map({True: '✅ Present', False: '❌ Absent'})
        st.dataframe(df[['Name', 'source', 'Status', 'timestamp']], use_container_width=True, hide_index=True)
        
        qc1, qc2 = st.columns(2)
        with qc1:
            if st.button("🗑️ Clear Queue", type="secondary", use_container_width=True):
                st.session_state.attendance_master_queue = []
                st.session_state.attendance_images = []
                st.rerun()  
        with qc2:
            if st.button("🚀 Confirm & Save All", type="primary", use_container_width=True):
                st.balloons()

                # 1. GUEST MODE INTERCEPTION
                if st.session_state.get('is_guest'):
                    st.success("✅ Demo Mode: Attendance saved successfully!")
                    time.sleep(1)
                    st.session_state.attendance_master_queue = []
                    st.session_state.attendance_images = []
                    st.rerun()
                    
                else:
                    enrolled = get_students_for_subject(selected_sub['subject_id'])
                    present_ids = {log['student_id'] for log in st.session_state.attendance_master_queue}
                    final_batch = []
                    batch_timestamp = datetime.now().isoformat()
                    for entry in enrolled:
                        final_batch.append({
                            "student_id": entry['student_id'],
                            "subject_id": selected_sub['subject_id'],
                            "is_present": (entry['student_id'] in present_ids),
                            "source": 'System-Final',
                            "timestamp": batch_timestamp
                        })
                    create_attendance(final_batch)
                    st.session_state.attendance_master_queue = [] 
                    st.session_state.attendance_images = []        
                    st.success("Session attendance logged cleanly!")
                    time.sleep(1.5)
                    st.rerun()
    elif not st.session_state.attendance_master_queue:
        if photo_count == 0:
            st.info("The attendance queue is empty. Upload photos or use voice assistant to begin.")

    if st.session_state.active_dialog == "photo":
        add_photos_dialog(selected_sub)
        st.stop()
    elif st.session_state.active_dialog == "voice":
        voice_attendance_dialog(selected_sub['subject_id'])
        st.stop()

def teacher_tab_manage_subjects():
    # 1. Add New Subject Button
    if st.button("+ Add New Subject", type="primary"):
        st.session_state.active_dialog = "add_subject"
        st.rerun()

    # 2. Get Data & Calculate Accurate Stats
    teacher_id = st.session_state.current_teacher['teacher_id']
    subjects = get_teacher_subjects(teacher_id)
    all_attendance = get_attendance_for_teacher(teacher_id)
    
    # Create a DataFrame for accurate counting
    df = pd.DataFrame(all_attendance)
    
    # Helper to calculate unique classes per subject (ignoring override duplicates)
    def get_unique_class_count(sub_id):
        if df.empty or 'subject_id' not in df.columns:
            return 0
        # Filter for this subject and count unique dates
        sub_df = df[df['subject_id'] == sub_id].copy()
        if sub_df.empty:
            return 0
        sub_df['timestamp'] = pd.to_datetime(sub_df['timestamp'], format='mixed')
        return sub_df['timestamp'].dt.date.nunique()

    # 3. Render Subject Cards
    for i in range(0, len(subjects), 2):
        cols = st.columns(2)
        for j, sub in enumerate(subjects[i:i+2]):
            with cols[j]:
                # Define callbacks
                def set_share(s=sub):
                    st.session_state.active_dialog = "share_subject"
                    st.session_state.shared_subject_data = s
                    st.rerun()
                
                def set_edit(s=sub):
                    st.session_state.active_dialog = "edit_attendance"
                    st.session_state.edit_subject_data = s
                    st.rerun()

                # Render Card
                subject_card(
                    sub['name'], 
                    sub['subject_code'], 
                    sub['section'], 
                    stats={
                        "students": sub.get('total_students', 0), 
                        "classes": get_unique_class_count(sub['subject_id'])
                    },
                    footer_callback=set_share,
                    edit_callback=set_edit
                )

    # 4. Render Dialogs at the end (Handles popups cleanly)
    if st.session_state.get("active_dialog") == "add_subject":
        create_subject_dialogue(teacher_id)
    elif st.session_state.get("active_dialog") == "share_subject":
        s = st.session_state.shared_subject_data
        share_subject_dialogue(s['name'], s['subject_code'])
    elif st.session_state.get("active_dialog") == "edit_attendance":
        edit_attendance_dialog(st.session_state.edit_subject_data)
                                        
def teacher_tab_attendance_records():
    # 1. FETCH DATA (MOCK OR REAL)
    if st.session_state.get('is_guest'):
        records = [
            {"student_id": "123", "subject_id": 999, "is_present": True, "timestamp": "2026-06-15T09:00:00", "source": "Face"},
            {"student_id": "456", "subject_id": 999, "is_present": False, "timestamp": "2026-06-15T09:00:00", "source": "Face"},
            {"student_id": "123", "subject_id": 998, "is_present": True, "timestamp": "2026-06-14T14:30:00", "source": "Voice"}
        ]
        subjects = get_teacher_subjects('GUEST_MODE_ID')
    else:
        records = get_attendance_for_teacher(st.session_state.current_teacher['teacher_id'])
        subjects = get_teacher_subjects(st.session_state.current_teacher['teacher_id'])
    
    if not records: 
        return st.info("No records found.")
    
    # 2. TRANSFORM DATA
    df = pd.DataFrame(records)
    sub_map = {s['subject_id']: s['name'] for s in subjects}
    
    # Populate extra columns
    df['Subject Name'] = df['subject_id'].map(sub_map)
    df['Name'] = df['student_id'].apply(get_student_name) # Uses our new mock-aware function
    df['Status'] = df['is_present'].map({True: '✅ Present', False: '❌ Absent'})
    
    # Ensure timestamp is datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df['date'] = df['timestamp'].dt.date

    # 3. DISPLAY
    st.subheader("Attendance History")
    view_type = st.radio("Organize by:", ["Recent", "Date-wise", "Subject-wise"], horizontal=True)
    
    # Sort the WHOLE dataframe first
    df = df.sort_values(by='timestamp', ascending=False)

    if view_type == "Recent":
        st.dataframe(df[['date', 'Subject Name', 'Name', 'Status', 'source']], use_container_width=True)
        
    elif view_type == "Date-wise":
        for d in sorted(df['date'].unique(), reverse=True):
            with st.expander(f"📅 {d}"): 
                st.dataframe(df[df['date'] == d][['Subject Name', 'Name', 'Status', 'source']], use_container_width=True)
                
    elif view_type == "Subject-wise":
        for sub_id in df['subject_id'].unique():
            with st.expander(f"📚 {sub_map.get(sub_id, 'Unknown')}"): 
                st.dataframe(df[df['subject_id'] == sub_id][['date', 'Name', 'Status', 'source']], use_container_width=True)
