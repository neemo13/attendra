import numpy as np
import io
import librosa
import streamlit as st
from resemblyzer import VoiceEncoder, preprocess_wav

@st.cache_resource
def get_encoder():
    return VoiceEncoder()

def get_optimized_candidates_matrix(candidates_dict):
    """Returns sids, matrix (NORMALISED), and the dimensionality."""
    sids = []
    embeddings = []
    
    if not candidates_dict: return [], np.array([]), 0
    
    # Pre-determine dimension
    first_emb = np.array(list(candidates_dict.values())[0]).flatten()
    dim = first_emb.shape[0]
    
    for sid, e in candidates_dict.items():
        emb = np.array(e).flatten()
        if emb.shape[0] == dim:
            # IMPORTANT: Normalize during matrix creation
            norm = np.linalg.norm(emb)
            embeddings.append(emb / norm if norm > 0 else emb)
            sids.append(sid)
            
    return sids, np.array(embeddings), dim

def identify_speaker(new_embedding, sids, matrix, dim):
    """Compares normalized embedding against normalized matrix."""
    new_emb = np.array(new_embedding).flatten()
    norm_new = new_emb / (np.linalg.norm(new_emb) + 1e-10)
    
    # With both matrix and new_emb normalized:
    # Cosine Distance = 1 - (Matrix @ new_emb)
    # Euclidean Distance = sqrt(2 - 2 * (Matrix @ new_emb))
    
    similarities = matrix @ norm_new 
    best_idx = np.argmax(similarities)
    
    # Return similarity score (higher is better)
    # We use this regardless of dimension to simplify the thresholding
    return sids[best_idx], float(similarities[best_idx]), "similarity"

def identify_speaker_bulk(new_embeddings, sids, matrix, threshold=0.65):
    """
    new_embeddings: array of shape (N_segments, 256)
    matrix: array of shape (N_students, 256)
    """
    # Matrix multiplication: (N_segments, 256) @ (256, N_students) -> (N_segments, N_students)
    similarities = new_embeddings @ matrix.T
    
    # Get best match index for each segment
    best_indices = np.argmax(similarities, axis=1)
    best_scores = np.max(similarities, axis=1)
    
    results = {}
    for i, score in enumerate(best_scores):
        if score >= threshold:
            sid = sids[best_indices[i]]
            # Store only the highest score for this student
            if sid not in results or score > results[sid]:
                results[sid] = float(score)
    return results

def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.35):
    """
    Processes audio using Cosine Distance (Lower is better).
    Threshold should be around 0.3 - 0.4.
    """
    try:
        encoder = get_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        segments = librosa.effects.split(audio, top_db=20) 
        
        sids, matrix, dim = get_optimized_candidates_matrix(candidates_dict)
        if dim == 0: return {}
        
        results = {}
        for start, end in segments:
            if (end - start) < sr * 0.2: continue 
            
            wav = preprocess_wav(audio[start:end])
            raw_emb = encoder.embed_utterance(wav).flatten()
            norm_emb = raw_emb / (np.linalg.norm(raw_emb) + 1e-10)
            
            # Calculate Cosine Similarity
            similarities = matrix @ norm_emb 
            
            # Convert to Cosine Distance: (1 - similarity)
            distances = 1.0 - similarities
            
            for i, sid in enumerate(sids):
                dist = float(distances[i])
                print(f"DEBUG: Segment {start}-{end} | Student: {sid} | Distance: {dist:.4f}")
                
                # LOOK FOR LOWEST DISTANCE
                if dist <= threshold:
                    # If student not in results OR we found a closer distance
                    if sid not in results or dist < results[sid]:
                        results[sid] = dist
                    
        print(f"DEBUG: Final Matched Students: {list(results.keys())}")
        return results

    except Exception as e:
        print(f"DEBUG CRITICAL ERROR: {e}")
        return {}