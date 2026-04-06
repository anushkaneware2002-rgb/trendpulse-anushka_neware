import requests
import json
import time
from datetime import datetime

# HackerNews API URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Required header
headers = {"User-Agent": "TrendPulse/1.0"}

# Categories and keywords
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

MAX_PER_CATEGORY = 25


# Function to assign category based on title keywords
def get_category(title):
    title = title.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in title:
                return category
    return None


print("Fetching top stories...")

# Step 1: Get top 500 story IDs
try:
    response = requests.get(TOP_STORIES_URL, headers=headers)
    story_ids = response.json()[:500]
except Exception as e:
    print("Error fetching top stories:", e)
    exit()

collected_data = []
category_count = {cat: 0 for cat in categories}


# Step 2: Fetch story details
for category in categories:
    print(f"Collecting {category} stories...")

    for story_id in story_ids:

        # Stop if category limit reached
        if category_count[category] >= MAX_PER_CATEGORY:
            break

        try:
            url = ITEM_URL.format(story_id)
            res = requests.get(url, headers=headers)
            story = res.json()

            # Skip if story has no title
            if not story or "title" not in story:
                continue

            title = story["title"]
            story_category = get_category(title)

            # Check if story belongs to current category
            if story_category == category:
                data = {
                    "post_id": story.get("id"),
                    "title": title,
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", "unknown"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                collected_data.append(data)
                category_count[category] += 1

        except Exception:
            print(f"Failed to fetch story {story_id}")
            continue

    # Wait 2 seconds between categories
    time.sleep(2)


# Step 3: Save to JSON file
date_str = datetime.now().strftime("%Y%m%d")
filename = f"data/trends_{date_str}.json"

# Create folder if not exists
import os
if not os.path.exists("data"):
    os.makedirs("data")

with open(filename, "w", encoding="utf-8") as f:
    json.dump(collected_data, f, indent=4)

print(f"\nCollected {len(collected_data)} stories. Saved to {filename}")
