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

            # Get genre names using genre_id_name_map

            list_of_genre_names_for_this_movie = []
            genre_ids_from_movie = raw_movie_dict.get('genre_ids', [])

            if genre_ids_from_movie and genre_id_name_map:
                for one_genre_id in genre_ids_from_movie:
                    name = genre_id_name_map.get(one_genre_id)
                    if name: 
                        list_of_genre_names_for_this_movie.append(name)

            cleaned_movie_entry['genre_names'] = list_of_genre_names_for_this_movie

            # Get keyword names

            list_of_keyword_names_for_this_movie = []
            keywords_from_movie = raw_movie_dict.get('keywords_data')

            if keywords_from_movie and isinstance(keywords_from_movie, dict):
                list_of_keyword_dicts = keywords_from_movie.get('keywords')
                if list_of_keyword_dicts and isinstance(list_of_keyword_dicts, list):
                    for keyword_dict_item in list_of_keyword_dicts:
                        if isinstance(keyword_dict_item, dict):
                            name = keyword_dict_item.get('name')
                            if name:
                                list_of_keyword_names_for_this_movie.append(name)

            cleaned_movie_entry['keyword_names'] = list_of_keyword_names_for_this_movie

            # Get cast

            list_of_top_cast_names = []
            num_top_cast_to_extract = 3
            credits_from_movie = raw_movie_dict.get('credits_data', {})
            cast_from_movie = credits_from_movie.get('cast', [])
            if isinstance(cast_from_movie, list):
                for actor in cast_from_movie[:num_top_cast_to_extract]:
                    if isinstance(actor, dict):
                        name = actor.get('name')
                        if name:
                            list_of_top_cast_names.append(name)

            cleaned_movie_entry['cast'] = list_of_top_cast_names

            print(f"Processing: ID {cleaned_movie_entry['id']}, Title: {cleaned_movie_entry['title']}, Genres: {cleaned_movie_entry['genre_names']}, Keywords: {cleaned_movie_entry['keyword_names']}")

            processed_movies_list.append(cleaned_movie_entry)

        print(f"\nFinished processing. {len(processed_movies_list)} movies processed.")
    # Later, we'll save processed_movies_list to a new file.
    # If you want to see the first processed entry:
    if len(processed_movies_list) > 0:
        print("\nFirst processed movie entry (so far):")
        # pp.pprint(processed_movies_list[0]) # if you have pprint imported and pp defined
        print(processed_movies_list[0])

