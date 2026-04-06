import json
import csv
import os

# Step 1: Find JSON file inside data folder
data_folder = "data"
json_file = None

for file in os.listdir(data_folder):
    if file.endswith(".json"):
        json_file = os.path.join(data_folder, file)
        break

if not json_file:
    print("No JSON file found in data folder")
    exit()

print("Loading file:", json_file)

# Step 2: Load JSON data
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Total records before cleaning:", len(data))

# Step 3: Clean Data
cleaned_data = []

for item in data:
    # Skip missing values
    if not item.get("title") or not item.get("author"):
        continue
    
    # Clean title spaces
    item["title"] = item["title"].strip()
    
    cleaned_data.append(item)

print("Total records after cleaning:", len(cleaned_data))

# Step 4: Save CSV file
csv_file = "data/cleaned_trends.csv"

keys = [
    "post_id",
    "title",
    "category",
    "score",
    "num_comments",
    "author",
    "collected_at"
]

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=keys)
    writer.writeheader()
    writer.writerows(cleaned_data)

print("Cleaned data saved to:", csv_file)
