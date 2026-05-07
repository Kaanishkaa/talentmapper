"""
Skill tagging pipeline.
Loads Excel rule files and matches businesses to skill IDs using keyword matching.
"""

from __future__ import annotations
import re
import pandas as pd
from pathlib import Path
from functools import lru_cache
import config


@lru_cache(maxsize=None)
def _load_skill_rules() -> dict[str, pd.DataFrame]:
    """Load all Excel skill rule files into a dict keyed by business group."""
    rules = {}
    for xlsx in config.SKILL_TAG_DIR.glob("*.xlsx"):
        key = xlsx.stem
        df = pd.read_excel(xlsx, engine="openpyxl")
        # Drop header/footer rows that are not actual skill rules
        df = df.dropna(subset=["Skills IDs"])
        df = df[df["Skills Tags"].astype(str).str.strip() != ""]
        rules[key] = df
    return rules


def identify_business_group(business: dict) -> str | None:
    """Map a business to its skill rule group based on type + description keywords."""
    text = " ".join([
        business.get("business_type", ""),
        business.get("description", ""),
        business.get("name", ""),
    ]).lower()

    best_group = None
    best_score = 0
    for group, keywords in config.BUSINESS_GROUP_MAP.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > best_score:
            best_score = score
            best_group = group
    return best_group if best_score > 0 else None


def _parse_skill_ids(raw: str) -> list[int]:
    """Parse a comma-separated or newline-separated skill IDs string into ints."""
    raw = str(raw)
    # Extract all leading digit sequences
    ids = re.findall(r"\b(\d+)\b", raw)
    return [int(i) for i in ids]


def _parse_skill_names(raw: str) -> list[str]:
    """Parse skill names from multi-line IDs+names string."""
    raw = str(raw)
    names = []
    for line in raw.split("\n"):
        line = line.strip().lstrip(",").strip()
        if ":" in line:
            # Format: "7: Retail & Foodservice>Management>Restaurant"
            name = line.split(":", 1)[1].strip()
            if name:
                names.append(name)
    return names if names else [raw.strip()]


def tag_skills(business: dict) -> dict:
    """
    Tag a business with matching skill IDs and names.
    Returns updated business dict with 'skills' key.
    """
    rules = _load_skill_rules()
    group = identify_business_group(business)
    business["business_group"] = group or "Unknown"

    if group is None or group not in rules:
        business["skills"] = []
        business["skill_tags"] = []
        return business

    df = rules[group]
    text = " ".join([
        business.get("business_type", ""),
        business.get("description", ""),
        business.get("name", ""),
    ]).lower()

    matched_skills: list[dict] = []
    seen_ids: set[int] = set()

    for _, row in df.iterrows():
        tag = str(row.get("Skills Tags", "")).strip()
        rule = str(row.get("Prompt Rule", "")).lower()
        raw_ids = row.get("Skills IDs", "")
        raw_names = row.get("Skills Names", "")

        if pd.isna(raw_ids) or str(raw_ids).strip() in ("", "nan"):
            continue

        # Check if any keyword from the rule text or tag appears in the business description
        rule_keywords = re.findall(r"\b\w{4,}\b", rule)
        tag_keywords = re.findall(r"\b\w{4,}\b", tag.lower())
        all_keywords = rule_keywords + tag_keywords

        if any(kw in text for kw in all_keywords):
            ids = _parse_skill_ids(str(raw_ids))
            names = _parse_skill_names(str(raw_names)) if not pd.isna(raw_names) else [tag]
            for sid, sname in zip(ids, names + [tag] * max(0, len(ids) - len(names))):
                if sid not in seen_ids:
                    seen_ids.add(sid)
                    matched_skills.append({
                        "skill_id": sid,
                        "skill_name": sname,
                        "tag": tag,
                    })

    business["skills"] = matched_skills
    business["skill_tags"] = list({s["tag"] for s in matched_skills})
    return business


def tag_all(businesses: list[dict]) -> list[dict]:
    return [tag_skills(b) for b in businesses]
