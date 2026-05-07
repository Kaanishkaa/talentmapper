import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
SKILL_TAG_DIR = DATA_DIR / "skill_tag_csv"

DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

SEMANTIC_SIMILARITY_THRESHOLD = 0.6
MAX_RESULTS_PER_SEARCH = 20

BUSINESS_GROUP_MAP = {
    "Food_and_Beverage_Establishments": [
        "restaurant", "cafe", "coffee", "bar", "brewery", "bakery",
        "pizza", "sushi", "taco", "deli", "sandwich", "ice cream",
        "food truck", "catering", "bistro", "grill", "steakhouse",
        "donut", "smoothie", "juice", "wine bar", "distillery",
    ],
    "Animal_Care_and_Services": [
        "veterinary", "vet", "pet", "animal", "dog", "cat", "grooming",
        "boarding", "kennel", "pet hotel", "pet sitting", "dog walking",
        "aquarium", "zoo",
    ],
    "Cleaning_and_Remediation": [
        "cleaning", "laundry", "dry cleaning", "maid", "housekeeping",
        "janitorial", "carpet cleaning", "window cleaning", "remediation",
        "pressure washing",
    ],
    "Amusement_and_Recreation_and_Cultural_Centers_and_Golf_Courses": [
        "golf", "bowling", "arcade", "movie theater", "cinema", "museum",
        "aquarium", "amusement", "recreation", "escape room", "go kart",
        "water park", "theme park", "zoo", "gallery", "cultural center",
        "fitness", "gym",
    ],
}
