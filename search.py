import sys
import argparse
from src.db import search_books, PSYCOPG2_AVAILABLE

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False


def print_books_table(books):
    if not books:
        print("\n[INFO] No books found matching search criteria.")
        return

    print(f"\n[OK] Found {len(books)} matching book(s):\n")

    if HAS_TABULATE:
        headers = ["ID", "Filename", "Title", "Author", "License", "Confidence", "Processed Date"]
        rows = []
        for b in books:
            rows.append([
                b.get("id"),
                b.get("filename", "")[:25],
                (b.get("title") or "N/A")[:25],
                (b.get("author") or "N/A")[:20],
                (b.get("license_detected") or "Unknown")[:25],
                f"{b.get('license_confidence', 0.0):.2f}",
                str(b.get("processed_at"))[:19]
            ])
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        # Fallback table printing
        print("-" * 100)
        print(f"{'ID':<4} | {'Filename':<25} | {'Title':<20} | {'License':<25} | {'Processed'}")
        print("-" * 100)
        for b in books:
            fn = (b.get("filename") or "")[:25]
            tt = (b.get("title") or "N/A")[:20]
            lc = (b.get("license_detected") or "Unknown")[:25]
            pa = str(b.get("processed_at"))[:19]
            print(f"{b.get('id'):<4} | {fn:<25} | {tt:<20} | {lc:<25} | {pa}")
        print("-" * 100)

    # Detailed summary for each book
    print("\n--- Detailed View ---")
    for idx, b in enumerate(books, 1):
        print(f"\n[{idx}] {b.get('filename')}")
        print(f"    Path           : {b.get('file_path')}")
        print(f"    Title          : {b.get('title') or 'N/A'}")
        print(f"    Author         : {b.get('author') or 'N/A'}")
        print(f"    Publisher      : {b.get('publisher') or 'N/A'}")
        print(f"    License        : {b.get('license_detected')}")
        print(f"    License Family : {b.get('license_family')}")
        print(f"    Evidence       : {(b.get('license_evidence') or '').strip()[:150]}...")
        print(f"    Processed At   : {b.get('processed_at')}")


def main():
    parser = argparse.ArgumentParser(description="Search books stored in PostgreSQL database.")
    parser.add_argument("-q", "--query", type=str, help="Search term (title, filename, author, keyword, text sample)")
    parser.add_argument("-l", "--license", type=str, help="Filter by detected license name")
    parser.add_argument("-a", "--all", action="store_true", help="List all processed books")
    parser.add_argument("--limit", type=int, default=50, help="Maximum results to return (default: 50)")

    args = parser.parse_args()

    if not PSYCOPG2_AVAILABLE:
        print("[ERROR] psycopg2 is not installed. Please run: pip install psycopg2-binary")
        sys.exit(1)

    # If flags passed via CLI
    if args.query or args.license or args.all:
        q = None if args.all else args.query
        books = search_books(query=q, license_filter=args.license, limit=args.limit)
        print_books_table(books)
        return

    # Interactive prompt loop if no arguments provided
    print("\n==============================================")
    print("   POSTGRESQL BOOK SEARCH SYSTEM (CLI)")
    print("==============================================")

    while True:
        try:
            print("\nEnter search query (or 'all' to list all, 'exit' to quit):")
            user_input = input("> ").strip()

            if user_input.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                break

            if user_input.lower() == "all":
                books = search_books(limit=args.limit)
            else:
                books = search_books(query=user_input, limit=args.limit)

            print_books_table(books)

        except (KeyboardInterrupt, EOFError):
            print("\nExiting search.")
            break


if __name__ == "__main__":
    main()
