import streamlit as st
import pickle
import pandas as pd
import requests

# Set the page config to wide mode
st.set_page_config(layout="wide")

# Load the data
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

# Fetch movie poster from API
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a80455b985b1f48ddf19fca89eba7ff1&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Recommend movies based on selected movie
def recommend(movie):
    if movie not in movies['title'].values:
        return "Movie not found in database.", []
    
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Streamlit App
st.title('Movie Recommender System')
st.write("Welcome to the Movie Recommender System. Please select a movie from the dropdown list and we'll recommend similar movies that you might like.")

selected_movie_name = st.selectbox(
    'Select a movie:',
    [''] + list(movies['title'].values)
)

if st.button('Recommend'):
    if selected_movie_name:
        names,posters = recommend(selected_movie_name)
        
        if posters:
            col1, col2, col3, col4, col5 = st.columns(5)
            columns = [col1, col2, col3, col4, col5]
             
            for i in range(5):
                with columns[i]:
                    # st.image(posters[i])
                    st.markdown(f'<img src="{posters[i]}" style="max-width:100%; margin-bottom:10px; pointer-events: none;">', unsafe_allow_html=True)
                    st.write(f'<p style="text-align: center;">{names[i]}</p>', unsafe_allow_html=True)
        else:
            st.write(names)
    else:
        st.write("Please select a movie.")
