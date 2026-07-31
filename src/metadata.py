import os
import hashlib
from datetime import datetime


def calculate_md5(file_path):
    hash_md5 = hashlib.md5()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()


def extract_basic_metadata(pdf_path):

    metadata = {}

    metadata["file_path"] = pdf_path
    metadata["filename"] = os.path.basename(pdf_path)
    metadata["file_size_bytes"] = os.path.getsize(pdf_path)
    metadata["md5_hash"] = calculate_md5(pdf_path)
    metadata["processed_at"] = str(datetime.now())

    return metadata