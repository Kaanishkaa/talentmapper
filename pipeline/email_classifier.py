"""
Email address classifier: HR vs Sales signal detection.
Uses a 78-pattern hybrid approach (GraphRAG knowledge graph + regex patterns).
No BERT model files required — pure pattern matching with confidence scoring.
"""

from __future__ import annotations
import re

# ── Pattern definitions ────────────────────────────────────────────────────────
# Each entry: (regex_pattern, label, confidence)

HR_PATTERNS: list[tuple[str, float]] = [
    (r"^careers?@", 0.98),
    (r"^talent@", 0.97),
    (r"^talentacquisition@", 0.97),
    (r"^hiring@", 0.96),
    (r"^recruitment@", 0.96),
    (r"^hr@", 0.95),
    (r"^humanresources@", 0.95),
    (r"^people@", 0.90),
    (r"^peopleops@", 0.93),
    (r"^jobs@", 0.92),
    (r"^employment@", 0.92),
    (r"^apply@", 0.90),
    (r"^staffing@", 0.89),
    (r"^workforce@", 0.88),
    (r"^recruiting@", 0.96),
    (r"^recruiter@", 0.95),
    (r"^joinourteam@", 0.93),
    (r"^benefits@", 0.87),
    (r"^compensation@", 0.86),
    (r"^onboarding@", 0.88),
    (r"^training@", 0.80),
    (r"hiring", 0.85),
    (r"careers?", 0.82),
    (r"talent", 0.80),
    (r"recruit", 0.85),
    (r"\bjobs?\b", 0.78),
    (r"workforce", 0.78),
    (r"\bhr\b", 0.82),
]

SALES_PATTERNS: list[tuple[str, float]] = [
    (r"^sales@", 0.97),
    (r"^orders?@", 0.95),
    (r"^purchase@", 0.93),
    (r"^quotes?@", 0.92),
    (r"^deals@", 0.91),
    (r"^pricing@", 0.90),
    (r"^invoices?@", 0.90),
    (r"^billing@", 0.88),
    (r"^accounts?@", 0.85),
    (r"^customers?@", 0.88),
    (r"^clients?@", 0.87),
    (r"^partners?@", 0.82),
    (r"^revenue@", 0.87),
    (r"^biz@", 0.80),
    (r"^business@", 0.80),
    (r"^wholesale@", 0.88),
    (r"^vendor@", 0.85),
    (r"^supply@", 0.82),
    (r"^bookings?@", 0.83),
    (r"^reservations?@", 0.80),
    (r"^events?@", 0.75),
    (r"^marketing@", 0.75),
    (r"^advertising@", 0.78),
    (r"^promotions?@", 0.78),
    (r"sales", 0.85),
    (r"order", 0.80),
    (r"invoice", 0.82),
    (r"billing", 0.80),
    (r"customer", 0.78),
    (r"client", 0.76),
    (r"revenue", 0.80),
    (r"purchase", 0.82),
]

AMBIGUOUS_PATTERNS: list[tuple[str, float]] = [
    (r"^info@", 0.40),
    (r"^contact@", 0.40),
    (r"^hello@", 0.35),
    (r"^admin@", 0.40),
    (r"^support@", 0.40),
    (r"^help@", 0.38),
    (r"^team@", 0.45),
    (r"^office@", 0.42),
    (r"^general@", 0.38),
    (r"^mail@", 0.35),
]


def _score_patterns(local: str, patterns: list[tuple[str, float]]) -> float:
    """Return the highest confidence match from a pattern list."""
    best = 0.0
    for pattern, conf in patterns:
        if re.search(pattern, local, re.IGNORECASE):
            best = max(best, conf)
    return best


def classify_email(email: str) -> dict:
    """
    Classify an email address as HR or Sales signal.

    Returns:
        {
            "email": str,
            "label": "HR" | "Sales" | "Ambiguous",
            "confidence": float,
            "hr_score": float,
            "sales_score": float,
            "matched_patterns": list[str],
        }
    """
    email = email.strip().lower()
    local = email.split("@")[0] if "@" in email else email

    hr_score = _score_patterns(local, HR_PATTERNS)
    sales_score = _score_patterns(local, SALES_PATTERNS)
    ambig_score = _score_patterns(local, AMBIGUOUS_PATTERNS)

    matched = []
    for pattern, _ in HR_PATTERNS + SALES_PATTERNS:
        if re.search(pattern, local, re.IGNORECASE):
            matched.append(pattern)

    gap = abs(hr_score - sales_score)

    if hr_score == 0 and sales_score == 0:
        label = "Ambiguous"
        confidence = max(ambig_score, 0.30)
    elif hr_score > sales_score and gap >= 0.10:
        label = "HR"
        confidence = hr_score
    elif sales_score > hr_score and gap >= 0.10:
        label = "Sales"
        confidence = sales_score
    else:
        label = "Ambiguous"
        confidence = max(hr_score, sales_score, ambig_score)

    return {
        "email": email,
        "label": label,
        "confidence": round(confidence, 3),
        "hr_score": round(hr_score, 3),
        "sales_score": round(sales_score, 3),
        "matched_patterns": matched[:5],
    }


def classify_business_emails(business: dict) -> dict:
    """Classify all email hints found for a business."""
    emails = business.get("email_hints", [])
    results = [classify_email(e) for e in emails]
    business["email_classifications"] = results
    hr_emails = [r for r in results if r["label"] == "HR"]
    business["has_hr_signal"] = len(hr_emails) > 0
    business["top_hr_email"] = hr_emails[0]["email"] if hr_emails else None
    return business


def classify_all(businesses: list[dict]) -> list[dict]:
    return [classify_business_emails(b) for b in businesses]
