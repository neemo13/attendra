from src.database.config import supabase
import bcrypt
import streamlit as st
from datetime import datetime
import numpy as np
import json

def is_write_allowed():
    """
    Returns False if the user is a guest, preventing accidental DB modification.
    """
    if st.session_state.get('is_guest', False):
        st.warning("🔒 Guest Mode: Write actions are disabled for demo purposes.")
        return False
    return True

def get_student_by_name(name):
    """Fetches a student record by their name."""
    response = supabase.table("students").select("*").eq("name", name).execute()
    return response.data[0] if response.data else None

def verify_password(plain_password, hashed_password):
    """Verifies a plain text password against a stored hash."""
    return check_pass(plain_password, hashed_password)


def format_attendance_log(student_id, subject_id, is_present, source):
    return {
        "student_id": student_id,
        "subject_id": subject_id,
        "is_present": bool(is_present),
        "source": source,
        "timestamp": datetime.now().isoformat()
    }

def reset_attendance_state():
    st.session_state.attendance_images = []
    st.session_state.attendance_results_df = None
    st.session_state.attendance_logs = None
    st.session_state.voice_attendance_results = None
    st.session_state.open_photo_dialog = False

def hash_pass(pwd: str) -> str:
    return bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_pass(pwd: str, hashed: str) -> bool:
    return bcrypt.checkpw(pwd.encode('utf-8'), hashed.encode('utf-8'))

def check_teacher_exist(username: str) -> bool:
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0

def create_teacher(username, password, name):
    if not is_write_allowed(): return None

    hashed_password = hash_pass(password)
    data = {"username": username, "password": hashed_password, "name": name}
    response = supabase.table("teachers").insert(data).execute()
    return response.data

def teacher_login(username, password):
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher["password"]):
            return teacher
    return None

def get_all_students():
    response = supabase.table("students").select('*').execute()
    return response.data

def create_student(name, password, face_embedding, voice_embedding=None):
    if not is_write_allowed(): return None

    hashed_password = hash_pass(password) 
    
    # Ensure embedding is a standard list of 512 floats
    emb_array = np.array(face_embedding)
    if emb_array.size != 512:
        print(f"CRITICAL: Embedding size mismatch! Expected 512, got {emb_array.size}")
        return False
        
    data = {
        "name": name,
        "password": hashed_password,
        "face_embedding": emb_array.tolist(),
        "voice_embedding": voice_embedding
    }
    
    try:
        response = supabase.table("students").insert(data).execute()
        return response.data
    except Exception as e:
        print(f"Database Error: {e}")
        return False

def get_student_by_id(student_id):
    
    response = supabase.table("students").select("*").eq("student_id", student_id).execute()
    
    if response.data and len(response.data) > 0:
        return response.data[0]
    return None

def get_student_name(student_id):
    # GUEST MODE MOCKING
    if st.session_state.get('is_guest'):
        mock_names = {
            "123": "John Doe (Demo)",
            "456": "Jane Smith (Demo)"
        }
        # Use the passed argument: student_id
        return mock_names.get(str(student_id), "Unknown Student")
    
    # REAL DB LOGIC
    student = get_student_by_id(student_id)
    return student['name'] if student else "Unknown"

def create_subject(subject_code, name, section, teacher_id):
    if not is_write_allowed(): return None

    data = {
        "subject_code": subject_code,
        "name": name,
        "section": section,
        "teacher_id": teacher_id
    }
    response = supabase.table("subjects").insert(data).execute()
    return response.data

def get_teacher_subjects(teacher_id):

    if teacher_id == 'GUEST_MODE_ID':
        return [
            {
                "subject_id": 999,
                "name": "Introduction to AI",
                "subject_code": "CS103",
                "section": "A",
                "total_students": 45,
                "total_classes": 12
            },
            {
                "subject_id": 998,
                "name": "Database Systems",
                "subject_code": "DB202",
                "section": "B",
                "total_students": 32,
                "total_classes": 8
            }
        ]

    response = supabase.table("subjects") \
        .select("subject_id, name, subject_code, section") \
        .eq("teacher_id", teacher_id) \
        .execute()

    subjects = response.data

    for sub in subjects:
        # REAL-TIME student count
        count_res = supabase.table("subject_students") \
            .select("student_id", count="exact") \
            .eq("subject_id", sub["subject_id"]) \
            .execute()

        sub["total_students"] = count_res.count or 0

        # attendance classes (keep your logic)
        logs = supabase.table("attendance_logs") \
            .select("timestamp") \
            .eq("subject_id", sub["subject_id"]) \
            .execute().data

        sub["total_classes"] = len(set(l["timestamp"] for l in logs)) if logs else 0

    return subjects

def enroll_student_to_subject(student_id, subject_id):
    if not is_write_allowed(): return None

    data = {"student_id": student_id, "subject_id": subject_id}
    response = supabase.table("subject_students").insert(data).execute()
    return response.data

def unenroll_student_from_subject(student_id, subject_id):
    if not is_write_allowed(): return None

    response = supabase.table("subject_students") \
        .delete() \
        .eq("student_id", student_id) \
        .eq("subject_id", subject_id) \
        .execute()
    return response.data

def get_student_attendance(student_id):
    response = supabase.table("attendance_logs") \
        .select("is_present, subject_id, timestamp") \
        .eq("student_id", student_id) \
        .execute()
    return response.data

def get_student_subjects(student_id):
    response = supabase.table("subjects") \
        .select("subject_id, name, subject_code, section, subject_students!inner(student_id)") \
        .eq("subject_students.student_id", student_id) \
        .execute()
    return response.data

def get_attendance_for_teacher(teacher_id):
    # 1. Get IDs of subjects taught by this teacher first
    subjects = get_teacher_subjects(teacher_id)
    subject_ids = [s['subject_id'] for s in subjects]
    
    if not subject_ids:
        return []

    # 2. Query attendance logs filtered by those specific subject_ids
    # We select ONLY the primitive columns to avoid JSON blobs
    response = supabase.table("attendance_logs") \
    .select("student_id, subject_id, is_present, source, timestamp") \
    .in_("subject_id", subject_ids) \
    .execute()
        
    return response.data

def create_attendance(attendance_list):
    if not is_write_allowed(): return None
    """
    Saves/Updates attendance records using upsert to prevent duplicates.
    """
    if not attendance_list:
        return None
    try:
        # Using upsert to handle updates and inserts
        response = supabase.table("attendance_logs") \
            .upsert(attendance_list, on_conflict="student_id,subject_id,timestamp") \
            .execute()
        
        # Clear images only after successful DB action
        st.session_state.attendance_images = [] 
        return response.data
    except Exception as e:
        print(f"Error saving attendance: {e}")
        return None
    
def get_students_for_subject(subject_id):
    if st.session_state.get('is_guest'):
        # Return mock list 
        return [{"student_id": "123"}, {"student_id": "456"}]

    response = supabase.table("subject_students") \
        .select("student_id") \
        .eq("subject_id", subject_id) \
        .execute()
    return response.data

def get_subject_student_matrix(subject_id):
    """
    Fetches student embeddings using the junction table 'subject_students'
    to correctly link subjects to students.
    """
    try:
        # We query the junction table 'subject_students' 
        # and join the 'students' table to get the embedding.
        response = supabase.table("subject_students") \
            .select("student_id, students(face_embedding)") \
            .eq("subject_id", subject_id) \
            .execute()
    except Exception as e:
        print(f"Database error: {e}")
        return [], np.array([], dtype=np.float32)
    
    sids = []
    matrix = []
    
    for row in response.data:
        # Access the linked student data correctly
        student_data = row.get('students') or {}
        emb = student_data.get('face_embedding')
        sid = row.get('student_id')

        # --- DEEP INSPECTION DEBUG ---
        print(f"DEBUG: Inspecting Student {sid}")
        print(f"  - Raw type: {type(emb)}")
        
        # Handle string-serialized JSON from DB if necessary
        if isinstance(emb, str):
            try:
                emb = json.loads(emb)
                print(f"  - Converted string to list, new length: {len(emb) if isinstance(emb, list) else 'Error'}")
            except:
                print(f"  - FAILED to parse string: {emb[:30]}...")
                continue
                
        # Validate that we have a 512-dim list
        if emb is not None and isinstance(emb, (list, np.ndarray)) and len(emb) == 512:
            sids.append(row['student_id'])
            matrix.append(emb)
            print(f"  - SUCCESS: Student {sid} added.")
        else:
            sid = row.get('student_id')
            print(f"  - REJECTED: Student {sid} (Length: {len(emb) if emb is not None else 'None'})")
            
    if not matrix:
        return [], np.array([], dtype=np.float32)
            
    return sids, np.array(matrix, dtype=np.float32)

def get_attendance_for_subject_by_date(sub_id, date_str):
    """
    date_str is 'YYYY-MM-DD'. 
    We convert this to a start (00:00:00) and end (23:59:59) datetime.
    """
    start_date = f"{date_str}T00:00:00"
    end_date = f"{date_str}T23:59:59"
    
    try:
        response = supabase.table("attendance_logs") \
            .select("*") \
            .eq("subject_id", sub_id) \
            .gte("timestamp", start_date) \
            .lte("timestamp", end_date) \
            .execute()
            
        return response.data
    except Exception as e:
        print(f"DEBUG: Error: {e}")
        return []