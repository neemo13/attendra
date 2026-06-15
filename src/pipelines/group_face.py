import streamlit as st
import numpy as np
from PIL import Image
from insightface.app import FaceAnalysis

@st.cache_resource
def get_group_face_app():
    app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider']) 
    app.prepare(ctx_id=0, det_size=(640, 640))
    return app


def process_group_photo(img_np, sids, matrix, threshold=1.4):
    """
    Processes a group photo with high-res resizing and diagnostic output.
    """
    app = get_group_face_app()
    
    # 1. Image Resizing for Detection (Fixes high-res detection failure)
    h, w = img_np.shape[:2]
    max_dim = 1280
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        new_w, new_h = int(w * scale), int(h * scale)
        img_pil = Image.fromarray(img_np).resize((new_w, new_h), Image.Resampling.LANCZOS)
        img_np_resized = np.array(img_pil)
    else:
        img_np_resized = img_np

    # 2. BGR Conversion
    if img_np_resized.ndim == 3 and img_np_resized.shape[2] == 3:
        img_np_final = img_np_resized[:, :, ::-1] 
    else:
        img_np_final = img_np_resized

    # 3. Detection
    faces = app.get(img_np_final)
    
    # DEBUG: If 0 faces, save the image for inspection
    if len(faces) == 0:
        print("DEBUG: InsightFace detected 0 faces. Saving debug_dump.png for inspection.")
        Image.fromarray(img_np_final).save("debug_dump.png")
    
    print(f"DEBUG: InsightFace detected {len(faces)} faces.")
    
    # 4. Filter by size
    results = [f for f in faces if (f.bbox[2]-f.bbox[0]) > 30 and (f.bbox[3]-f.bbox[1]) > 30]
    
    if not results or len(matrix) == 0:
        return set()

    identified_ids = set()
    norm_matrix = np.array(matrix, dtype=np.float32)
    norm_matrix = norm_matrix / (np.linalg.norm(norm_matrix, axis=1, keepdims=True) + 1e-10)

    # 5. Matching
    for i, face in enumerate(results):
        target_emb = face.embedding.flatten().astype(np.float32)
        target_emb = target_emb / (np.linalg.norm(target_emb) + 1e-10)
        
        distances = np.linalg.norm(norm_matrix - target_emb, axis=1)
        min_idx = np.argmin(distances)
        min_dist = distances[min_idx]
        
        print(f"DEBUG: Face {i} matched to Student {sids[min_idx]} with distance {min_dist:.4f}")
        
        if min_dist < threshold:
            identified_ids.add(sids[min_idx])
            
    return identified_ids