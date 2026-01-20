import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gzip
from dotenv import load_dotenv

# Fetch poster from TMDB API
def fetch_poster(movie_id):
    api_key = os.getenv("TMDB_API_KEY")
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)

    if response.status_code != 200:
        return "https://via.placeholder.com/500x750?text=No+Image"

    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"http://image.tmdb.org/t/p/w500/{poster_path}"
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Recommendation function
def recommend(movie):
    if movie not in movies['title'].values:
        return [], []

    # Because we reset index, this is now safe
    movie_index = movies[movies['title'] == movie].index[0]

    # Use iloc to ensure positional indexing
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommended_movies_posters

# Load data
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict).reset_index(drop=True)  # reset index here

# Load similarity matrix safely
if os.path.exists('similarity.pkl'):
    with open('similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)
elif os.path.exists('similarity.pkl.gz'):
    with gzip.open('similarity.pkl.gz', 'rb') as f:
        similarity = pickle.load(f)
else:
    st.error("similarity file not found. Please check your deployment files.")

# Verify alignment
if len(movies) != similarity.shape[0]:
    st.error(f"Mismatch: movies={len(movies)}, similarity={similarity.shape}")
else:
    # Streamlit UI
    st.title('🎬 Movie Recommender System')

    selected_movie_name = st.selectbox(
        'Select a movie:',
        movies['title'].values
    )

    if st.button('Recommend'):
        names, posters = recommend(selected_movie_name)

        if names:
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                with col:
                    st.text(names[idx])
                    st.image(posters[idx])
        else:
            st.warning("Movie not found in dataset.")
