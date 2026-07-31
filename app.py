import os
from flask import Flask, render_template, request, jsonify, send_file
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

        return jsonify({"book": dict(book)})
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
