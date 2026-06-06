"""
Face Search Module using ArcFace (insightface).
Generates face embeddings and compares selfie against event photos.
"""

import os
import numpy as np
import cv2
from insightface.app import FaceAnalysis

# Initialize ArcFace model (lazy loading)
_face_app = None


def _get_face_app():
    """Lazy-load the ArcFace face analysis model."""
    global _face_app
    if _face_app is None:
        _face_app = FaceAnalysis(
            name="buffalo_l", providers=["CPUExecutionProvider"]
        )
        _face_app.prepare(ctx_id=-1, det_size=(640, 640))
    return _face_app


def get_face_embedding(image_path: str) -> np.ndarray:
    """
    Extract face embedding from an image using ArcFace.

    Args:
        image_path: Path to the image file.

    Returns:
        512-dimensional face embedding as numpy array.

    Raises:
        ValueError: If no face is detected in the image.
    """
    app = _get_face_app()
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    faces = app.get(img)

    if len(faces) == 0:
        raise ValueError("No face detected in the image")

    # Return the embedding of the largest face (most prominent)
    largest_face = max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))
    return largest_face.embedding


def get_all_face_embeddings(image_path: str) -> list:
    """
    Extract all face embeddings from an image.

    Args:
        image_path: Path to the image file.

    Returns:
        List of dicts with 'embedding' and 'bbox' keys.
    """
    app = _get_face_app()
    img = cv2.imread(image_path)

    if img is None:
        return []

    faces = app.get(img)

    return [
        {
            "embedding": face.embedding,
            "bbox": face.bbox.tolist(),
        }
        for face in faces
    ]


def cosine_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """Compute cosine similarity between two embeddings."""
    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(dot_product / (norm1 * norm2))


def compare_faces(selfie_path: str, event_photos_dir: str, threshold: float = 0.3) -> list:
    """
    Compare a selfie against all event photos and return matches.

    Args:
        selfie_path: Path to the selfie image.
        event_photos_dir: Path to directory containing event photos.
        threshold: Minimum similarity score to consider a match.

    Returns:
        List of dicts sorted by similarity score (descending):
        [{"filename": str, "similarity": float, "event_dir": str}, ...]
    """
    # Get selfie embedding
    selfie_embedding = get_face_embedding(selfie_path)

    matches = []
    supported_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

    # Iterate through event photos
    for filename in os.listdir(event_photos_dir):
        ext = os.path.splitext(filename)[1].lower()
        if ext not in supported_extensions:
            continue

        photo_path = os.path.join(event_photos_dir, filename)

        try:
            face_data_list = get_all_face_embeddings(photo_path)

            for face_data in face_data_list:
                similarity = cosine_similarity(
                    selfie_embedding, face_data["embedding"]
                )

                if similarity >= threshold:
                    matches.append(
                        {
                            "filename": filename,
                            "similarity": round(similarity, 4),
                            "event_dir": os.path.basename(event_photos_dir),
                        }
                    )
                    break  # One match per photo is enough

        except Exception:
            # Skip photos that can't be processed
            continue

    # Sort by similarity (highest first)
    matches.sort(key=lambda x: x["similarity"], reverse=True)
    return matches


def search_all_events(selfie_path: str, photos_base_dir: str, threshold: float = 0.3) -> list:
    """
    Search across all event directories for matching faces.

    Args:
        selfie_path: Path to the selfie image.
        photos_base_dir: Base path to the PHOTOS directory.
        threshold: Minimum similarity score.

    Returns:
        List of matches across all events, sorted by similarity.
    """
    all_matches = []

    if not os.path.exists(photos_base_dir):
        return all_matches

    for event_dir_name in os.listdir(photos_base_dir):
        event_dir_path = os.path.join(photos_base_dir, event_dir_name)

        if not os.path.isdir(event_dir_path):
            continue

        event_matches = compare_faces(selfie_path, event_dir_path, threshold)
        all_matches.extend(event_matches)

    # Sort all matches by similarity
    all_matches.sort(key=lambda x: x["similarity"], reverse=True)
    return all_matches
