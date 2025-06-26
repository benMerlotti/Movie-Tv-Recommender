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

            raw_genre_names = cleaned_movie_entry.get('genre_names', "")
            processed_genre_names = []

            if isinstance(raw_genre_names, list):
                for name_string in raw_genre_names:
                    if isinstance(name_string, str):
                        name_lower = name_string.lower()
                        name_formatted = name_lower.replace(" ", "")
                        name_formatted_punctuation = name_formatted.replace(".", "")
                        processed_genre_names.append(name_formatted_punctuation)
            cleaned_movie_entry['processed_genre_names'] = processed_genre_names

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

            raw_keywords = cleaned_movie_entry.get('keyword_names', [])
            processed_keywords = []

            if isinstance(raw_keywords, list):
                for name_string in raw_keywords:
                    if isinstance(name_string, str):
                        name_lower = name_string.lower()
                        name_formatted = name_lower.replace(" ", "")
                        name_formatted_punctuation = name_formatted.replace(".", "")
                        processed_keywords.append(name_formatted_punctuation)
            cleaned_movie_entry['processed_keywords'] = processed_keywords

            

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

            raw_cast = cleaned_movie_entry.get('cast', [])
            processed_cast = []

            if isinstance(raw_cast, list):
                for name_string in raw_cast:
                    if isinstance(name_string, str):
                        name_lower = name_string.lower()
                        name_formatted = name_lower.replace(" ", "")
                        name_formatted_punctuation = name_formatted.replace(".", "")
                        processed_cast.append(name_formatted_punctuation)
            cleaned_movie_entry['processed_cast'] = processed_cast


            # Get Director

            directors_names_found = []
            crew_from_movie = credits_from_movie.get('crew', [])

            for crew_member in crew_from_movie:
                if crew_member['job'] == 'Director':
                    name = crew_member.get('name')
                    if name:
                        directors_names_found.append(name)

            cleaned_movie_entry['director'] = directors_names_found

            raw_director = cleaned_movie_entry.get('director', "")
            processed_director = []

            if isinstance(raw_director, list):
                for name_string in raw_director:
                    if isinstance(name_string, str):
                        name_lower = name_string.lower()
                        name_formatted = name_lower.replace(" ", "")
                        name_formatted_punctuation = name_formatted.replace(".", "")
                        processed_director.append(name_formatted_punctuation)
            cleaned_movie_entry['director_processed'] = processed_director



            # Get Overview

            cleaned_movie_entry['overview'] = raw_movie_dict.get('overview', "")

            raw_overview = cleaned_movie_entry.get('overview', "")

            processed_overview = raw_overview.lower()

            cleaned_movie_entry['overview_processed'] = processed_overview

            # --- Build Content Soup ---

            soup_components = []

           # 1. Overview (split into words)
            overview_str = cleaned_movie_entry.get('overview_processed', "")
            if overview_str: # Check if it's not an empty string
                soup_components.extend(overview_str.split()) # Split by space and add words

            # 2. Genres (already a list of processed strings)
            genres_list = cleaned_movie_entry.get('genres_processed', [])
            soup_components.extend(genres_list)

            # 3. Keywords (already a list of processed strings)
            keywords_list = cleaned_movie_entry.get('keywords_processed', [])
            soup_components.extend(keywords_list)

            # 4. Top Cast (already a list of processed strings)
            #    Consider adding cast members multiple times to give them more weight (optional)
            #    Example: for _ in range(2): soup_components.extend(top_cast_list)
            top_cast_list = cleaned_movie_entry.get('top_cast_processed', [])
            soup_components.extend(top_cast_list) 
            # If you want to weight them, you could do:
            # for _ in range(2): # Add each cast member twice
            #    soup_components.extend(top_cast_list)


            # 5. Director (a single processed string, or None)
            #    Consider adding director multiple times for weight (optional)
            #    Example: for _ in range(3): if director_str: soup_components.append(director_str)
            director_list = cleaned_movie_entry.get('director_processed', [])
            if director_list: # Check if it's not None and not an empty string
                soup_components.extend(director_list)
                # If you want to weight the director, you could do:
                # soup_components.append(director_str) # Add a second time
                # soup_components.append(director_str) # Add a third time

            # 6. Join all components into a single string, separated by spaces
            final_content_soup = " ".join(soup_components)
            
            cleaned_movie_entry['content_soup'] = final_content_soup
            # --- End Create Content Soup ---

            print(f"Processing: ID {cleaned_movie_entry['id']}, Title: {cleaned_movie_entry['title']}, Genres: {cleaned_movie_entry['genre_names']}, Keywords: {cleaned_movie_entry['keyword_names']}")

            processed_movies_list.append(cleaned_movie_entry)


        print(f"\nFinished processing. {len(processed_movies_list)} movies processed.")
    # Later, we'll save processed_movies_list to a new file.
    # If you want to see the first processed entry:
    if len(processed_movies_list) > 0:
        print("\nFirst processed movie entry (so far):")
        # pp.pprint(processed_movies_list[0]) # if you have pprint imported and pp defined
        print(processed_movies_list[0])

        print('test')

