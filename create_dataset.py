# import requests



# url = "https://api.themoviedb.org/3/movie/top_rated"

# params = {
#     "api_key": API_KEY,
#     "page": 1
# }

# response = requests.get(url, params=params)
# data = response.json()

# print("Total pages:", data["total_pages"])
# print("Movies found:", len(data["results"]))
# print("First movie:", data["results"][0]["title"])

# import requests
# import pandas as pd

# API_KEY =  # Replace with your actual API key

# movies = []

# for page in range(1, 6):
#     url = "https://api.themoviedb.org/3/movie/top_rated"
#     params = {"api_key": API_KEY, "page": page}

#     response = requests.get(url, params=params)
#     data = response.json()

#     for movie in data["results"]:
#         movies.append({
#             "title": movie["title"],
#             "overview": movie["overview"],
#             "genre_ids": movie["genre_ids"]
#         })

# df = pd.DataFrame(movies)
# df.to_csv("movies_dataset.csv", index=False)

# print("Dataset created successfully!")
# print("Total movies:", len(df))

import requests
import pandas as pd
import time
import os

from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
CSV_FILE = "movies_dataset.csv"

url = "https://api.themoviedb.org/3/movie/top_rated"

# Load existing dataset to resume progress
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    movies = df.to_dict("records")
    start_page = len(movies) // 20 + 1
    print("Existing movies:", len(movies))
    print("Resuming from page:", start_page)
else:
    movies = []
    start_page = 1

# Get total pages
try:
    response = requests.get(
        url,
        params={"api_key": API_KEY, "page": 1},
        timeout=30
    )
    response.raise_for_status()
    total_pages = response.json()["total_pages"]
    print("Total pages:", total_pages)
except requests.exceptions.RequestException as e:
    print("Could not connect to TMDB:", e)
    raise SystemExit

# Download pages with automatic retries
for page in range(start_page, total_pages + 1):

    success = False

    for attempt in range(1, 6):
        try:
            response = requests.get(
                url,
                params={"api_key": API_KEY, "page": page},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            if "results" not in data:
                raise ValueError("Unexpected API response")

            for movie in data["results"]:
                movies.append({
                    "title": movie["title"],
                    "overview": movie["overview"],
                    "genre_ids": movie["genre_ids"]
                })

            success = True
            break

        except (requests.exceptions.RequestException,
                ValueError, KeyError) as e:
            print(
                f"Page {page}, attempt {attempt}/5 failed: {e}"
            )
            time.sleep(3 * attempt)

    if not success:
        pd.DataFrame(movies).to_csv(CSV_FILE, index=False)
        print("Stopped. Progress saved.")
        print("Run the script again to resume.")
        break

    if page % 25 == 0 or page == total_pages:
        pd.DataFrame(movies).to_csv(CSV_FILE, index=False)
        print(
            f"Pages completed: {page}/{total_pages}"
        )
        print("Movies collected:", len(movies))

    time.sleep(0.2)

else:
    pd.DataFrame(movies).to_csv(CSV_FILE, index=False)
    print("Dataset completed successfully!")
    print("Total movies:", len(movies))