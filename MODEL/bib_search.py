"""
Bib Number Search Module using EasyOCR.
Extracts bib numbers from event photos using preprocessing + OCR.
"""

import os
import re
import cv2
import numpy as np
import easyocr

# Initialize EasyOCR reader (lazy loading)
_reader = None


def _get_reader():
    """Lazy-load the EasyOCR reader."""
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(["en"], gpu=False)
    return _reader


def preprocess_image(image: np.ndarray) -> np.ndarray:
    """
    Preprocess image for better OCR results.
    Applies CLAHE and sharpening.

    Args:
        image: Input image as numpy array (BGR).

    Returns:
        Preprocessed image as numpy array.
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Apply sharpening kernel
    sharpen_kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])
    sharpened = cv2.filter2D(enhanced, -1, sharpen_kernel)

    return sharpened


def extract_bib_number(image_path: str) -> list:
    """
    Extract potential bib numbers from an event photo.

    Args:
        image_path: Path to the event photo.

    Returns:
        List of detected number strings.
    """
    reader = _get_reader()

    img = cv2.imread(image_path)
    if img is None:
        return []

    # Preprocess
    preprocessed = preprocess_image(img)

    # Run OCR
    results = reader.readtext(preprocessed)

    # Extract numbers (bib numbers are typically numeric)
    bib_numbers = []
    for _, text, confidence in results:
        # Clean the text and look for numeric patterns
        cleaned = re.sub(r"[^0-9]", "", text)
        if cleaned and len(cleaned) >= 1 and confidence > 0.3:
            bib_numbers.append(cleaned)

    return bib_numbers


def process_event_photos(event_dir: str) -> dict:
    """
    Batch process all photos in an event directory.
    Extracts bib numbers from each photo.

    Args:
        event_dir: Path to the event photo directory.

    Returns:
        Dict mapping filename to list of detected bib numbers:
        {"photo1.jpg": ["123", "456"], ...}
    """
    metadata = {}
    supported_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

    if not os.path.exists(event_dir):
        return metadata

    for filename in os.listdir(event_dir):
        ext = os.path.splitext(filename)[1].lower()
        if ext not in supported_extensions:
            continue

        photo_path = os.path.join(event_dir, filename)

        try:
            bib_numbers = extract_bib_number(photo_path)
            if bib_numbers:
                metadata[filename] = bib_numbers
        except Exception:
            # Skip photos that can't be processed
            continue

    return metadata


def search_by_bib(bib_number: str, event_dir: str) -> list:
    """
    Search for photos containing a specific bib number.

    Args:
        bib_number: The bib number to search for.
        event_dir: Path to the event photo directory.

    Returns:
        List of dicts with matching photo info:
        [{"filename": str, "detected_numbers": list, "event_dir": str}, ...]
    """
    metadata = process_event_photos(event_dir)
    matches = []

    for filename, detected_numbers in metadata.items():
        # Check if the bib number matches any detected number
        for detected in detected_numbers:
            if bib_number in detected or detected in bib_number:
                matches.append(
                    {
                        "filename": filename,
                        "detected_numbers": detected_numbers,
                        "event_dir": os.path.basename(event_dir),
                    }
                )
                break

    return matches


def search_all_events(bib_number: str, photos_base_dir: str) -> list:
    """
    Search for a bib number across all event directories.

    Args:
        bib_number: The bib number to search for.
        photos_base_dir: Base path to the PHOTOS directory.

    Returns:
        List of matches across all events.
    """
    all_matches = []

    if not os.path.exists(photos_base_dir):
        return all_matches

    for event_dir_name in os.listdir(photos_base_dir):
        event_dir_path = os.path.join(photos_base_dir, event_dir_name)

        if not os.path.isdir(event_dir_path):
            continue

        event_matches = search_by_bib(bib_number, event_dir_path)
        all_matches.extend(event_matches)

    return all_matches
