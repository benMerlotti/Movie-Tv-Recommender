import json

def load_raw_movie_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    raw_data_filepath = "tmdb_movies_raw_data.json"
    raw_movies_list = load_raw_movie_data(raw_data_filepath)

    if raw_movies_list:
        processed_movies_list = []

        print(f"\nStarting to process {len(raw_movies_list)} movies...")
        for raw_movie_dict in raw_movies_list:
            cleaned_movie_entry = {}

            cleaned_movie_entry['id'] = raw_movie_dict['id']
            cleaned_movie_entry['title'] = raw_movie_dict['title']

            print(f"Processing: ID {cleaned_movie_entry['id']}, Title: {cleaned_movie_entry['title']}")

            processed_movies_list.append(cleaned_movie_entry)

        print(f"\nFinished processing. {len(processed_movies_list)} movies processed.")
    # Later, we'll save processed_movies_list to a new file.
    # If you want to see the first processed entry:
    if len(processed_movies_list) > 0:
        print("\nFirst processed movie entry (so far):")
        # pp.pprint(processed_movies_list[0]) # if you have pprint imported and pp defined
        print(processed_movies_list[0])

