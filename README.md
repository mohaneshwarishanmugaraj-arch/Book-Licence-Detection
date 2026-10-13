# Book Licence Detection

A Python application for extracting metadata and text from PDF books, detecting likely license or copyright notices, saving processed records to PostgreSQL, and searching the resulting collection through a web interface or command-line tool.

> **Important:** License detection is automated and may be incorrect or incomplete. Treat results as research clues, not legal advice. Verify the document and its source before relying on a license determination.

## Features

- Parses PDFs into JSON and Markdown with OpenDataLoader PDF.
- Collects file metadata and document metadata such as title, author, publisher, language, and page count.
- Extracts document text and looks for license and copyright evidence.
- Uses the NVIDIA-hosted Llama model when configured; falls back to deterministic keyword rules when the LLM is unavailable or returns an unknown result.
- Writes per-document license and metadata JSON files under `output/`.
- Saves and updates records in PostgreSQL, including extracted text, for later search.
- Provides a Flask search portal and a CLI search utility.

## Project layout

```text
.
├── app.py                  # Flask search portal and JSON API
├── main.py                 # Batch PDF processing pipeline
├── search.py               # PostgreSQL command-line search utility
├── LLM.py                  # Standalone NVIDIA API connectivity test
├── schema.sql              # PostgreSQL table and index definitions
├── requirements.txt        # Python dependencies
├── input/                  # PDF files to process (created automatically)
├── output/                 # Parser results and generated metadata (created automatically)
├── src/
│   ├── db.py               # PostgreSQL setup, persistence, and search
│   ├── jsonreader.py       # JSON loader
│   ├── metadata.py         # File-level metadata and MD5 calculation
│   ├── metadataBuilder.py  # Combines file and PDF metadata
│   ├── pdfparser.py        # PDF parser wrapper
│   ├── preprocessor.py     # Text cleanup for rule-based detection
│   └── rule_engine.py      # License and copyright keyword rules
└── templates/
    └── index.html          # Web search interface
```

## Requirements

- Python 3.10 or newer is recommended.
- PostgreSQL for storing records and using search features.
- NVIDIA API key for LLM-based detection. The rule-based detector still works without the key.
- Dependencies listed in `requirements.txt`.

OpenDataLoader PDF may have additional runtime requirements depending on its installed version and platform. If PDF conversion fails, consult the package's installation guidance and the error output.

## Installation

Run commands from the project root.

1. Create and activate a virtual environment (recommended):

   **Windows PowerShell**
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```shell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Create a local `.env` file in the project root. It is ignored by Git. Add the variables you need:

   ```dotenv
   NVIDIA_API_KEY=your_nvidia_api_key
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=book_licence_detection
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_database_password
   PORT=5000
   ```

   `NVIDIA_API_KEY` is optional for rule-only detection. The PostgreSQL variables default to `localhost:5432`, database `postgres`, user `postgres`, and password `postgres` if omitted. Set these to match your PostgreSQL setup; do not commit real credentials.

4. Create the PostgreSQL database named in `POSTGRES_DB` (for example, `book_licence_detection`) and ensure the configured user can connect and create tables/indexes.

5. Initialize the table and indexes:

   ```shell
   python -c "from src.db import init_db; init_db()"
   ```

   `main.py` also attempts initialization when the batch pipeline starts. The web app expects PostgreSQL and the `books` table to be available; it does not initialize the database on startup. `schema.sql` is provided for reference, while `src/db.py`'s `init_db()` is the initializer used by the application.

## Process PDF files

1. Put one or more `.pdf` files in the project-root `input/` directory. The directory is created automatically if it does not exist.
2. Run the batch processor:

   ```shell
   python main.py
   ```

For each PDF, the pipeline parses the file, extracts metadata and text, attempts license detection, writes JSON results to `output/`, and tries to save the record to PostgreSQL. Processing errors for individual files are printed so the rest of the batch can continue.

Typical generated artifacts include:

- `output/<document>.json` and `output/<document>.md` — OpenDataLoader parser output.
- `output/<document>_license_result.json` — license detection result.
- `output/<document>_complete_metadata.json` — combined metadata and license result.

The pipeline's LLM step sends selected license-related text (up to 12,000 characters) from a document to NVIDIA's API when a key is configured and the API is reachable. Do not process sensitive documents with this option unless that data sharing is acceptable. Without a usable LLM connection, processing falls back to the local keyword rules.

## Search using the web portal

Start the Flask app:

```shell
python app.py
```

Open <http://localhost:5000> (or the port configured with `PORT`). Search terms are matched against filenames, titles, authors, publisher, keywords, subject, extracted text, and license evidence. The license selector filters results by detected license. The interface also provides book metadata and extracted-text views.

The portal requires PostgreSQL records to have been populated by the PDF processing pipeline. If the database is empty, process PDFs first.

### HTTP API

- `GET /api/search?query=<text>&license=<license>&limit=50` — searches stored records; `query` and `license` are optional, and `limit` defaults to 50.
- `GET /api/licenses` — returns the distinct detected license values.
- `GET /api/book/<filename>` — returns selected metadata for one matching filename.
- `GET /api/book_text/<filename>` — returns the stored full text and sample for one matching filename.

## Search using the CLI

List records or search by text/license:

```shell
python search.py --all
python search.py --query "climate change"
python search.py --license "CC BY"
python search.py --query "biology" --license "Public Domain" --limit 20
```

Without search flags, `search.py` starts an interactive prompt. Enter `all` to list all records or `exit` to quit. The CLI requires a reachable PostgreSQL database.

## Test NVIDIA API access

`LLM.py` sends a small test prompt to the configured NVIDIA endpoint and requires `NVIDIA_API_KEY`:

```shell
python LLM.py
```

## Database notes

PostgreSQL connection settings are read from the environment variables `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD`. The application creates a `books` table and indexes through `init_db()`. Records are upserted by filename, so processing a filename already stored updates its record.

The web interface and API return extracted content from the database. Run this development app only in a trusted environment: it has debug mode enabled, has no authentication, and exposes stored book text through its routes. Do not deploy it publicly without adding appropriate security controls and a production WSGI server.

## Troubleshooting

- **Database connection errors:** Check that PostgreSQL is running, that the database exists, and that the `.env` credentials/port are correct. Initialize the schema with the command above.
- **No books in search:** Confirm that PDFs are in `input/`, processing completed, and records were saved to the same PostgreSQL database used by the web app.
- **NVIDIA API errors:** Check `NVIDIA_API_KEY` and network/API access. The pipeline should continue using rule-based detection when the LLM is unavailable.
- **PDF conversion errors:** Check the PDF file and OpenDataLoader PDF's platform/runtime requirements. Parser output is written under `output/`.
- **Missing Python modules:** Activate the intended virtual environment and install `requirements.txt` there.

## Limitations

- Rule-based detection relies on known phrases and can miss variations or return false matches.
- LLM output can also be wrong; confidence is not a legal determination.
- Text-based extraction may be insufficient for scanned or image-only PDFs.
- Search and web API functionality depend on a working PostgreSQL instance.
- The app currently provides no authentication, authorization, or production deployment configuration.
