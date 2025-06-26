import json
import requests

API_KEY = "2b6c4ad7ca2d1d55f39efe779b148a21"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

def load_raw_movie_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def fetch_genre_map():
    genre_list_url = f"{TMDB_BASE_URL}/genre/movie/list?api_key={API_KEY}"

    response = requests.get(genre_list_url)
    data = response.json()

    id_to_name_map = {}

    if 'genres' in data and data['genres']:
        for genre_item in data['genres']:
            genre_id = genre_item.get('id')
            genre_name = genre_item.get('name')
            if genre_id is not None and genre_name is not None:
                id_to_name_map[genre_id] = genre_name

    return id_to_name_map




if __name__ == "__main__":
    raw_data_filepath = "tmdb_movies_raw_data.json"
    raw_movies_list = load_raw_movie_data(raw_data_filepath)

    genre_id_name_map = fetch_genre_map()
    if not genre_id_name_map: # Check if the map was actually created
        print("Warning: Genre map is empty. Genre names will not be available for movies.")

    print(genre_id_name_map)

    if raw_movies_list:
        processed_movies_list = []

        print(f"\nStarting to process {len(raw_movies_list)} movies...")
        for raw_movie_dict in raw_movies_list:
            cleaned_movie_entry = {}

            cleaned_movie_entry['id'] = raw_movie_dict['id']
            cleaned_movie_entry['title'] = raw_movie_dict['title']

            list_of_genre_names_for_this_movie = []
            genre_ids_from_movie = raw_movie_dict.get('genre_ids', [])

            if genre_ids_from_movie and genre_id_name_map:
                for one_genre_id in genre_ids_from_movie:
                    name = genre_id_name_map.get(one_genre_id)
                    if name: 
                        list_of_genre_names_for_this_movie.append(name)

            cleaned_movie_entry['genre_names'] = list_of_genre_names_for_this_movie

            print(f"Processing: ID {cleaned_movie_entry['id']}, Title: {cleaned_movie_entry['title']}, Genres: {cleaned_movie_entry['genre_names']}")

            processed_movies_list.append(cleaned_movie_entry)

        print(f"\nFinished processing. {len(processed_movies_list)} movies processed.")
    # Later, we'll save processed_movies_list to a new file.
    # If you want to see the first processed entry:
    if len(processed_movies_list) > 0:
        print("\nFirst processed movie entry (so far):")
        # pp.pprint(processed_movies_list[0]) # if you have pprint imported and pp defined
        print(processed_movies_list[0])

