def build_metadata(basic_metadata, pdf_json):

    metadata = {
        "file_path": basic_metadata["file_path"],
        "filename": basic_metadata["filename"],
        "source_folder": basic_metadata["file_path"].rsplit("\\", 1)[0],
        "file_size_bytes": basic_metadata["file_size_bytes"],
        "md5_hash": basic_metadata["md5_hash"],

        "title": pdf_json.get("title", ""),
        "author": pdf_json.get("author", ""),
        "publisher": pdf_json.get("publisher", ""),
        "subject": pdf_json.get("subject", ""),
        "keywords": pdf_json.get("keywords", ""),
        "creation_date": pdf_json.get("creation_date", ""),
        "language": pdf_json.get("language", ""),
        "page_count": pdf_json.get("page_count", 0),

        "has_toc": False,
        "pdf_version": pdf_json.get("pdf_version", ""),
        "is_encrypted": pdf_json.get("is_encrypted", False),
        "is_corrupted": False,
        "is_parseable": True,
        "is_scanned_only": False,

        "first_page_char_count": 0,
        "text_sample": "",

        "license_detected": "",
        "license_source": "",
        "license_confidence": 0.0,

        "quality_tier": "",
        "exclude_from_training": False,
        "exclusion_reason": "",

        "processed_at": basic_metadata["processed_at"],
        "processing_error": ""
    }

    return metadata