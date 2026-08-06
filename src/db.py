import os
import re
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Try importing psycopg2
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False


def get_db_config():
    """Retrieve PostgreSQL connection parameters from environment variables."""
    return {
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": int(os.getenv("POSTGRES_PORT", 5432)),
        "dbname": os.getenv("POSTGRES_DB", "postgres"),
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", "postgres")
    }


def get_db_connection():
    """Establish and return a PostgreSQL database connection."""
    if not PSYCOPG2_AVAILABLE:
        raise ImportError(
            "psycopg2 module is not installed. Please install it using: pip install psycopg2-binary"
        )

    config = get_db_config()
    return psycopg2.connect(**config)


def init_db():
    """Initialize PostgreSQL database table and indexes."""
    if not PSYCOPG2_AVAILABLE:
        print("[WARN] psycopg2 unavailable; skipping DB initialization.")
        return False

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        schema_sql = """
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            filename VARCHAR(255) NOT NULL UNIQUE,
            file_path TEXT NOT NULL,
            source_folder TEXT,
            file_size_bytes BIGINT,
            md5_hash VARCHAR(32),
            title TEXT,
            author TEXT,
            publisher TEXT,
            subject TEXT,
            keywords TEXT,
            creation_date VARCHAR(100),
            language VARCHAR(50),
            page_count INT,
            has_toc BOOLEAN DEFAULT FALSE,
            pdf_version VARCHAR(50),
            is_encrypted BOOLEAN DEFAULT FALSE,
            is_corrupted BOOLEAN DEFAULT FALSE,
            is_parseable BOOLEAN DEFAULT TRUE,
            is_scanned_only BOOLEAN DEFAULT FALSE,
            first_page_char_count INT DEFAULT 0,
            text_sample TEXT,
            full_text TEXT,
            license_detected VARCHAR(255),
            license_family VARCHAR(255),
            copyright_status VARCHAR(255),
            license_evidence TEXT,
            license_source VARCHAR(255),
            license_confidence DOUBLE PRECISION,
            detection_method VARCHAR(100),
            quality_tier VARCHAR(100),
            exclude_from_training BOOLEAN DEFAULT FALSE,
            exclusion_reason TEXT,
            processing_error TEXT,
            license_detection JSONB,
            raw_metadata JSONB,
            processed_at TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );

        ALTER TABLE books ADD COLUMN IF NOT EXISTS full_text TEXT;
        ALTER TABLE books ADD COLUMN IF NOT EXISTS license_source VARCHAR(255);

        CREATE INDEX IF NOT EXISTS idx_books_md5_hash ON books(md5_hash);
        CREATE INDEX IF NOT EXISTS idx_books_license ON books(license_detected);
        """

        cursor.execute(schema_sql)
        conn.commit()
        cursor.close()
        conn.close()
        print("[OK] PostgreSQL database table 'books' initialized successfully.")
        return True
    except Exception as e:
        print(f"[WARN] PostgreSQL connection/initialization error: {e}")
        print("[INFO] Continuing execution without database logging...")
        return False


def clean_nul(val):
    if isinstance(val, str):
        return val.replace("\x00", "")
    return val


def save_to_postgres(metadata, license_detection, processed_at=None):
    """
    Upserts PDF metadata and license detection payload into PostgreSQL.
    """
    if not PSYCOPG2_AVAILABLE:
        print("[WARN] psycopg2 is not installed. Skipping PostgreSQL storage.")
        return False

    if not metadata or not isinstance(metadata, dict):
        print("[ERROR] Invalid metadata passed to save_to_postgres.")
        return False

    if processed_at is None:
        processed_at = metadata.get("processed_at") or datetime.now().isoformat()

    filename = clean_nul(metadata.get("filename", ""))
    if not filename:
        print("[ERROR] Metadata missing 'filename'. Cannot save to DB.")
        return False

    # Extract scalar fields
    file_path = clean_nul(metadata.get("file_path", ""))
    source_folder = clean_nul(metadata.get("source_folder", ""))
    file_size_bytes = metadata.get("file_size_bytes", 0)
    md5_hash = clean_nul(metadata.get("md5_hash", ""))
    title = clean_nul(metadata.get("title", ""))
    author = clean_nul(metadata.get("author", ""))
    publisher = clean_nul(metadata.get("publisher", ""))
    subject = clean_nul(metadata.get("subject", ""))
    keywords = clean_nul(metadata.get("keywords", ""))
    creation_date = clean_nul(str(metadata.get("creation_date", "")))
    language = clean_nul(metadata.get("language", ""))
    page_count = metadata.get("page_count", 0)
    has_toc = bool(metadata.get("has_toc", False))
    pdf_version = clean_nul(metadata.get("pdf_version", ""))
    is_encrypted = bool(metadata.get("is_encrypted", False))
    is_corrupted = bool(metadata.get("is_corrupted", False))
    is_parseable = bool(metadata.get("is_parseable", True))
    is_scanned_only = bool(metadata.get("is_scanned_only", False))
    first_page_char_count = metadata.get("first_page_char_count", 0)
    text_sample = clean_nul(metadata.get("text_sample", ""))
    full_text = clean_nul(metadata.get("full_text", text_sample))

    license_detected = clean_nul(metadata.get("license_detected") or license_detection.get("license_name", "Unknown"))
    license_family = clean_nul(metadata.get("license_family") or license_detection.get("license_family", ""))
    copyright_status = clean_nul(metadata.get("copyright_status") or license_detection.get("copyright_status", ""))
    license_evidence = clean_nul(metadata.get("license_evidence") or license_detection.get("evidence", ""))
    license_source = clean_nul(metadata.get("license_source") or license_detection.get("source", ""))
    license_confidence = float(metadata.get("license_confidence", license_detection.get("confidence", 0.0)))
    detection_method = clean_nul(metadata.get("detection_method") or license_detection.get("method", ""))

    quality_tier = clean_nul(metadata.get("quality_tier", ""))
    exclude_from_training = bool(metadata.get("exclude_from_training", False))
    exclusion_reason = clean_nul(metadata.get("exclusion_reason", ""))
    processing_error = clean_nul(metadata.get("processing_error", ""))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO books (
            filename, file_path, source_folder, file_size_bytes, md5_hash,
            title, author, publisher, subject, keywords, creation_date, language,
            page_count, has_toc, pdf_version, is_encrypted, is_corrupted,
            is_parseable, is_scanned_only, first_page_char_count, text_sample, full_text,
            license_detected, license_family, copyright_status, license_evidence, license_source,
            license_confidence, detection_method, quality_tier, exclude_from_training,
            exclusion_reason, processing_error, license_detection, raw_metadata, processed_at
        ) VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
        ON CONFLICT (filename) DO UPDATE SET
            file_path = EXCLUDED.file_path,
            source_folder = EXCLUDED.source_folder,
            file_size_bytes = EXCLUDED.file_size_bytes,
            md5_hash = EXCLUDED.md5_hash,
            title = EXCLUDED.title,
            author = EXCLUDED.author,
            publisher = EXCLUDED.publisher,
            subject = EXCLUDED.subject,
            keywords = EXCLUDED.keywords,
            creation_date = EXCLUDED.creation_date,
            language = EXCLUDED.language,
            page_count = EXCLUDED.page_count,
            has_toc = EXCLUDED.has_toc,
            pdf_version = EXCLUDED.pdf_version,
            is_encrypted = EXCLUDED.is_encrypted,
            is_corrupted = EXCLUDED.is_corrupted,
            is_parseable = EXCLUDED.is_parseable,
            is_scanned_only = EXCLUDED.is_scanned_only,
            first_page_char_count = EXCLUDED.first_page_char_count,
            text_sample = EXCLUDED.text_sample,
            full_text = EXCLUDED.full_text,
            license_detected = EXCLUDED.license_detected,
            license_family = EXCLUDED.license_family,
            copyright_status = EXCLUDED.copyright_status,
            license_evidence = EXCLUDED.license_evidence,
            license_source = EXCLUDED.license_source,
            license_confidence = EXCLUDED.license_confidence,
            detection_method = EXCLUDED.detection_method,
            quality_tier = EXCLUDED.quality_tier,
            exclude_from_training = EXCLUDED.exclude_from_training,
            exclusion_reason = EXCLUDED.exclusion_reason,
            processing_error = EXCLUDED.processing_error,
            license_detection = EXCLUDED.license_detection,
            raw_metadata = EXCLUDED.raw_metadata,
            processed_at = EXCLUDED.processed_at;
        """

        json_license_detection = json.dumps(license_detection, ensure_ascii=False).replace("\u0000", "").replace("\x00", "")
        json_metadata = json.dumps(metadata, ensure_ascii=False).replace("\u0000", "").replace("\x00", "")

        cursor.execute(sql, (
            filename, file_path, source_folder, file_size_bytes, md5_hash,
            title, author, publisher, subject, keywords, creation_date, language,
            page_count, has_toc, pdf_version, is_encrypted, is_corrupted,
            is_parseable, is_scanned_only, first_page_char_count, text_sample, full_text,
            license_detected, license_family, copyright_status, license_evidence, license_source,
            license_confidence, detection_method, quality_tier, exclude_from_training,
            exclusion_reason, processing_error,
            json_license_detection,
            json_metadata,
            processed_at
        ))

        conn.commit()
        cursor.close()
        conn.close()
        print(f"[OK] PostgreSQL: Successfully saved/updated record for '{filename}'")
        return True
    except Exception as e:
        print(f"[ERROR] PostgreSQL insertion failed for '{filename}': {e}")
        return False


def extract_search_snippet(text, query, snippet_len=250):
    """Extract context snippet around matching query in text."""
    if not text or not query:
        return ""
    idx = text.lower().find(query.lower())
    if idx == -1:
        return text[:snippet_len] + "..." if len(text) > snippet_len else text
    start = max(0, idx - 80)
    end = min(len(text), idx + len(query) + 120)
    snippet = text[start:end].strip()
    prefix = "..." if start > 0 else ""
    suffix = "..." if end < len(text) else ""
    return f"{prefix}{snippet}{suffix}"


def search_books(query=None, license_filter=None, limit=50):
    """
    Search books in PostgreSQL by query string across title, filename, author, keywords, text_sample, full_text.
    """
    if not PSYCOPG2_AVAILABLE:
        print("[WARN] psycopg2 is not installed. Cannot perform database search.")
        return []

    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        sql = "SELECT * FROM books WHERE 1=1"
        params = []

        if query and query.strip():
            q = f"%{query.strip()}%"
            sql += """ AND (
                filename ILIKE %s OR
                title ILIKE %s OR
                author ILIKE %s OR
                publisher ILIKE %s OR
                keywords ILIKE %s OR
                subject ILIKE %s OR
                text_sample ILIKE %s OR
                full_text ILIKE %s OR
                license_detected ILIKE %s OR
                license_evidence ILIKE %s
            )"""
            params.extend([q] * 10)

        if license_filter and license_filter.strip():
            sql += " AND license_detected ILIKE %s"
            params.append(f"%{license_filter.strip()}%")

        sql += " ORDER BY processed_at DESC LIMIT %s"
        params.append(limit)

        cursor.execute(sql, params)
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        # Convert RealDictRow to standard Python dicts and compute snippet
        books = []
        for row in results:
            b = dict(row)
            if query and query.strip():
                content_to_search = b.get("full_text") or b.get("text_sample") or ""
                b["matching_snippet"] = extract_search_snippet(content_to_search, query.strip())
            else:
                sample = b.get("text_sample") or b.get("full_text") or ""
                b["matching_snippet"] = sample[:250] + "..." if len(sample) > 250 else sample
            books.append(b)

        return books

    except Exception as e:
        print(f"[ERROR] PostgreSQL search failed: {e}")
        return []
