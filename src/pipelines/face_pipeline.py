import face_recognition
import numpy as np
from src.database.db import get_all_students

def get_face_embeddings(image_np):
    locs = face_recognition.face_locations(np.ascontiguousarray(image_np), model="hog")
    encs = face_recognition.face_encodings(np.ascontiguousarray(image_np), known_face_locations=locs)
    return [np.array(e) for e in encs]

def verify_student(image_np):
    current_encodings = get_face_embeddings(image_np)
    if not current_encodings: return None
    
    student_db = get_all_students()
    for student in student_db:
        if "face_embedding" not in student: continue
        saved_enc = np.array(student.get("face_embedding"))
        dist = np.linalg.norm(saved_enc - current_encodings[0])
        # This print will appear once per check in your terminal
        print(f"DEBUG: Comparing against {student.get('name')}. Distance: {dist:.4f}")
        if dist <= 0.6:
            return student
    return None