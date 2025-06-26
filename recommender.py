import json
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_processed_movie_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

if __name__ == "__main__":
    movies_data = load_processed_movie_data('movies_prepared_for_recommender.json')

    if movies_data:
        corpus = []

        movie_titles = []
        movie_ids = []

        for movie_idx, movie in enumerate(movies_data):
            soup = movie.get('content_soup', "")
            corpus.append(soup)
            movie_titles.append(movie.get('title', "N/A"))
            movie_ids.append(movie.get('id', -1))

        if not corpus:
            print("Corpus is empty. Exiting.")

        else:
            print(f"Created corpus with {len(corpus)} documents.")
            print(f"First document in corpus: {corpus[0][:200]}")

            tfidf_vectorizer = TfidfVectorizer(stop_words='english')

            tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

            print(f"Shape of TF-IDF matrix: {tfidf_matrix.shape}")

            print("\nCalculating cosine similarity matrix...")

            cosine_sim_matrix = cosine_similarity(tfidf_matrix)

            print(f"Shape of Cosine Similarity matrix: {cosine_sim_matrix.shape}")
    else:
        print("Failed to load processed movie data")