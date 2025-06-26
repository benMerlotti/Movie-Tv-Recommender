import json
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_processed_movie_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def get_recommendations(input_title, titles_list, similarity_matrix, num_recommendations=10):
    
    print(f"Getting recommendations for {input_title}")

    try:
        movie_idx = titles_list.index(input_title)
    except ValueError:
        return f"Error: Movie '{input_title}' is not found in the dataset"
    
    similarity_scores_for_input_movie = similarity_matrix[movie_idx]

    movie_similarity_pairs = list(enumerate(similarity_scores_for_input_movie))

    sorted_similar_movies = sorted(movie_similarity_pairs, key=lambda item: item[1], reverse=True)

    recommended_movie_indices_scores = sorted_similar_movies[1 :num_recommendations + 1]

    recommended_titles = []
    for recommended_idx, score in recommended_movie_indices_scores:
        recommended_titles.append(f"{titles_list[recommended_idx]} (Score:{score:.4f})")

    if not recommended_titles:
        return "No recommendations found (other than the movie itself)."
        
    return recommended_titles



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

            if movie_titles:
                test_movie_index = 0

                if 0 <= test_movie_index < len(movie_titles):
                    test_movie_title = movie_titles[test_movie_index]

                    print(f"\n--- Attempting to get recommendations for: '{test_movie_title}' ---")

                    recommendations = get_recommendations(
                        input_title=test_movie_title,
                        titles_list=movie_titles,
                        similarity_matrix=cosine_sim_matrix,
                        num_recommendations=5
                    )

                    if isinstance(recommendations, str):
                        print(recommendations)
                    elif recommendations:
                        print(f"\nTop 5 recommendations for '{test_movie_title}':")
                        for i, rec_title_with_score in enumerate(recommendations):
                            print(f" {i+1}. {rec_title_with_score}")
                    else:
                        print("Received an empty list of recommendations.")
                else:
                    print(f"Error Test movie index {test_movie_index}  is out of bounds.")
            else:
                print("Error: movie_titles list is empty, cannpt pick a test movie")
                    
    else:
        print("Failed to load processed movie data")