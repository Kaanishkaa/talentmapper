"""
Business discovery pipeline.
In demo mode: returns realistic mock data.
In live mode: calls Google Places API + Gemini for prompt parsing.
"""

from __future__ import annotations
import re
import config
from mock.data import get_mock_businesses


def parse_prompt(prompt: str) -> dict:
    """
    Extract business_type and location from a natural language prompt.
    Demo mode: simple regex heuristic.
    Live mode: Gemini API call.
    """
    if config.DEMO_MODE or not config.GEMINI_API_KEY:
        return _parse_prompt_local(prompt)
    return _parse_prompt_gemini(prompt)


def _parse_prompt_local(prompt: str) -> dict:
    """Heuristic prompt parser — handles 'X in Y' patterns."""
    prompt = prompt.strip()
    pattern = re.compile(r"^(.*?)\s+in\s+(.+)$", re.IGNORECASE)
    match = pattern.match(prompt)
    if match:
        business_type = match.group(1).strip().title()
        location = match.group(2).strip().title()
    else:
        business_type = prompt.title()
        location = "Unknown Location"
    return {"business_type": business_type, "location": location, "raw_prompt": prompt}


def _parse_prompt_gemini(prompt: str) -> dict:
    import google.generativeai as genai
    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-pro")
    response = model.generate_content(
        f"Extract the business type and location from this prompt. "
        f"Return JSON with keys 'business_type' and 'location'.\nPrompt: {prompt}"
    )
    import json
    return json.loads(response.text)


def search_businesses(parsed_prompt: dict) -> list[dict]:
    """
    Search for businesses matching the parsed prompt.
    Demo mode: returns mock data.
    Live mode: Google Places API.
    """
    if config.DEMO_MODE or not config.GOOGLE_PLACES_API_KEY:
        raw_prompt = parsed_prompt.get("raw_prompt", "")
        return get_mock_businesses(raw_prompt)
    return _search_places_api(parsed_prompt)


def _search_places_api(parsed_prompt: dict) -> list[dict]:
    import requests
    query = f"{parsed_prompt['business_type']} in {parsed_prompt['location']}"
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "key": config.GOOGLE_PLACES_API_KEY,
        "maxResultCount": config.MAX_RESULTS_PER_SEARCH,
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    results = []
    for place in resp.json().get("results", []):
        results.append({
            "place_id": place.get("place_id"),
            "name": place.get("name"),
            "address": place.get("formatted_address"),
            "rating": place.get("rating"),
            "website": "",
            "description": place.get("types", []),
            "business_type": parsed_prompt["business_type"],
            "email_hints": [],
            "career_url": "",
        })
    return results
