import os
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

METADATA_DIR = os.path.join(BASE_DIR, "METADATA")

os.makedirs(METADATA_DIR, exist_ok=True)

FACE_METADATA_FILE = os.path.join(
    METADATA_DIR,
    "face_embeddings.pkl"
)

BIB_METADATA_FILE = os.path.join(
    METADATA_DIR,
    "bib_metadata.pkl"
)


def load_face_metadata():

    if not os.path.exists(FACE_METADATA_FILE):
        return []

    with open(FACE_METADATA_FILE, "rb") as f:
        return pickle.load(f)


def save_face_metadata(data):

    with open(FACE_METADATA_FILE, "wb") as f:
        pickle.dump(data, f)


def load_bib_metadata():

    if not os.path.exists(BIB_METADATA_FILE):
        return []

    with open(BIB_METADATA_FILE, "rb") as f:
        return pickle.load(f)


def save_bib_metadata(data):

    with open(BIB_METADATA_FILE, "wb") as f:
        pickle.dump(data, f)