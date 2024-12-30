from flask import Flask, request, jsonify
from datetime import datetime
from typing import List
import pandas as pd
import unicodedata
import pickle
import string
import hashlib
import os

app = Flask(__name__)
MODEL_PATH = "/mnt/data/rules.p"

last_checksum = None
last_rules = None

def get_checksum(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def load_rules():
    global last_checksum, last_rules
    if not os.path.exists(MODEL_PATH): raise Exception("no rule generator file")
    if get_checksum(MODEL_PATH) == last_checksum: return last_rules
    
    print("loading rules...")
    try:
        last_rules = pickle.load(open(MODEL_PATH, "rb"))
        last_checksum = get_checksum(MODEL_PATH)

    except FileNotFoundError:
        last_rules = None
        print(f"Model file not found at {MODEL_PATH}. \
        Please ensure the rules exists.")
    return last_rules


r = load_rules()
r = load_rules()
def normalize_track_name(track_name: str) -> str:
    track_name = track_name.lower()
    track_name = unicodedata.normalize('NFC', track_name)
    track_name = track_name.strip()
    track_name = track_name.translate(
        str.maketrans('', '', string.punctuation))
    return track_name


def recommend_songs(user_songs: List[str],
                    rules: pd.DataFrame,
                    top_n: int = 5) -> str:
    """
    Recommend songs based on association rules.
    Parameters:
        user_songs (list): List of songs the user likes.
        rules (DataFrame): Association rules with columns \
        ['antecedents', 'consequents', 'confidence', 'lift'].
        top_n (int): Number of top recommendations to return.
    Returns:
        DataFrame: Top recommended songs with associated metrics.
    """
    user_songs = [normalize_track_name(x) for x in user_songs]

    # Filter rules where the antecedent is a subset of user songs
    matching_rules = rules[rules['antecedents'].apply(
        lambda x: set(user_songs).issubset(x))].copy()

    # If none of the rules match the query, respond in random
    if not len(matching_rules):
        matching_rules = rules.sample(n=top_n**2)

    # Exclude songs already in user's list
    matching_rules['recommended_songs'] = matching_rules['consequents'].apply(
        lambda x: x - set(user_songs))

    # Remove duplicate rows based on the 'recommended_songs' column
    matching_rules = matching_rules.drop_duplicates(
        subset=['recommended_songs'])

    # Flatten recommendations and calculate scores
    recommendations = (
        matching_rules.explode('recommended_songs')
        .dropna(subset=['recommended_songs'])
        .sort_values(by=['confidence', 'lift'], ascending=False)
    )

    recommendations = recommendations[[
        'recommended_songs',
        'confidence',
        'lift']].head(top_n).to_json()

    return recommendations

# Define the route for recommendations
@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.get_json(force=True)
    user_songs = data.get("songs", [])

    if not user_songs:
        return jsonify({
            "error": "Invalid input. \
            Please provide a list of songs in the 'songs' field."
        }), 400

    rules = load_rules()
    recommendations = recommend_songs(user_songs, rules)
    response = {
        "songs": recommendations,
        "version": "1.0.0",
        "model_date": datetime.now().strftime("%Y-%m-%d"),
    }
    return jsonify(response)

if __name__ == "__main__":
    host = os.environ.get('FLASK_RUN_HOST')
    port = os.environ.get('FLASK_RUN_PORT')
    port = int(port)
    app.run(host=host, port=port)
