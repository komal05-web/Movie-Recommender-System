# 🎬 Movie Recommender System

A content‑based movie recommendation system built with **Python**, **scikit‑learn**, and **Streamlit**.  
It uses the TMDB 5000 dataset, processes movie metadata (overview, genres, keywords, cast, crew), and generates recommendations based on cosine similarity of feature vectors. Posters are fetched dynamically from the TMDB API.

---

## 📂 Project Structure
MovieRecommender-main/ 
├── app.py                # Streamlit app 
├── movie_dict.pkl        # Pickled movie metadata dictionary 
├── similarity.pkl        # Pickled similarity matrix 
├── README.md             # Project documentation 
└── data/                 # Raw TMDB dataset (movies + credits CSVs)

---

## ⚙️ Features

- Preprocesses movie metadata (genres, keywords, cast, crew, overview).
- Builds a **bag-of-words model** with stemming and vectorization.
- Computes a **cosine similarity matrix** for recommendations.
- Interactive **Streamlit UI**:
  - Select a movie from a dropdown.
  - Get top 5 recommended movies.
  - Display movie posters using TMDB API.

---

## 🛠️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/MovieRecommender-main.git
cd MovieRecommender-main


#Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

pip install -r requirements.txt
## Prepare data
Download the TMDB 5000 dataset (tmdb_5000_movies.csv and tmdb_5000_credits.csv) and place them in a data/ folder.

##Generate pickle files
Run the preprocessing notebook to create movie_dict.pkl and similarity.pkl:

import pickle

# Save movies DataFrame as dict
pickle.dump(new_df.to_dict(), open('movie_dict.pkl','wb'))

# Save similarity matrix
pickle.dump(similarity, open('similarity.pkl','wb'))

## 🚀 Run the App

streamlit run app.py

