-- PostgreSQL Schema for PDF Metadata & License Storage

CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL UNIQUE,
    file_path TEXT NOT NULL,
    source_folder TEXT,
    file_size_bytes BIGINT,
    md5_hash VARCHAR(32) UNIQUE,
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
    license_detected VARCHAR(255),
    license_family VARCHAR(255),
    copyright_status VARCHAR(255),
    license_evidence TEXT,
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

-- Index for fast lookup by MD5 hash
CREATE INDEX IF NOT EXISTS idx_books_md5_hash ON books(md5_hash);

-- Index for license filtering
CREATE INDEX IF NOT EXISTS idx_books_license ON books(license_detected);

-- GIN Full Text Search Index for ultra-fast title, author, filename, and keyword search
CREATE INDEX IF NOT EXISTS idx_books_fts ON books USING gin(
    to_tsvector('english', 
        coalesce(title, '') || ' ' || 
        coalesce(author, '') || ' ' || 
        coalesce(filename, '') || ' ' || 
        coalesce(keywords, '') || ' ' || 
        coalesce(publisher, '') || ' ' || 
        coalesce(license_detected, '') || ' ' ||
        coalesce(text_sample, '')
    )
);
