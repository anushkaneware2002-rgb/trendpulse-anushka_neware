import pandas as pd
import numpy as np

# Step 1: Load CSV file from Task 2
file_path = "data/cleaned_trends.csv"

df = pd.read_csv(file_path)

print("Loaded data:", df.shape)

# Step 2: Print first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Step 3: Average score and comments
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print("\nAverage score:", avg_score)
print("Average comments:", avg_comments)

# -------------------------------------
# NumPy Analysis
# -------------------------------------

scores = df["score"].values
comments = df["num_comments"].values

print("\n--- NumPy Stats ---")

print("Mean score:", np.mean(scores))
print("Median score:", np.median(scores))
print("Std deviation:", np.std(scores))

print("Max score:", np.max(scores))
print("Min score:", np.min(scores))

# Category with most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()

print("\nMost stories in:", top_category)

# Most commented story
max_comments_index = np.argmax(comments)

top_story_title = df.iloc[max_comments_index]["title"]
top_story_comments = comments[max_comments_index]

print("\nMost commented story:")
print(top_story_title, "-", top_story_comments, "comments")

# -------------------------------------
# Step 3: Add New Columns
# -------------------------------------

# Engagement column
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Popular column
df["is_popular"] = df["score"] > avg_score

# -------------------------------------
# Step 4: Save New CSV
# -------------------------------------

output_file = "data/trends_analysed.csv"

df.to_csv(output_file, index=False)

print("\nSaved to", output_file)
