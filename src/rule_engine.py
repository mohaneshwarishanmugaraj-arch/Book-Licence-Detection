import re


# ============================================================
# 1. LICENSE DEFINITIONS
# ============================================================

# Each license has:
#   - name: Official license name
#   - family: License category
#   - keywords: List of keyword patterns to match
#   - multi_keywords: List of keyword combos (ALL must match)
#   - permissions: commercial, modify, redistribute, attribution

LICENSES = [

    # --------------------------------------------------------
    # Creative Commons (most specific first)
    # --------------------------------------------------------

    {
        "name": "CC BY-NC-ND 4.0",
        "family": "Creative Commons",
        "multi_keywords": [
            ["creative commons", "noncommercial", "noderivatives"],
            ["creative commons", "noncommercial", "no derivatives"],
            ["creative commons", "non-commercial", "no-derivatives"],
            ["cc by-nc-nd"],
        ],
        "keywords": [
            "cc by-nc-nd",
            "cc-by-nc-nd",
        ],
        "commercial_use": False,
        "modification_allowed": False,
        "redistribution_allowed": True,
        "attribution_required": True,
    },

    {
        "name": "CC BY-NC-SA 4.0",
        "family": "Creative Commons",
        "multi_keywords": [
            ["creative commons", "noncommercial", "sharealike"],
            ["creative commons", "non-commercial", "share-alike"],
            ["creative commons", "non-commercial", "share alike"],
        ],
        "keywords": [
            "cc by-nc-sa",
            "cc-by-nc-sa",
        ],
        "commercial_use": False,
        "modification_allowed": True,
        "redistribution_allowed": True,
        "attribution_required": True,
    },

    {
        "name": "CC BY-NC 4.0",
        "family": "Creative Commons",
        "multi_keywords": [
            ["creative commons", "noncommercial"],
            ["creative commons", "non-commercial"],
        ],
        "keywords": [
            "cc by-nc",
            "cc-by-nc",
        ],
        "commercial_use": False,
        "modification_allowed": True,
        "redistribution_allowed": True,
        "attribution_required": True,
    },

    {
        "name": "CC BY-ND 4.0",
        "family": "Creative Commons",
        "multi_keywords": [
            ["creative commons", "noderivatives"],
            ["creative commons", "no derivatives"],
            ["creative commons", "no-derivatives"],
        ],
        "keywords": [
            "cc by-nd",
            "cc-by-nd",
        ],
        "commercial_use": True,
        "modification_allowed": False,
        "redistribution_allowed": True,
        "attribution_required": True,
    },

    {
        "name": "CC BY-SA 4.0",
        "family": "Creative Commons",
        "multi_keywords": [
            ["creative commons", "sharealike"],
            ["creative commons", "share-alike"],
            ["creative commons", "share alike"],
        ],
        "keywords": [
            "cc by-sa",
            "cc-by-sa",
        ],
        "commercial_use": True,
        "modification_allowed": True,
        "redistribution_allowed": True,
        "attribution_required": True,
    },

    {
        "name": "CC BY 4.0",
        "family": "Creative Commons",
        "multi_keywords": [
            ["creative commons", "attribution"],
        ],
        "keywords": [
            "cc by 4.0",
            "cc by 3.0",
            "cc by 2.0",
            "cc-by-4.0",
            "cc-by-3.0",
        ],
        "commercial_use": True,
        "modification_allowed": True,
        "redistribution_allowed": True,
        "attribution_required": True,
    },

    {
        "name": "CC0 1.0",
        "family": "Creative Commons",
        "multi_keywords": [
            ["creative commons", "public domain dedication"],
        ],
        "keywords": [
            "cc0 1.0",
            "cc0",
        ],
        "commercial_use": True,
        "modification_allowed": True,
        "redistribution_allowed": True,
        "attribution_required": False,
    },

    # --------------------------------------------------------
    # Software Licenses
    # --------------------------------------------------------

    {
        "name": "MIT License",
        "family": "Permissive",
        "multi_keywords": [],
        "keywords": [
            "mit license",
            "permission is hereby granted, free of charge",
        ],
        "commercial_use": True,
        "modification_allowed": True,
        "redistribution_allowed": True,
        "attribution_required": True,
    },

    {
        "name": "Apache License 2.0",
        "family": "Permissive",
        "multi_keywords": [
            ["apache license", "version 2.0"],
            ["apache license", "2.0"],
        ],
        "keywords": [
            "apache license, version 2.0",
            "apache license 2.0",
            "apache-2.0",
        ],
        "commercial_use": True,
        "modification_allowed": True,
        "redistribution_allowed": True,
        "attribution_required": True,
    },

    {
        "name": "GPL v3",
        "family": "Copyleft",
        "multi_keywords": [
            ["gnu general public license", "version 3"],
        ],
        "keywords": [
            "gplv3",
            "gpl-3.0",
            "gnu general public license version 3",
        ],
        "commercial_use": True,
        "modification_allowed": True,
        "redistribution_allowed": True,
        "attribution_required": True,
    },

    {
        "name": "GPL v2",
        "family": "Copyleft",
        "multi_keywords": [
            ["gnu general public license", "version 2"],
        ],
        "keywords": [
            "gplv2",
            "gpl-2.0",
            "gnu general public license version 2",
        ],
        "commercial_use": True,
        "modification_allowed": True,
        "redistribution_allowed": True,
        "attribution_required": True,
    },

    {
        "name": "GPL",
        "family": "Copyleft",
        "multi_keywords": [],
        "keywords": [
            "gnu general public license",
            "gpl license",
        ],
        "commercial_use": True,
        "modification_allowed": True,
        "redistribution_allowed": True,
        "attribution_required": True,
    },

    {
        "name": "LGPL",
        "family": "Copyleft",
        "multi_keywords": [],
        "keywords": [
            "gnu lesser general public license",
            "lgpl",
        ],
        "commercial_use": True,
        "modification_allowed": True,
        "redistribution_allowed": True,
        "attribution_required": True,
    },

    {
        "name": "GFDL",
        "family": "Copyleft",
        "multi_keywords": [],
        "keywords": [
            "gnu free documentation license",
            "gfdl",
        ],
        "commercial_use": True,
        "modification_allowed": True,
        "redistribution_allowed": True,
        "attribution_required": True,
    },

    {
        "name": "Mozilla Public License 2.0",
        "family": "Copyleft",
        "multi_keywords": [],
        "keywords": [
            "mozilla public license",
            "mpl 2.0",
            "mpl-2.0",
        ],
        "commercial_use": True,
        "modification_allowed": True,
        "redistribution_allowed": True,
        "attribution_required": True,
    },

    {
        "name": "BSD 3-Clause",
        "family": "Permissive",
        "multi_keywords": [
            [
                "redistribution and use in source and binary forms",
                "neither the name"
            ],
        ],
        "keywords": [
            "bsd 3-clause",
            "bsd-3-clause",
        ],
        "commercial_use": True,
        "modification_allowed": True,
        "redistribution_allowed": True,
        "attribution_required": True,
    },

    {
        "name": "BSD 2-Clause",
        "family": "Permissive",
        "multi_keywords": [],
        "keywords": [
            "bsd 2-clause",
            "bsd-2-clause",
            "redistribution and use in source and binary forms",
        ],
        "commercial_use": True,
        "modification_allowed": True,
        "redistribution_allowed": True,
        "attribution_required": True,
    },

    # --------------------------------------------------------
    # Public Domain
    # --------------------------------------------------------

    {
        "name": "Public Domain",
        "family": "Public Domain",
        "multi_keywords": [],
        "keywords": [
            "public domain",
        ],
        "commercial_use": True,
        "modification_allowed": True,
        "redistribution_allowed": True,
        "attribution_required": False,
    },

    # --------------------------------------------------------
    # All Rights Reserved (must be LAST)
    # --------------------------------------------------------

    {
        "name": "NCERT",
        "family": "Educational",
        "multi_keywords": [
            ["national council of educational research and training", "textbook"],
            ["national council of educational research and training", "class"],
        ],
        "keywords": [
            "national council of educational research and training",
            "ncert",
        ],
        "commercial_use": False,
        "modification_allowed": False,
        "redistribution_allowed": False,
        "attribution_required": True,
    },

    {
        "name": "All Rights Reserved",
        "family": "Copyright",
        "multi_keywords": [],
        "keywords": [
            "all rights reserved",
            "no part of this publication may be reproduced",
            "no part of this book may be reproduced",
            "may not be reproduced without prior permission",
            "without the prior permission of the publisher",
        ],
        "commercial_use": False,
        "modification_allowed": False,
        "redistribution_allowed": False,
        "attribution_required": False,
    },
]


# ============================================================
# 2. EXTRACT COPYRIGHT HOLDER
# ============================================================

def extract_copyright_holder(text):
    """
    Extract copyright holder from text using
    common copyright patterns.
    """

    # --------------------------------------------------------
    # Pattern: (c) Name, Year
    # or: copyright (c) Year Name
    # or: copyright Name
    # --------------------------------------------------------

    patterns = [

        # (c) National Council of Educational Research
        r"(?:copyright\s*)?(?:\u00a9|\(c\))\s*"
        r"(?:\d{4}\s*,?\s*)?"
        r"([A-Z][A-Za-z\s,&.]+?)(?:\.|,|\n|$)",

        # Copyright 2006 by Author Name
        r"copyright\s+\d{4}\s+(?:by\s+)?"
        r"([A-Z][A-Za-z\s,&.]+?)(?:\.|,|\n|$)",

        # Published by Publisher Name
        r"published\s+(?:by|at)\s+(?:the\s+)?"
        r"([A-Z][A-Za-z\s,&.]+?)(?:\.|,|\n|$)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:

            holder = match.group(1).strip()

            # Clean up trailing punctuation
            holder = holder.rstrip(" ,.")

            if len(holder) > 3:

                return holder

    return ""


# ============================================================
# 3. FIND EVIDENCE TEXT
# ============================================================

def find_evidence(text, keyword, context_chars=200):
    """
    Find the keyword in text and return surrounding
    context as evidence.
    """

    text_lower = text.lower()

    keyword_lower = keyword.lower()

    pos = text_lower.find(keyword_lower)

    if pos == -1:

        return ""

    start = max(0, pos - context_chars)

    end = min(
        len(text),
        pos + len(keyword) + context_chars
    )

    evidence = text[start:end].strip()

    return evidence


# ============================================================
# 4. DETECT LICENSE (DETERMINISTIC)
# ============================================================

def detect_license_rule_based(text):
    """
    Deterministic rule-based license detection.

    Scans text for known license keywords and
    returns a structured result.

    The license list is ordered from most specific
    to least specific to avoid false matches.

    Returns None if no match is found.
    """

    if not text:

        return None

    text_lower = text.lower()

    # --------------------------------------------------------
    # Scan each license definition
    # --------------------------------------------------------

    # Prefer explicit copyright restriction notices over
    # general publisher/educational identity matches.
    if "all rights reserved" in text_lower or "no part of this publication may be reproduced" in text_lower:
        return {
            "license_name": "All Rights Reserved",
            "license_family": "Copyright",
            "copyright_holder": extract_copyright_holder(text),
            "copyright_status": "All Rights Reserved",
            "commercial_use": False,
            "modification_allowed": False,
            "redistribution_allowed": False,
            "attribution_required": False,
            "evidence": find_evidence(text, "all rights reserved"),
            "confidence": 1.0,
            "method": "Rule-Based",
            "matched_keyword": "all rights reserved",
        }

    for license_def in LICENSES:

        matched = False
        matched_keyword = ""

        # ----------------------------------------------------
        # Check multi-keyword combos first
        # (ALL keywords in a combo must be present)
        # ----------------------------------------------------

        for combo in license_def.get(
            "multi_keywords", []
        ):

            all_found = all(
                kw in text_lower
                for kw in combo
            )

            if all_found:

                matched = True

                matched_keyword = " + ".join(combo)

                break

        # ----------------------------------------------------
        # Check single keywords
        # ----------------------------------------------------

        if not matched:

            for keyword in license_def.get(
                "keywords", []
            ):

                if keyword in text_lower:

                    matched = True

                    matched_keyword = keyword

                    break

        # ----------------------------------------------------
        # Build result if matched
        # ----------------------------------------------------

        if matched:

            evidence = find_evidence(
                text,
                matched_keyword.split(" + ")[0]
                if " + " in matched_keyword
                else matched_keyword
            )

            # Try to extract copyright holder
            # from the original (non-lowered) text
            copyright_holder = extract_copyright_holder(
                text
            )

            # Determine copyright status
            if license_def["name"] == "All Rights Reserved":

                copyright_status = "All Rights Reserved"

            elif license_def["family"] == "Public Domain":

                copyright_status = "Public Domain"

            elif license_def["name"] == "NCERT":

                copyright_status = "Licensed under NCERT"

            else:

                copyright_status = (
                    f"Licensed under {license_def['name']}"
                )

            result = {

                "license_name":
                    license_def["name"],

                "license_family":
                    license_def["family"],

                "copyright_holder":
                    copyright_holder,

                "copyright_status":
                    copyright_status,

                "commercial_use":
                    license_def["commercial_use"],

                "modification_allowed":
                    license_def["modification_allowed"],

                "redistribution_allowed":
                    license_def["redistribution_allowed"],

                "attribution_required":
                    license_def["attribution_required"],

                "evidence":
                    evidence,

                "confidence":
                    1.0,

                "method":
                    "Rule-Based",

                "matched_keyword":
                    matched_keyword,
            }

            return result

    # --------------------------------------------------------
    # No match found
    # --------------------------------------------------------

    return None
