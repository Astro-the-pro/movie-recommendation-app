import pickle
import pandas as pd
import streamlit as st
import requests

# Load movie data and similarity matrix
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app UI
st.title('🎬 Hollywood Movie Recommendation System')

selected_movie_name = st.selectbox(
    'Select a movie you like:',
    movies['title'].values
)
combined_similarity = []

for i in range(1, 7):
    with open(f"similarity_part_{i}.pkl", "rb") as f:
        part = pickle.load(f)
        combined_similarity.extend(part)

# Now it's the full similarity matrix again


API_KEY = "92d940e8e1aeafc210c040464da7658c"

# Function to fetch poster and TMDB movie link
def fetch_poster_and_link(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        data = requests.get(url, timeout=5).json()
        poster_path = data.get('poster_path', '')
        poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/300x450?text=No+Poster"
        tmdb_link = f"https://www.themoviedb.org/movie/{movie_id}"
        return poster_url, tmdb_link
    except Exception as e:
        print(f"Error: {e}")
        return "https://via.placeholder.com/300x450?text=Error", "#"

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = combined_similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    posters = []
    links = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        poster_url, tmdb_link = fetch_poster_and_link(movie_id)
        recommended_movies.append(title)
        posters.append(poster_url)
        links.append(tmdb_link)

    return recommended_movies, posters, links

# Show recommendations
if st.button('Recommend'):
    names, posters, links = recommend(selected_movie_name)
    st.markdown("### ✨ You might also like:")
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            # Clickable title with TMDB link
            st.markdown(
                f"<a href='{links[i]}' target='_blank'><h5 style='color:#4CAF50; text-align: center;'>{names[i]}</h5></a>",
                unsafe_allow_html=True
            )
