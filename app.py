from flask import Flask, request, jsonify
from textblob import TextBlob
import nltk
import os
# nltk_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nltk_data')
# os.makedirs(nltk_data_dir, exist_ok=True)
# nltk.data.path.append(nltk_data_dir)
# nltk.download('punkt', download_dir=nltk_data_dir)
import string

# Download required NLTK data
nltk.download('punkt_tab', quiet=True)
nltk.download('punkt', quiet=True)

# try:
#     nltk.data.find('tokenizers/punkt')
# except LookupError:
#     nltk.download('punkt')

app = Flask(__name__)

def preprocess_word(word):
    return word.strip(string.punctuation)

def get_words(text):
    return [preprocess_word(word) for word in text.split() if preprocess_word(word)]

def syllable_count(word):
    vowels = "aeiouy"
    word = word.lower()
    count = 0
    if len(word) == 0:
        return 0
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count += 1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        count += 1
    if count == 0:
        count = 1
    return count

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '').strip()
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    sentences = nltk.sent_tokenize(text)
    sentence_count = len(sentences)
    if sentence_count == 0:
        return jsonify({'error': 'No sentences found'}), 400
    
    words = get_words(text)
    word_count = len(words)
    if word_count == 0:
        return jsonify({'error': 'No words found'}), 400
    
    unique_words = set(word.lower() for word in words)
    unique_word_count = len(unique_words)
    
    total_chars = sum(len(word) for word in words)
    avg_word_length = round(total_chars / word_count, 2)
    
    total_syllables = sum(syllable_count(word) for word in words)
    avg_syllables_per_word = total_syllables / word_count
    
    words_per_sentence = word_count / sentence_count
    
    flesch_reading_ease = 206.835 - 1.015 * words_per_sentence - 84.6 * avg_syllables_per_word
    flesch_reading_ease = round(flesch_reading_ease, 2)
    
    flesch_kincaid_grade = 0.39 * words_per_sentence + 11.8 * avg_syllables_per_word - 15.59
    flesch_kincaid_grade = round(flesch_kincaid_grade, 2)
    
    corrected_text = str(TextBlob(text).correct())
    
    return jsonify({
        'statistics': {
            'sentence_count': sentence_count,
            'word_count': word_count,
            'unique_word_count': unique_word_count,
            'average_word_length': avg_word_length
        },
        'readability': {
            'flesch_reading_ease': flesch_reading_ease,
            'flesch_kincaid_grade': flesch_kincaid_grade
        },
        'grammar_correction': corrected_text
    })

@app.route('/', methods=['GET'])
def home():
    return "Text Analysis API is running. Use /analyze endpoint with POST requests."

if __name__ == '__main__':
    app.run(debug=True)