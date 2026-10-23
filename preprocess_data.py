import pandas as pd

df = pd.read_csv("movies_with_genres.csv")

print("Before cleaning:", len(df))

df = df.drop_duplicates(subset="title")
df = df.dropna(subset=["overview", "genres"])

df["overview"] = df["overview"].astype(str).str.strip()
df["genres"] = df["genres"].astype(str).str.strip()

df = df[
    (df["overview"] != "") &
    (df["genres"] != "")
]

df.to_csv("cleaned_movies.csv", index=False)

print("After cleaning:", len(df))
print("Cleaned dataset saved!")
print(df[["title", "genres"]].head())