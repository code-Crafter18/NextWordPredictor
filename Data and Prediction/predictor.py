from flask import Flask, request, jsonify
import json
from difflib import get_close_matches
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend requests

DICT_FILE = "ngram_dict.json"

# Load n-gram dictionary
def load_ngram_dict():
    with open(DICT_FILE, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return {tuple(k.split("|||")): v for k, v in data.items()}

ngram_dict = load_ngram_dict()

def predict_next_words(context_tuple, top_k=3):
    """Predict next words using backoff logic."""
    for length in range(len(context_tuple), 0, -1):
        sub_tuple = context_tuple[-length:]
        if sub_tuple in ngram_dict:
            next_words_dict = ngram_dict[sub_tuple]
            break
    else:
        return []

    sorted_words = sorted(next_words_dict.items(), key=lambda x: x[1], reverse=True)
    return [word for word, count in sorted_words][:top_k]

# --- THIS IS THE UPDATED FUNCTION ---
def predict_current_word(context_tuple, partial_word, top_k=3):
    """
    Autocomplete the current partial word.
    This version correctly handles single letters and uses prefix matching.
    """
    candidates = set()
    
    # If there is no context (i.e., we are typing the first word)
    if not context_tuple:
        # Our candidates are all words that can start a phrase in our model
        for key in ngram_dict.keys():
            if len(key) == 1:
                candidates.add(key[0])
    # If there is context, find all words that can follow it
    else:
        for key, next_words in ngram_dict.items():
            if key == context_tuple:
                candidates.update(next_words.keys())

    if not candidates:
        return []


    matches = sorted([word for word in candidates if word.startswith(partial_word)])
    
    return matches[:top_k]

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data or 'context' not in data or 'mode' not in data:
        return jsonify({"error": "Missing fields"}), 400

    words = data['context'].strip().lower().split()
    mode = data['mode']

    if mode == "next":
        context_tuple = tuple(words[-4:])
        predictions = predict_next_words(context_tuple)
        
    elif mode == "current":
        if not words:
            return jsonify({"predictions": []})
        partial_word = words[-1]
        context_tuple = tuple(words[:-1])
        context_tuple = context_tuple[-3:]
        predictions = predict_current_word(context_tuple, partial_word)
    else:
        return jsonify({"error": "Invalid mode"}), 400

    return jsonify({"predictions": predictions})

if __name__ == "__main__":
    print("🚀 Running predictor backend on http://127.0.0.1:5000")
    app.run(debug=True)