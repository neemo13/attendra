from src.database.config import supabase
import bcrypt

def hash_pass(pwd: str) -> str:
    # gensalt() stays as bytes; decode the final hash back to a string for text storage
    return bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_pass(pwd: str, hashed: str) -> bool:
    # Fixed typo from .encoder() to .encode()
    return bcrypt.checkpw(pwd.encode('utf-8'), hashed.encode('utf-8'))

def check_teacher_exist(username: str) -> bool:
    # Fixed invalid .execute(0) syntax
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0

def create_teacher(username, password, name):
    hashed_password = hash_pass(password) # 🚀 Securely hash it before saving!
    data = {"username" : username, "password" : hashed_password, "name" : name}
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

def create_student(name, face_embedding, voice_embedding):
    data = {
        "name": name,
        "face_embedding": face_embedding,  # Stored as a flat list/float array
        "voice_embedding": voice_embedding # Defaults to None if they skip voice enrollment
    }
    response = supabase.table("students").insert(data).execute()
    return response.data

def get_student_by_id(student_id):
    
    students = get_all_students()
    return next((s for s in students if str(s.get("student_id")) == str(student_id)), None)