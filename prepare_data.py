import json

def load_raw_movie_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    raw_data_filepath = "tmdb_movies_raw_data.json"
    movie_data = load_raw_movie_data(raw_data_filepath)

    if movie_data:
        print(len(movie_data))