import re


# ============================================================
# 1. CLEAN TEXT
# ============================================================

def clean_text(text):
    """
    Clean raw extracted text for license detection.

    - Convert to lowercase
    - Collapse multiple whitespace
    - Remove blank lines
    - Strip leading/trailing whitespace
    """

    if not text:

        return ""

    # --------------------------------------------------------
    # Lowercase
    # --------------------------------------------------------

    text = text.lower()

    # --------------------------------------------------------
    # Replace newlines with spaces (preserve paragraphs)
    # --------------------------------------------------------

    text = re.sub(
        r"\n\s*\n",
        "\n\n",
        text
    )

    # --------------------------------------------------------
    # Collapse multiple spaces into one
    # --------------------------------------------------------

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # --------------------------------------------------------
    # Remove lines that are only whitespace
    # --------------------------------------------------------

    lines = text.splitlines()

    cleaned_lines = [
        line.strip()
        for line in lines
        if line.strip()
    ]

    return "\n".join(cleaned_lines)


# ============================================================
# 2. EXTRACT FIRST N PAGES TEXT
# ============================================================

def extract_first_pages(
    full_text,
    max_pages=10,
    chars_per_page=3000
):
    """
    Focus on the first N pages of text.

    Copyright and license information is almost
    always in the first 5-10 pages of a book.

    Uses character count as a proxy for page count.
    """

    if not full_text:

        return ""

    max_chars = max_pages * chars_per_page

    if len(full_text) <= max_chars:

        return full_text

    return full_text[:max_chars]


# ============================================================
# 3. REMOVE NOISE
# ============================================================

def remove_noise(text):
    """
    Remove common noise patterns from extracted text.

    - Page numbers
    - Image file references
    - Repeated separators
    """

    if not text:

        return ""

    # --------------------------------------------------------
    # Remove image file references
    # --------------------------------------------------------

    text = re.sub(
        r"\S+_images/\S+\.(png|jpg|jpeg|gif|bmp)",
        "",
        text,
        flags=re.IGNORECASE
    )

    # --------------------------------------------------------
    # Remove standalone page numbers
    # --------------------------------------------------------

    text = re.sub(
        r"^\s*\d{1,3}\s*$",
        "",
        text,
        flags=re.MULTILINE
    )

    # --------------------------------------------------------
    # Remove repeated separators
    # --------------------------------------------------------

    text = re.sub(
        r"[-=_]{5,}",
        "",
        text
    )

    return text.strip()


# ============================================================
# 4. FULL PREPROCESSING PIPELINE
# ============================================================

def preprocess_text(
    full_text,
    max_pages=10,
    chars_per_page=3000
):
    """
    Full preprocessing pipeline.

    1. Extract first N pages
    2. Remove noise
    3. Clean text

    Returns cleaned text ready for license detection.
    """

    print(
        "\n========== TEXT PREPROCESSING =========="
    )

    if not full_text:

        print("[WARN] No text to preprocess")

        return ""

    print(
        f"Original text length: "
        f"{len(full_text)} characters"
    )

    # --------------------------------------------------------
    # Step 1: First pages
    # --------------------------------------------------------

    text = extract_first_pages(
        full_text,
        max_pages=max_pages,
        chars_per_page=chars_per_page
    )

    print(
        f"After page filtering: "
        f"{len(text)} characters"
    )

    # --------------------------------------------------------
    # Step 2: Remove noise
    # --------------------------------------------------------

    text = remove_noise(text)

    print(
        f"After noise removal: "
        f"{len(text)} characters"
    )

    # --------------------------------------------------------
    # Step 3: Clean
    # --------------------------------------------------------

    text = clean_text(text)

    print(
        f"After cleaning: "
        f"{len(text)} characters"
    )

    print("[OK] Text preprocessing completed")

    return text
