import pickle
import streamlit as st
import requests

def fetch_poster_and_imdb(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=cc35fffd90141ea2e9a9c17715ece274&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"http://image.tmdb.org/t/p/w500{poster_path}"
    imdb_id = data['imdb_id']
    return full_path, imdb_id

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_imdb_ids = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster, imdb_id = fetch_poster_and_imdb(movie_id)
        recommended_movie_posters.append(poster)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_imdb_ids.append(imdb_id)
    return recommended_movie_names, recommended_movie_posters, recommended_movie_imdb_ids

st.set_page_config(page_title="MovIO", page_icon=":clapper:", layout="wide")
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f0f0; /* Light grey background for a clean look */
    }
    .stButton button {
        background-color: #000000; /* Black background for the button */
        color: white !important; /* White text color for the button */
        border: none;
        padding: 12px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 20px auto; /* Center align the button */
        cursor: pointer;
        border-radius: 8px;
        display: block;
    }
    .stButton button:focus, .stButton button:active {
        color: white !important; /* Keep text white on focus and active states */
    }
    .stSelectbox select {
        border-radius: 8px;
        cursor: pointer; /* Change cursor to pointer */
    }
    .stMarkdown, .stText {
        color: #333333; /* Dark text color for better visibility */
    }
    .stImage img {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        display: block;
        margin: 0 auto; /* Center align images */
    }
    .title {
        color: #000000; /* Black color for the title */
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .description {
        color: #555555; /* Slightly lighter text for the description */
        font-size: 18px;
        text-align: center;
        margin-bottom: 20px;
    }
    .heading {
        color: #000000; /* Black color for headings */
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
    }
    .stSelectbox label {
        color: #000000 !important; /* Force black color for selectbox label */
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">🎬 MovIO: Movie Recommendations</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="description">Discover movies you’ll love with our personalized recommendations. Select a movie from the dropdown menu and get a list of similar movies with their posters and IMDb links.</div>',
    unsafe_allow_html=True
)

movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

movie_list = movies['title'].values
placeholder = "Select a movie"
selected_movie = st.selectbox(
    'Type or select a movie to get recommendations',
    [placeholder] + list(movie_list),
    index=0,
    help="Please select a movie from the list or type to search.",
    label_visibility="visible"
)

if selected_movie != placeholder:
    show_recommendations = st.button('Show Recommendations')
    
    if show_recommendations:
        recommended_movie_names, recommended_movie_posters, recommended_movie_imdb_ids = recommend(selected_movie)

        st.markdown('<div class="heading">Recommended Movies:</div>', unsafe_allow_html=True)
        
        cols = st.columns(5)
        for i, col in enumerate(cols):
            if i < len(recommended_movie_names):
                with col:
                    st.markdown(f"**{recommended_movie_names[i]}**", unsafe_allow_html=True)
                    st.markdown(
                        f'<a href="https://www.imdb.com/title/{recommended_movie_imdb_ids[i]}" target="_blank"><img src="{recommended_movie_posters[i]}" width="100"></a>',
                        unsafe_allow_html=True
                    )
            else:
                with col:
                    st.empty()
