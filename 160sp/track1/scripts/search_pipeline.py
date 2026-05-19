import json
import os
import time
from datetime import datetime

import requests
from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

if not PEXELS_API_KEY:
    raise ValueError("PEXELS_API_KEY not found in .env")

# -----------------------------
# Load room types
# -----------------------------
with open("data/space_types.json", "r") as f:
    space_types = json.load(f)

# -----------------------------
# API configuration
# -----------------------------
PEXELS_URL = "https://api.pexels.com/v1/search"

headers = {
    "Authorization": PEXELS_API_KEY
}

# -----------------------------
# Store all collected results
# -----------------------------
all_results = []

# -----------------------------
# Loop through room types
# -----------------------------
for space_type, info in space_types.items():

    print(f"\nSearching for: {space_type}")

    search_terms = info["search_terms"]

    for query in search_terms:

        print(f"  Query: {query}")

        params = {
            "query": query,
            "per_page": 5
        }

        response = requests.get(
            PEXELS_URL,
            headers=headers,
            params=params
        )

        if response.status_code != 200:
            print(f"  ERROR: {response.status_code}")
            continue

        data = response.json()

        photos = data.get("photos", [])

        if len(photos) == 0:
            print(f"  No results found for '{query}'")
            continue

        # -----------------------------
        # Convert API response into
        # assignment-required format
        # -----------------------------
        for photo in photos:

            record = {
                "url": photo["src"]["original"],
                "thumbnail_url": photo["src"]["medium"],
                "title": photo.get("alt", ""),
                "photographer": photo["photographer"],
                "source_name": "Pexels",
                "source_page_url": photo["url"],
                "license": "Pexels License",
                "space_type": space_type,
                "search_query": query,
                "collected_at": datetime.utcnow().isoformat()
            }

            all_results.append(record)

        print(f"  Collected {len(photos)} images")

        # -----------------------------
        # Respect rate limits
        # -----------------------------
        time.sleep(1)

# -----------------------------
# Save results
# -----------------------------
output_path = "data/search_results.json"

with open(output_path, "w") as f:
    json.dump(all_results, f, indent=2)

print("\nDone.")
print(f"Saved {len(all_results)} image records to {output_path}")