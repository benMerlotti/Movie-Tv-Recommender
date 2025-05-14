import requests  # For making HTTP requests to websites/APIs
import json      # For working with JSON data (though requests often handles this for us)
import time      # For adding delays (pauses) in our script
# import os      # We might use this later for things like API keys from environment variables

API_KEY = "2b6c4ad7ca2d1d55f39efe779b148a21"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Example for fetching the first page of popular movies
page_number = 1
discover_movie_url = f"{TMDB_BASE_URL}/discover/movie?api_key={API_KEY}&sort_by=popularity.desc&page={page_number}"

print(f"Requesting URL: {discover_movie_url}") # Good for debugging to see what URL you're actually calling
response = requests.get(discover_movie_url)

if response.status_code == 200:
    print("Request successful!")
else: 
    print(f"Request failed with status code:{response.status_code}")
    print(f"Response content: {response.text}")

if response.status_code == 200:
    data = response.json()
    print("\n--- Parsed Data (first few movies) ---")
    if 'results' in data and data['results']:
        for movie in data['results'][:5]:
            movie_id = movie.get('id', 'N/A')
            title = movie.get('title', 'N/A')
            overview = movie.get('overview', 'N/A')
            print(f"ID: {movie_id}, Title: {title}")

    else:
        print("No 'results' found in the data or results list is empty.")
        