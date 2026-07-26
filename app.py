import streamlit as st
import pickle
import pandas as pd
import requests

API_KEY = "89e1546d"

@st.cache_data
def fetch_poster(movie):
    url = "https://www.omdbapi.com/"

    params = {
        "apikey": API_KEY,
        "t": movie
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("Response") == "True":
        return data.get("Poster")

    return None


# def recommend(movies):
#     l = []
#     distance = similarity[movie[movie['title'] == movies].index[0]]
#     similar_movies = sorted(enumerate(distance), reverse=True, key=lambda x: x[1])[1:6]
#     for i in similar_movies:
#         l.append(movie.iloc[i[0]].title)
#     return l

def recommend(movie):
    precomputed = top_movies[movies[movies['title'] == movie].index[0]][:5]

    precomputed_names = [
        movies.iloc[i]["title"]
        for i in precomputed
    ]
    return precomputed_names


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))
top_movies = pickle.load(open('top_movies.pkl','rb'))

st.title("Movie Recommender System")
st.write("Hello, *Guys!* :sunglasses:")

movie_name = st.selectbox(
    'Select one of the Movies',
    movies['title'].values)

if st.button('Recommend'):
    recommendation = recommend(movie_name)

    col = st.columns(5)


    for index, i in enumerate(recommendation):
        poster = fetch_poster(i)

        with col[index]:
            if poster:
                st.image(poster,width=150)
                st.write(i)
