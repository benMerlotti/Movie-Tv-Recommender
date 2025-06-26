import json
import requests

def load_processed_movie_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

if __name__ == "__main__":
    movies_data = load_processed_movie_data('movies_prepared_for_recommender.json')

    if movies_data:
        corpus = []
        for movie in movies_data:
            soup = movie.get('content_soup', "")
            corpus.append(soup)

        print(f"Created corpus with {len(corpus)} documents.")
        if corpus:
            print(f"First document in corpus: {corpus[0][:200]}")