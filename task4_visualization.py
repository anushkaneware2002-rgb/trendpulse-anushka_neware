# Task 4 - TrendPulse Visualizations
# This script loads analysed data and creates 3 charts + dashboard

import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------------
# 1. Load Data
# -------------------------------
file_path = "data/trends_analysed.csv"
df = pd.read_csv(file_path)

print("Data loaded successfully:", df.shape)


# -------------------------------
# Create outputs folder
# -------------------------------

output_folder = "outputs"
os.makedirs(output_folder, exist_ok=True)


# -------------------------------
# 2. Chart 1 - Top 10 Stories
# -------------------------------

# Sort by score and get top 10
top_stories = df.sort_values(by="score", ascending=False).head(10)

# Shorten long titles
top_stories["short_title"] = top_stories["title"].apply(
    lambda x: x[:50] + "..." if len(x) > 50 else x
)

plt.figure(figsize=(10,6))

plt.barh(top_stories["short_title"], top_stories["score"])

plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")

plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig("outputs/chart1_top_stories.png")

plt.show()


# -------------------------------
# 3. Chart 2 - Stories per Category
# -------------------------------

category_counts = df["category"].value_counts()

plt.figure(figsize=(8,5))

category_counts.plot(kind="bar", color=["skyblue","orange","green","red","purple"])

plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

plt.tight_layout()

plt.savefig("outputs/chart2_categories.png")

plt.show()


# -------------------------------
# 4. Chart 3 - Scatter Plot
# -------------------------------

popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.figure(figsize=(8,5))

plt.scatter(popular["score"], popular["num_comments"], 
            color="red", label="Popular")

plt.scatter(not_popular["score"], not_popular["num_comments"], 
            color="blue", label="Not Popular")

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")

plt.legend()

plt.tight_layout()

plt.savefig("outputs/chart3_scatter.png")

plt.show()


# -------------------------------
# BONUS - Dashboard
# -------------------------------

fig, axes = plt.subplots(1, 3, figsize=(18,5))

# Chart 1
axes[0].barh(top_stories["short_title"], top_stories["score"])
axes[0].set_title("Top Stories")
axes[0].set_xlabel("Score")

# Chart 2
axes[1].bar(category_counts.index, category_counts.values)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")

# Chart 3
axes[2].scatter(popular["score"], popular["num_comments"], 
                color="red", label="Popular")
axes[2].scatter(not_popular["score"], not_popular["num_comments"], 
                color="blue", label="Not Popular")

axes[2].set_title("Score vs Comments")
axes[2].legend()

plt.suptitle("TrendPulse Dashboard")

plt.tight_layout()

plt.savefig("outputs/dashboard.png")

plt.show()

print("All charts saved successfully")
