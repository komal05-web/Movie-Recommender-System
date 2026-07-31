import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gzip
import time
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
IMG_BASE = "http://image.tmdb.org/t/p/w500"
BACKDROP_BASE = "http://image.tmdb.org/t/p/w1280"
PLACEHOLDER = "https://via.placeholder.com/500x750/141826/E8B84B?text=No+Poster"
PERSON_PLACEHOLDER = "https://via.placeholder.com/300x300/141826/8B93A7?text=No+Photo"

st.set_page_config(page_title="CineMatch", page_icon="🎬", layout="wide")


# ---------------------------------------------------------
# Theme: cinema marquee — dark navy house, gold marquee
# lights, film-strip sprockets as the signature divider.
# ---------------------------------------------------------

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg-primary: #0B0E1A;
    --bg-card: #161B2E;
    --accent-gold: #F4B942;
    --accent-red: #E63950;
    --text-primary: #FFFFFF;
    --text-muted: #A8B0C3;
}

.stApp {
    background: linear-gradient(180deg, #10142380 0%, #0B0E1A 100%), #0B0E1A;
    color: var(--text-primary);
    font-family: 'Inter', sans-serif;
}

h1 {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: 0.01em;
    color: var(--accent-gold) !important;
    text-align: center;
    font-size: 2.9rem !important;
    padding-top: 0.2rem;
    margin-bottom: 0 !important;
    line-height: 1.2 !important;
}

h2, h3 {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.01em;
    color: var(--text-primary) !important;
}

p, span, div, label {
    font-family: 'Inter', sans-serif;
}

.subtitle {
    text-align: center;
    color: var(--text-muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-size: 0.85rem;
    font-weight: 600;
    margin-top: 4px;
    margin-bottom: 1.4rem;
}

.filmstrip {
    height: 14px;
    margin: 1.4rem 0 1.6rem 0;
    background-image: radial-gradient(circle, #07090F 3px, transparent 3.5px);
    background-size: 22px 14px;
    background-position: center;
    border-top: 1px solid rgba(232,184,75,0.25);
    border-bottom: 1px solid rgba(232,184,75,0.25);
    opacity: 0.9;
}

.movie-card {
    position: relative;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 6px 18px rgba(0,0,0,0.55);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    border: 1px solid rgba(232,184,75,0.15);
}
.movie-card:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 14px 30px rgba(232,184,75,0.25);
}
.movie-card img { width: 100%; display: block; }

.movie-title {
    text-align: center;
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    line-height: 1.3;
    color: var(--text-primary);
    margin-top: 0.6rem;
    min-height: 2.6em;
}

.rating-badge {
    position: absolute;
    top: 8px;
    right: 8px;
    background: rgba(11,14,26,0.85);
    border: 1.5px solid var(--accent-gold);
    color: var(--accent-gold);
    font-weight: 700;
    font-size: 0.78rem;
    padding: 3px 8px;
    border-radius: 20px;
}

.genre-pill {
    display: inline-block;
    background: rgba(232,184,75,0.12);
    border: 1px solid rgba(232,184,75,0.4);
    color: var(--accent-gold);
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    margin: 2px 6px 2px 0;
}

.stButton > button {
    background: linear-gradient(135deg, var(--accent-gold), #C99A2E);
    color: #0B0E1A !important;
    font-weight: 700;
    border: none;
    border-radius: 24px;
    padding: 0.45rem 1.1rem;
    letter-spacing: 0.03em;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(232,184,75,0.35);
}

.cast-avatar {
    border-radius: 50%;
    border: 2px solid var(--accent-gold);
    width: 100%;
    aspect-ratio: 1/1;
    object-fit: cover;
    display: block;
}
.cast-name {
    text-align: center;
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-top: 4px;
}

.review-stub {
    background: var(--bg-card);
    border: 1px dashed rgba(232,184,75,0.35);
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.7rem;
}
.review-author {
    color: var(--accent-gold);
    font-weight: 700;
    font-size: 0.9rem;
}
.review-meta {
    color: var(--text-muted);
    font-size: 0.78rem;
    margin-bottom: 0.4rem;
}

.hero-backdrop {
    position: relative;
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 1.2rem;
    border: 1px solid rgba(232,184,75,0.2);
}
.hero-backdrop img { width: 100%; display: block; filter: brightness(0.55); }
.hero-overlay {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    padding: 1.5rem 1.8rem;
    background: linear-gradient(to top, rgba(7,9,15,1) 25%, rgba(7,9,15,0.75) 65%, transparent);
}
.hero-title {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    font-size: 2.2rem;
    line-height: 1.25;
    letter-spacing: 0.005em;
    color: #FFFFFF;
    margin-bottom: 6px;
}
.hero-meta {
    color: var(--text-muted);
    font-size: 0.95rem;
    font-weight: 500;
}

.now-showing {
    background: var(--bg-card);
    border: 1px solid rgba(232,184,75,0.2);
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.6rem;
}
.now-showing-label {
    color: var(--accent-gold);
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 6px;
}

div[data-baseweb="select"] > div {
    background-color: var(--bg-card) !important;
    border-color: rgba(244,185,66,0.5) !important;
    border-radius: 8px !important;
}

div[data-baseweb="select"] * {
    color: var(--text-primary) !important;
    font-weight: 500;
}

div[data-baseweb="select"] svg {
    fill: var(--accent-gold) !important;
}

[data-testid="stWidgetLabel"] p {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

ul[data-baseweb="menu"] {
    background-color: var(--bg-card) !important;
}

ul[data-baseweb="menu"] li {
    color: var(--text-primary) !important;
}

ul[data-baseweb="menu"] li:hover {
    background-color: rgba(244,185,66,0.15) !important;
}

[data-testid="stExpander"] {
    background: var(--bg-card);
    border: 1px dashed rgba(232,184,75,0.3);
    border-radius: 8px;
}
</style>
"""


def filmstrip_divider():
    st.markdown('<div class="filmstrip"></div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# Shared request helper: timeout + retry so a dropped
# connection never crashes the app, it just falls back.
# ---------------------------------------------------------

def safe_get(url, params=None, retries=3, timeout=10):
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            if response.status_code == 200:
                return response
            return None
        except requests.exceptions.RequestException:
            if attempt < retries - 1:
                time.sleep(1.5)
                continue
            return None
    return None


# ---------------------------------------------------------
# TMDB fetch helpers (cached so reruns don't re-hit the API)
# ---------------------------------------------------------

@st.cache_data(ttl=3600)
def fetch_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    response = safe_get(url, params={"api_key": TMDB_API_KEY, "language": "en-US"})
    if response is None:
        return {}
    return response.json()


@st.cache_data(ttl=3600)
def fetch_credits(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/credits"
    response = safe_get(url, params={"api_key": TMDB_API_KEY})
    if response is None:
        return {"cast": [], "crew": []}
    return response.json()


@st.cache_data(ttl=3600)
def fetch_similar(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/similar"
    response = safe_get(url, params={"api_key": TMDB_API_KEY, "language": "en-US"})
    if response is None:
        return []
    return response.json().get("results", [])[:5]


@st.cache_data(ttl=3600)
def fetch_trailer(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/videos"
    response = safe_get(url, params={"api_key": TMDB_API_KEY})
    if response is None:
        return None
    results = response.json().get("results", [])
    trailer = next(
        (v for v in results if v.get("type") == "Trailer" and v.get("site") == "YouTube"),
        None
    )
    return trailer["key"] if trailer else None


@st.cache_data(ttl=3600)
def fetch_reviews(movie_id, max_reviews=5):
    url = f"{BASE_URL}/movie/{movie_id}/reviews"
    response = safe_get(url, params={"api_key": TMDB_API_KEY, "language": "en-US"})
    if response is None:
        return []
    return response.json().get("results", [])[:max_reviews]


def poster_url(details):
    poster_path = details.get("poster_path")
    return f"{IMG_BASE}/{poster_path}" if poster_path else PLACEHOLDER


# ---------------------------------------------------------
# Recommendation logic
# ---------------------------------------------------------

def recommend(movie):
    if movie not in movies['title'].values:
        return []

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    results = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        details = fetch_movie_details(movie_id)
        results.append({
            "id": movie_id,
            "title": title,
            "poster": poster_url(details),
            "rating": details.get("vote_average"),
        })
    return results


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict).reset_index(drop=True)

if os.path.exists('similarity.pkl'):
    with open('similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)
elif os.path.exists('similarity.pkl.gz'):
    with gzip.open('similarity.pkl.gz', 'rb') as f:
        similarity = pickle.load(f)
else:
    st.error("similarity file not found. Please check your deployment files.")
    st.stop()

if len(movies) != similarity.shape[0]:
    st.error(f"Mismatch: movies={len(movies)}, similarity={similarity.shape}")
    st.stop()


# ---------------------------------------------------------
# Navigation state
# ---------------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "search"
if "selected_movie_id" not in st.session_state:
    st.session_state.selected_movie_id = None


def go_to_details(movie_id):
    st.session_state.selected_movie_id = movie_id
    st.session_state.page = "details"


def go_back():
    st.session_state.page = "search"
    st.session_state.selected_movie_id = None


# ---------------------------------------------------------
# Shared: poster card grid (used on search + details page)
# ---------------------------------------------------------

def render_movie_grid(items, key_prefix):
    cols = st.columns(len(items))
    for col, item in zip(cols, items):
        with col:
            rating = item.get("rating")
            badge = f'<div class="rating-badge">⭐ {rating:.1f}</div>' if rating else ""
            st.markdown(
                f"""
                <div class="movie-card">
                    <img src="{item['poster']}" />
                    {badge}
                </div>
                <div class="movie-title">{item['title']}</div>
                """,
                unsafe_allow_html=True
            )
            if st.button("View Details", key=f"{key_prefix}_{item['id']}"):
                go_to_details(item["id"])
                st.rerun()


# ---------------------------------------------------------
# PAGE 1: Search + Recommendations
# ---------------------------------------------------------

def render_search_page():
    st.markdown("<h1>🎬 CineMatch</h1>", unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Pick a film · find your next watch</div>', unsafe_allow_html=True)

    selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

    # "Now Showing" live preview of the selected movie
    sel_row = movies[movies['title'] == selected_movie_name].iloc[0]
    sel_details = fetch_movie_details(sel_row.movie_id)

    if sel_details:
        overview = sel_details.get("overview", "")
        overview_short = overview[:220] + "..." if len(overview) > 220 else overview
        genres = sel_details.get("genres", [])
        pills = "".join(f'<span class="genre-pill">{g["name"]}</span>' for g in genres)
        rating = sel_details.get("vote_average", "N/A")
        year = (sel_details.get("release_date") or "")[:4]

        p1, p2 = st.columns([1, 4])
        with p1:
            st.image(poster_url(sel_details), use_container_width=True)
        with p2:
            st.markdown(
                f"""
                <div class="now-showing">
                    <div class="now-showing-label">Now Selecting</div>
                    <div class="hero-title" style="font-size:1.7rem;">{sel_details.get('title', selected_movie_name)} {f'({year})' if year else ''}</div>
                    <div style="margin:6px 0;">{pills}</div>
                    <div style="color:var(--text-muted); font-size:0.9rem;">⭐ {rating}/10</div>
                    <p style="margin-top:8px; font-size:0.9rem; color:var(--text-primary);">{overview_short}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    if st.button('🎟 Get Recommendations'):
        st.session_state.recs = recommend(selected_movie_name)

    if st.session_state.get("recs"):
        filmstrip_divider()
        st.markdown("<h3>Recommended For You</h3>", unsafe_allow_html=True)
        render_movie_grid(st.session_state.recs, key_prefix="rec")


# ---------------------------------------------------------
# PAGE 2: Movie Details
# ---------------------------------------------------------

def render_details_page():
    movie_id = st.session_state.selected_movie_id

    if st.button("← Back to recommendations"):
        go_back()
        st.rerun()

    details = fetch_movie_details(movie_id)
    if not details:
        st.error("Could not load movie details.")
        return

    credits = fetch_credits(movie_id)

    # --- Hero backdrop ---
    backdrop_path = details.get("backdrop_path")
    rating = details.get("vote_average", "N/A")
    runtime = details.get("runtime", "N/A")
    release_date = details.get("release_date", "N/A")

    if backdrop_path:
        st.markdown(
            f"""
            <div class="hero-backdrop">
                <img src="{BACKDROP_BASE}/{backdrop_path}" />
                <div class="hero-overlay">
                    <div class="hero-title">{details.get('title', '')}</div>
                    <div class="hero-meta">⭐ {rating}/10 &nbsp;|&nbsp; ⏱ {runtime} min &nbsp;|&nbsp; 📅 {release_date}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(f"<h1 style='font-size:2.4rem;'>{details.get('title', '')}</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(poster_url(details), use_container_width=True)
    with col2:
        genres = details.get("genres", [])
        pills = "".join(f'<span class="genre-pill">{g["name"]}</span>' for g in genres)
        st.markdown(f'<div style="margin-bottom:10px;">{pills}</div>', unsafe_allow_html=True)

        language = details.get("original_language", "N/A")
        st.markdown(f"<span style='color:var(--text-muted);'>Original Language: {language}</span>", unsafe_allow_html=True)

        st.markdown("<h3>Overview</h3>", unsafe_allow_html=True)
        st.write(details.get("overview", "No overview available."))

    filmstrip_divider()

    director = next(
        (c["name"] for c in credits.get("crew", []) if c.get("job") == "Director"),
        "N/A"
    )
    st.markdown("<h3>🎬 Director</h3>", unsafe_allow_html=True)
    st.write(director)

    st.markdown("<h3>🎭 Top Cast</h3>", unsafe_allow_html=True)
    cast = credits.get("cast", [])[:5]
    if cast:
        cast_cols = st.columns(len(cast))
        for c, actor in zip(cast_cols, cast):
            with c:
                profile_path = actor.get("profile_path")
                img = f"{IMG_BASE}/{profile_path}" if profile_path else PERSON_PLACEHOLDER
                st.markdown(
                    f"""
                    <img class="cast-avatar" src="{img}" />
                    <div class="cast-name">{actor.get('name', '')}</div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.write("No cast information available.")

    trailer_key = fetch_trailer(movie_id)
    if trailer_key:
        filmstrip_divider()
        st.markdown("<h3>▶ Trailer</h3>", unsafe_allow_html=True)
        st.video(f"https://www.youtube.com/watch?v={trailer_key}")

    similar = fetch_similar(movie_id)
    if similar:
        filmstrip_divider()
        st.markdown("<h3>🎞 Similar Movies</h3>", unsafe_allow_html=True)
        similar_items = [
            {
                "id": sm["id"],
                "title": sm.get("title", ""),
                "poster": f"{IMG_BASE}/{sm['poster_path']}" if sm.get("poster_path") else PLACEHOLDER,
                "rating": sm.get("vote_average"),
            }
            for sm in similar
        ]
        render_movie_grid(similar_items, key_prefix="sim")

    reviews = fetch_reviews(movie_id)
    filmstrip_divider()
    st.markdown("<h3>📝 User Reviews</h3>", unsafe_allow_html=True)
    if reviews:
        for review in reviews:
            author = review.get("author", "Anonymous")
            content = review.get("content", "")
            author_details = review.get("author_details", {})
            review_rating = author_details.get("rating")
            created_at = review.get("created_at", "")[:10]
            rating_str = f" — ⭐ {review_rating}/10" if review_rating else ""

            if len(content) > 800:
                content = content[:800] + "..."

            st.markdown(
                f"""
                <div class="review-stub">
                    <div class="review-author">{author}{rating_str}</div>
                    <div class="review-meta">{created_at}</div>
                    <div>{content}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.write("No reviews yet for this movie.")


# ---------------------------------------------------------
# Router
# ---------------------------------------------------------

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

if st.session_state.page == "search":
    render_search_page()
elif st.session_state.page == "details":
    render_details_page()