import streamlit as st
import numpy as np
import json
from insightface.app import FaceAnalysis
from src.database.db import get_all_students

@st.cache_resource
def get_face_app():
    """Caches the InsightFace model globally."""
    app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
    app.prepare(ctx_id=0, det_size=(640, 640))
    return app


def get_face_embedding(image_np):
    app = get_face_app()
    faces = app.get(image_np)

    if len(faces) == 0:
        return None

    if len(faces) > 1:
        return "MULTIPLE_FACES"

    return faces[0].embedding

def verify_student(image_np):
    # 1. Force BGR color space for InsightFace
    # If the image has 3 channels, assume RGB and flip to BGR

    app = get_face_app()
    
    if image_np.ndim == 3 and image_np.shape[2] == 3:
        image_np = image_np[:, :, ::-1]
    
    # 2. Detection
    faces = app.get(image_np)
    if not faces: 
        print("DEBUG: No face detected during login.")
        return None
    if len(faces) > 1: 
        print(f"DEBUG: Multiple faces detected: {len(faces)}")
        return "MULTIPLE_FACES"
    
    target_enc = faces[0].embedding.astype(np.float32)
    # Normalize the target embedding
    target_enc = target_enc / (np.linalg.norm(target_enc) + 1e-10)
    
    # 3. Vectorized Comparison
    student_db = get_all_students()
    if not student_db: 
        print("DEBUG: Database empty.")
        return None
    
    valid_students = []
    embeddings = []
    for s in student_db:
        emb = s.get("face_embedding")
        if isinstance(emb, str): emb = json.loads(emb)
        if emb and len(emb) == 512:
            valid_students.append(s)
            embeddings.append(emb)
    
    if not embeddings: return None
    
    matrix = np.array(embeddings, dtype=np.float32)
    # Normalize matrix rows
    matrix = matrix / (np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-10)
    
    # Calculate Euclidean distance on normalized vectors
    distances = np.linalg.norm(matrix - target_enc, axis=1)
    best_idx = np.argmin(distances)
    min_dist = distances[best_idx]
    
    print(f"DEBUG: Login match distance: {min_dist:.4f}")
    
    # 4. Final Verification
    if min_dist <= 1.2: 
        return valid_students[best_idx]
        
    return None