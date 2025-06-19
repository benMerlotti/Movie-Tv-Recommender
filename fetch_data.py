import requests  # For making HTTP requests to websites/APIs
import json      # For working with JSON data (though requests often handles this for us)
import time      # For adding delays (pauses) in our script
# import os      # We might use this later for things like API keys from environment variables

API_KEY = "2b6c4ad7ca2d1d55f39efe779b148a21"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

def fetch_discover_movies(num_pages):

    local_all_movies = []

    for current_page_number in range(1, num_pages + 1):
        discover_movie_url = f"{TMDB_BASE_URL}/discover/movie?api_key={API_KEY}&sort_by=popularity.desc&page={current_page_number}"

        print(f"\nFetching data for page {current_page_number}...")
        print(f"Requesting URL: {discover_movie_url}")

        response = requests.get(discover_movie_url)

        if response.status_code == 200:
            data = response.json()
            if 'results' in data and data['results']:
                local_all_movies.extend(data['results'])
                print(f"Successfully fetched {len(data['results'])} movies from page {current_page_number}.")
            else:
                print(f"No movies found on page {current_page_number} or 'results' key missing.")

        else:
            print(f"Request for page {current_page_number} failed with status code: {response.status_code}")
            print(f"Response content: {response.text}")
            break
        print("Pausing...")
        time.sleep(0.5)

    print(f"\n--- All Pages Fetched ---")
    print(f"Total movies collected: {len(local_all_movies)}")
    if local_all_movies:
        print("Sample of collected movies (first 3):")
        for movie in local_all_movies[:3]:
            print(f"ID: {movie.get('id')}, Title: {movie.get('title')}")

    return local_all_movies

def fetch_keywords_and_credit_for_movies(list_of_movie_dictionaries):

    for movie_dict in list_of_movie_dictionaries:
        movie_id = movie_dict.get('id')

        if not movie_id:
            print(f"Skipping movie with no ID: {movie_dict.get('title', 'Unknown Title')}")
            continue
        
        # --- Fetch Keywords ---
        keywords_url = f"{TMDB_BASE_URL}/movie/{movie_id}/keywords?api_key={API_KEY}"
        print(f"Requesting Keywords URL: {keywords_url}")
        try:
            response_keywords = requests.get(keywords_url)
            response_keywords.raise_for_status()
            keywords_data = response_keywords.json()
            movie_dict['keywords_data'] = keywords_data
            print(f"Successfully fetched keywords.")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error fetching keywords for movie ID {movie_id}: {http_err}")
            movie_dict['keywords_data'] = {'error': str(http_err)} # Store error info
        except Exception as err:
            print(f"    Error fetching keywords for movie ID {movie_id}: {err}")
            movie_dict['keywords_data'] = {'error': str(err)}
        
        time.sleep(0.3) # Pause after keywords call

        # --- Fetch Credits ---
        credits_url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits?api_key={API_KEY}"
        print(f"Requesting Credits URL: {credits_url}")
        try:
            response_credits = requests.get(credits_url)
            response_credits.raise_for_status()
            credits_data = response_credits.json()
            movie_dict['credits_data'] = credits_data
            print(f"Succesfully fetched credits.")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error fetching keywords for movie ID {movie_id}: {http_err}")
            movie_dict['keywords_data'] = {'error': str(http_err)} # Store error info
        except Exception as err:
            print(f"    Error fetching keywords for movie ID {movie_id}: {err}")
            movie_dict['keywords_data'] = {'error': str(err)}
        
        time.sleep(0.3) # Pause after keywords call
    print("\n--- Finished fetching keywords and credits ---")
    return list_of_movie_dictionaries

# Main ----------------------------------------------------------------

if __name__ == "__main__":
    desired_pages = 5

    discovered_movies = fetch_discover_movies(desired_pages)

    if discovered_movies:
        print(f"\nSuccessfully retrieved {len(discovered_movies)} basic movie entries.")
        print("Sample of first 3 movies retrieved:")
        for movie in discovered_movies[:3]:
            print(f"  ID: {movie.get('id')}, Title: {movie.get('title')}")
        print("\nNow enriching movies with keyowrds and credits...")
        enriched_movies = fetch_keywords_and_credit_for_movies(discovered_movies)
        if enriched_movies:
            output_filename = "tmdb_movies_raw_data.json"
            print(f"\nSaving all {len(enriched_movies)} enriched movies data to {output_filename}...")
            try:
                with open(output_filename, 'w', encoding='utf-8') as outfile:
                    json.dump(enriched_movies, outfile, indent=2)
                print(f"Successully saved data to {output_filename}")
            except IOError as e:
                print(f"Error: Could not write to file {output_filename}. IO Error {e}")
            except Exception as e:
                print(f"An unexpected error occurred while saving to file: {e}")
        else:
            print("\nNo movie data was enriched, so nothing to save.")
    else:
        print("No movies were retrieved from the discover endpoint.")

    