# flaskapi
# Text Analysis API

A Flask-based API that provides advanced text analysis capabilities including readability metrics, grammar correction, and text statistics.

## Features

- **Text Statistics**: Sentence count, word count, unique word count, average word length
- **Readability Metrics**: Flesch Reading Ease score, Flesch-Kincaid Grade Level
- **Grammar Correction**: Automatic correction of common grammatical errors

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Local Installation

1. Clone the repository or download the source code:
   ```
   git clone https://github.com/yourusername/text-analysis-api.git
   cd text-analysis-api
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   
   # On macOS/Linux
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Download NLTK data:
   ```python
   # Create setup_nltk.py with this content
   import nltk
   import ssl
   
   try:
       _create_unverified_https_context = ssl._create_unverified_context
   except AttributeError:
       pass
   else:
       ssl._create_default_https_context = _create_unverified_https_context
       
   nltk.download('punkt')
   print("NLTK punkt tokenizer successfully downloaded!")
   
   # Then run it
   python setup_nltk.py
   ```

5. Run the application locally:
   ```
   python app.py
   ```
   The API will be available at http://127.0.0.1:5000

### Deployment on Render

1. Push your code to a GitHub repository

2. Sign up for a free account on [Render](https://render.com/)

3. Create a new Web Service:
   - Connect to your GitHub repository
   - Select Python environment
   - Set build command: `pip install -r requirements.txt && python -c "import nltk; nltk.download('punkt')"`
   - Set start command: `gunicorn -c gunicorn_config.py app:app`
   - Choose the Free plan for testing

4. Your API will be available at the URL provided by Render

## API Usage

### Analyze Text

**Endpoint**: `/analyze`  
**Method**: POST  
**Content-Type**: application/json

#### Request Body

```json
{
  "text": "Your text to analyze goes here. It can include multiple sentences. This is an example."
}
```

#### Response

```json
{
  "statistics": {
    "sentence_count": 3,
    "word_count": 15,
    "unique_word_count": 14,
    "average_word_length": 4.27
  },
  "readability": {
    "flesch_reading_ease": 82.35,
    "flesch_kincaid_grade": 5.12
  },
  "grammar_correction": "Your text to analyze goes here. It can include multiple sentences. This is an example."
}
```

### Example Usage with cURL

```bash
curl -X POST \
  https://your-app-name.onrender.com/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"The quick brown fox jumps over the lazy dog. This sentence is used to test typing skills because it contains every letter in the English alphabet."}'
```

### Example Usage with Python Requests

```python
import requests
import json

url = "https://your-app-name.onrender.com/analyze"
headers = {"Content-Type": "application/json"}
data = {"text": "The quick brown fox jumps over the lazy dog. This sentence is used to test typing skills because it contains every letter in the English alphabet."}

response = requests.post(url, headers=headers, data=json.dumps(data))
result = response.json()
print(json.dumps(result, indent=2))
```

## Understanding Readability Scores

### Flesch Reading Ease
- **90-100**: Very easy to read, easily understood by an 11-year-old student
- **80-89**: Easy to read
- **70-79**: Fairly easy to read
- **60-69**: Plain English
- **50-59**: Fairly difficult to read
- **30-49**: Difficult to read
- **0-29**: Very difficult to read, best understood by university graduates

### Flesch-Kincaid Grade Level
Indicates the U.S. school grade level needed to understand the text. For example, a score of 8.2 means that the text can be understood by an eighth-grader.

## Troubleshooting

### Common Issues

1. **NLTK Resource Errors**:
   ```
   LookupError: Resource punkt not found.
   ```
   Solution: Run the NLTK setup script mentioned in the setup instructions.

2. **Flask App Not Running**:
   Check if there's already a process using port 5000. Change the port in `app.py` if needed:
   ```python
   if __name__ == '__main__':
       app.run(debug=True, port=5001)  # Change to a different port
   ```

3. **Render Deployment Fails**:
   - Check build logs for errors
   - Verify that all requirements are correctly listed in requirements.txt
   - Ensure the NLTK download command is included in the build command

## License

MIT License - See LICENSE file for details

## Contact

For questions or support, please open an issue on the GitHub repository.
