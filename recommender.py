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

          # --- INTERACTIVE RECOMMENDATION LOOP (This is the CLI part) ---
            print("\n--- Movie Recommender Ready! ---")
            print("Enter a movie title to get recommendations.")
            print("Type 'quit' (or 'exit', 'q') to stop.")

            while True: # Start an infinite loop (we'll break out of it)
                user_input_title = input("\nMovie title: ") # Prompt user and get their input

                # Check if the user wants to quit
                if user_input_title.lower() in ['quit', 'exit', 'q']:
                    print("Exiting recommender. Goodbye!")
                    break # Exit the while loop

                if not user_input_title: # Handle if the user just presses Enter
                    print("Please enter a movie title or type 'quit'.")
                    continue # Go to the start of the loop for new input

                # Call your existing recommendation function
                recommendations = get_recommendations(
                    input_title=user_input_title, 
                    titles_list=movie_titles,
                    similarity_matrix=cosine_sim_matrix,
                    num_recommendations=5 # Or however many you want to show
                )

                # Display the results
                if isinstance(recommendations, str): # Check if it returned an error message string
                    print(recommendations) # Print the error (e.g., "Movie not found")
                elif recommendations: # Check if the list of recommendations is not empty
                    print(f"\nTop 5 recommendations for '{user_input_title}':")
                    for i, rec_title_with_score in enumerate(recommendations, start=1):
                        print(f"  {i}. {rec_title_with_score}")
                else: # This case should ideally be covered by the error string check
                      # but good to have a fallback.
                    print(f"Sorry, no recommendations found for '{user_input_title}'.")
            # --- END INTERACTIVE LOOP ---