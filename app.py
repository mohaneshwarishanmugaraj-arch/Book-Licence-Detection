import os
from flask import Flask, render_template, request, jsonify
from src.db import search_books, get_db_connection, PSYCOPG2_AVAILABLE
from psycopg2.extras import RealDictCursor

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/search")
def api_search():
    query = request.args.get("query", "").strip()
    license_filter = request.args.get("license", "").strip()
    limit = int(request.args.get("limit", 50))

    if not PSYCOPG2_AVAILABLE:
        return jsonify({
            "error": "psycopg2 is not installed or PostgreSQL connection is unavailable.",
            "books": []
        }), 500

    books = search_books(query=query, license_filter=license_filter, limit=limit)
    return jsonify({
        "count": len(books),
        "books": books
    })


@app.route("/api/book/<filename>")
def api_book(filename):
    """Retrieve full book record including full text content."""
    if not PSYCOPG2_AVAILABLE:
        return jsonify({"error": "Database unavailable"}), 500

    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM books WHERE filename = %s OR filename ILIKE %s LIMIT 1", (filename, f"%{filename}%"))
        book = cursor.fetchone()
        cursor.close()
        conn.close()

        if not book:
            return jsonify({"error": "Book not found"}), 404

        book = dict(book)
        canonical = {
            "file_path": book.get("file_path"),
            "filename": book.get("filename"),
            "source_folder": book.get("source_folder"),
            "file_size_bytes": book.get("file_size_bytes"),
            "md5_hash": book.get("md5_hash"),
            "title": book.get("title"),
            "author": book.get("author"),
            "publisher": book.get("publisher"),
            "subject": book.get("subject"),
            "keywords": book.get("keywords"),
            "creation_date": book.get("creation_date"),
            "language": book.get("language"),
            "page_count": book.get("page_count"),
            "has_toc": book.get("has_toc"),
            "pdf_version": book.get("pdf_version"),
            "is_encrypted": book.get("is_encrypted"),
            "is_corrupted": book.get("is_corrupted"),
            "is_parseable": book.get("is_parseable"),
            "is_scanned_only": book.get("is_scanned_only"),
            "first_page_char_count": book.get("first_page_char_count"),
            "text_sample": book.get("text_sample"),
            "license_detected": book.get("license_detected"),
            "license_source": book.get("license_source"),
            "license_confidence": book.get("license_confidence"),
            "quality_tier": book.get("quality_tier"),
            "exclude_from_training": book.get("exclude_from_training"),
            "exclusion_reason": book.get("exclusion_reason"),
            "processed_at": book.get("processed_at"),
            "processing_error": book.get("processing_error"),
        }
        return jsonify({"book": canonical})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/book_text/<filename>")
def api_book_text(filename):
    """Retrieve full book text or text sample for reading."""
    if not PSYCOPG2_AVAILABLE:
        return jsonify({"error": "Database unavailable"}), 500

    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT full_text, text_sample FROM books WHERE filename = %s OR filename ILIKE %s LIMIT 1", (filename, f"%{filename}%"))
        book = cursor.fetchone()
        cursor.close()
        conn.close()

        if not book:
            return jsonify({"error": "Book not found"}), 404

        return jsonify({
            "full_text": book.get("full_text"),
            "text_sample": book.get("text_sample")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/licenses")
def api_licenses():
    """Get list of unique licenses present in database."""
    if not PSYCOPG2_AVAILABLE:
        return jsonify({"licenses": []})

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT license_detected FROM books WHERE license_detected IS NOT NULL AND license_detected != '' ORDER BY license_detected;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        licenses = [r[0] for r in rows]
        return jsonify({"licenses": licenses})
    except Exception as e:
        return jsonify({"error": str(e), "licenses": []})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"\n[OK] Starting PDF License & Metadata Search Web Portal on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
