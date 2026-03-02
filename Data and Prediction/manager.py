# Original manager.py (reads from data.txt)

import json
import re
from collections import defaultdict
from os.path import exists

file_name = "data.txt" # Reads from this text file
DICT_FILE = "ngram_dict.json" # Saves the dictionary here

def read_text(file_path):
    """Reads the text file and returns its content as a string."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            print(f"Successfully read {file_path}")
            return file.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return ""
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""


def preprocess(text):
    """Cleans and tokenizes text into words (including punctuation)."""
    text = text.lower()
    # This regex finds words or single non-word/non-space characters
    words = re.findall(r'\w+|[^\w\s]', text, re.UNICODE)
    return words

def build_ngram_dict(words):
    """Builds a dictionary with up to 4-gram contexts."""
    ngram_dict = defaultdict(lambda: defaultdict(int))
    # Look at sequences up to 5 words long (4 for context, 1 for the next word)
    for i in range(len(words) - 1):
        # Creates contexts of size 1, 2, 3, and 4
        for n in range(1, 5): # Creates 1-gram to 4-gram contexts
            if i + n < len(words):
                context = tuple(words[i : i + n])
                next_word = words[i + n]
                ngram_dict[context][next_word] += 1
    return ngram_dict

def load_existing_dict():
    """Loads existing dictionary if available."""
    if not exists(DICT_FILE):
        print("No existing dictionary found. Starting fresh.")
        return defaultdict(lambda: defaultdict(int))
    print(f"Loading existing dictionary from {DICT_FILE}...")
    try:
        with open(DICT_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
        # Convert keys back to tuples using the '|||' separator
        return {tuple(k.split("|||")): v for k, v in data.items()}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {DICT_FILE}. Starting fresh.")
        return defaultdict(lambda: defaultdict(int))
    except Exception as e:
        print(f"Error loading dictionary: {e}. Starting fresh.")
        return defaultdict(lambda: defaultdict(int))

def merge_dicts(base_dict, new_dict):
    """Merges new dictionary counts into the base dictionary."""
    print("Merging new n-grams into the dictionary...")
    merged_count = 0
    # Ensure base_dict uses defaultdict structure if loaded empty or from file
    if not isinstance(base_dict, defaultdict):
         temp_dict = defaultdict(lambda: defaultdict(int), base_dict)
         base_dict = temp_dict

    for context, next_words in new_dict.items():
        for word, count in next_words.items():
            base_dict[context][word] = base_dict[context].get(word, 0) + count
            merged_count += count # Count occurrences
    print(f"Merged {merged_count} n-gram occurrences.")
    return base_dict

def save_dict(data):
    """Saves the n-gram dictionary as a JSON file using ||| separator."""
    print(f"Saving updated dictionary to {DICT_FILE}...")
    try:
        # Convert tuple keys to strings for JSON
        saveable_data = {"|||".join(k): v for k, v in data.items()}
        with open(DICT_FILE, 'w', encoding='utf-8') as file:
            json.dump(saveable_data, file, ensure_ascii=False, indent=2)
        print("Dictionary saved successfully.")
    except Exception as e:
        print(f"Error saving dictionary: {e}")

# --- Main Execution ---
if __name__ == "__main__":
    print(f"📖 Reading text from: {file_name}")
    text = read_text(file_name)

    if text: # Only proceed if text was successfully read
        print("🧹 Preprocessing text...")
        words = preprocess(text)
        print(f"Total tokens found: {len(words)}")

        if words:
            print(f"🔢 Building n-gram dictionary...")
            new_dict = build_ngram_dict(words)
            print(f"Built n-grams for {len(new_dict)} unique contexts.")

            print("📂 Loading existing dictionary (if any)...")
            existing_dict_loaded = load_existing_dict()
            existing_dict = defaultdict(lambda: defaultdict(int), existing_dict_loaded)

            updated_dict = merge_dicts(existing_dict, new_dict)

            save_dict(updated_dict)
            print(f"✅ Dictionary processing complete. Saved in '{DICT_FILE}'")
        else:
             print("❌ No words found after preprocessing. Dictionary not updated.")
    else:
        print("❌ No text read from file. Dictionary not updated.")