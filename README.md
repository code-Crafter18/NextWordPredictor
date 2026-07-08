# Next Word Predictor with Autocomplete

A next-word prediction system built with a 4-gram language model and backoff strategy, served through a Flask API with a simple web interface for real-time predictions.

## Features
- 4-gram language model with backoff strategy (falls back to 3-gram/2-gram/1-gram when a full 4-gram match isn't found) to improve prediction accuracy and coverage
- Flask API that serves predictions to the frontend
- Simple web page with a text input bar — displays next-word / autocomplete suggestions as you type
- Prefix matching for autocomplete suggestions

## Tech Stack
- **Backend:** Python, Flask
- **Modeling:** N-gram language model (4-gram with backoff)
- **Frontend:** HTML, CSS, JavaScript (basic input + display page)

## Project Structure
- **Data and Prediction/** – training data and prediction/model logic
- **next_word_predictor/** – Flask app and web interface


## How It Works
1. The model is trained on a text corpus, building a frequency table of 4-word sequences.
2. When a user types text, the last 3 words are used to look up the most likely next word.
3. If no match is found, the model backs off to a 3-gram, then 2-gram, then 1-gram lookup.
4. Predictions are returned via the Flask API and displayed instantly on the page, along with prefix-matched autocomplete suggestions.
