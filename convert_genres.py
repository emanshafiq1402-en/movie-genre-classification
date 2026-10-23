import pandas as pd
import requests
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

url = "https://api.themoviedb.org/3/genre/movie/list"

response = requests.get(
    url,
    params={"api_key": API_KEY},
    timeout=30
)
response.raise_for_status()

genres = {
    genre["id"]: genre["name"]
    for genre in response.json()["genres"]
}

df = pd.read_csv("movies_dataset.csv")

def convert_genres(value):
    ids = eval(value) if isinstance(value, str) else value
    return ", ".join(
        genres[genre_id]
        for genre_id in ids
        if genre_id in genres
    )

df["genres"] = df["genre_ids"].apply(convert_genres)
df.to_csv("movies_with_genres.csv", index=False)

print("Conversion complete!")
print("Total movies:", len(df))
print(df[["title", "genres"]].head())