"""
Career page detection pipeline.
Classifies URLs as career pages using 52 patterns across 5 signal categories.
No ML model required — pure pattern + heuristic scoring.
"""

from __future__ import annotations
import re
from urllib.parse import urlparse

# ── Pattern definitions ────────────────────────────────────────────────────────

PATH_PATTERNS: list[tuple[str, float]] = [
    (r"/careers?/?$", 0.95),
    (r"/jobs/?$", 0.93),
    (r"/hiring/?$", 0.92),
    (r"/job-openings?/?$", 0.91),
    (r"/open-positions?/?$", 0.90),
    (r"/work-with-us/?$", 0.88),
    (r"/join-us/?$", 0.87),
    (r"/join-our-team/?$", 0.90),
    (r"/opportunities/?$", 0.85),
    (r"/employment/?$", 0.87),
    (r"/apply/?$", 0.82),
    (r"/career-opportunities?/?$", 0.90),
    (r"/job-listings?/?$", 0.88),
    (r"/vacancies?/?$", 0.86),
    (r"/recruiting/?$", 0.85),
    (r"/careers?/", 0.88),
    (r"/jobs?/", 0.85),
    (r"/people/?$", 0.65),
    (r"/team/?$", 0.55),
    (r"/culture/?$", 0.60),
    (r"/about/careers?", 0.87),
    (r"/company/jobs?", 0.88),
]

SUBDOMAIN_PATTERNS: list[tuple[str, float]] = [
    (r"^jobs\.", 0.92),
    (r"^careers?\.", 0.93),
    (r"^hiring\.", 0.90),
    (r"^apply\.", 0.88),
    (r"^work\.", 0.75),
    (r"^talent\.", 0.85),
    (r"^recruitment\.", 0.88),
]

EXTERNAL_JOB_BOARD_PATTERNS: list[tuple[str, float]] = [
    (r"greenhouse\.io", 0.95),
    (r"lever\.co", 0.95),
    (r"workday\.com", 0.92),
    (r"jobvite\.com", 0.90),
    (r"taleo\.net", 0.90),
    (r"icims\.com", 0.90),
    (r"smartrecruiters\.com", 0.90),
    (r"bamboohr\.com", 0.88),
    (r"ashbyhq\.com", 0.90),
    (r"myworkdayjobs\.com", 0.93),
    (r"apply\.workable\.com", 0.92),
    (r"jobs\.lever\.co", 0.95),
    (r"boards\.greenhouse\.io", 0.95),
    (r"indeed\.com/cmp/", 0.80),
    (r"linkedin\.com/jobs/", 0.75),
    (r"glassdoor\.com/Jobs/", 0.75),
]

KEYWORD_PATTERNS: list[tuple[str, float]] = [
    (r"openings?", 0.75),
    (r"positions?", 0.65),
    (r"applicat", 0.70),
    (r"talent", 0.65),
    (r"workforce", 0.68),
    (r"recruit", 0.75),
    (r"staffing", 0.70),
]


def classify_career_url(url: str) -> dict:
    """
    Classify whether a URL points to a career/jobs page.

    Returns:
        {
            "url": str,
            "is_career_page": bool,
            "confidence": float,
            "signals": list[str],
            "signal_type": str,
        }
    """
    url = url.strip()
    if not url:
        return {"url": url, "is_career_page": False, "confidence": 0.0, "signals": [], "signal_type": "none"}

    try:
        parsed = urlparse(url)
    except Exception:
        return {"url": url, "is_career_page": False, "confidence": 0.0, "signals": [], "signal_type": "error"}

    path = parsed.path.lower()
    subdomain = parsed.netloc.lower().split(".")[0] if parsed.netloc else ""
    full_url = url.lower()

    signals: list[str] = []
    best_score = 0.0
    signal_type = "none"

    for pattern, conf in EXTERNAL_JOB_BOARD_PATTERNS:
        if re.search(pattern, full_url, re.IGNORECASE):
            signals.append(f"job_board:{pattern}")
            if conf > best_score:
                best_score = conf
                signal_type = "external_job_board"

    for pattern, conf in SUBDOMAIN_PATTERNS:
        if re.search(pattern, subdomain, re.IGNORECASE):
            signals.append(f"subdomain:{pattern}")
            if conf > best_score:
                best_score = conf
                signal_type = "subdomain"

    for pattern, conf in PATH_PATTERNS:
        if re.search(pattern, path, re.IGNORECASE):
            signals.append(f"path:{pattern}")
            if conf > best_score:
                best_score = conf
                signal_type = "path"

    for pattern, conf in KEYWORD_PATTERNS:
        if re.search(pattern, full_url, re.IGNORECASE):
            signals.append(f"keyword:{pattern}")
            best_score = max(best_score, conf)
            if signal_type == "none":
                signal_type = "keyword"

    is_career = best_score >= 0.70

    return {
        "url": url,
        "is_career_page": is_career,
        "confidence": round(best_score, 3),
        "signals": signals[:5],
        "signal_type": signal_type,
    }


def detect_career_page(business: dict) -> dict:
    """Detect and classify the career page for a business."""
    career_url = business.get("career_url", "")
    website = business.get("website", "")

    result = classify_career_url(career_url) if career_url else classify_career_url(website)
    business["career_detection"] = result
    business["has_career_page"] = result["is_career_page"]
    business["career_page_url"] = career_url if result["is_career_page"] else None
    return business


def detect_all(businesses: list[dict]) -> list[dict]:
    return [detect_career_page(b) for b in businesses]
