import pickle
import nltk
from nltk.corpus import stopwords
import re
from flask import Flask, request, jsonify, render_template
from nltk.tokenize import word_tokenize
app = Flask(__name__)
# Initialize NLTK's stopwords list
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
# Define preprocessing functions
def remove_stopwords_and_punctuations(text):
    tokens = nltk.word_tokenize(text)
    filtered_tokens = [token for token in tokens if token.lower() not in stop_words and token.isalpha()]
    filtered_text = [re.sub(r"(n't|'m|'s|'re|'ll|'ve|'d|\.\.\.|-)", '', token) for token in filtered_tokens if token]
    filtered_text = ' '.join(filtered_text)
    return filtered_text
def remove_numbers(text):
    words = word_tokenize(text)
    pattern = re.compile(r'\d+')
    words = [word for word in words if not pattern.match(word)]
    clean_text = ' '.join(words)
    return clean_text
def preprocess_text(text):
    text = text.lower()
    text = remove_stopwords_and_punctuations(text)
    text = remove_numbers(text)
    return text
# Define the mapping from prediction values to text labels
prediction_mapping = {
    0: 'Negative',
    1: 'Irrelevant',
    2: 'Neutral',
    3: 'Positive'
}
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/predict', methods=['POST'])
def predict():

    with open('vectorizer.pkl', 'rb') as vec_file:
        vectorizer = pickle.load(vec_file)
    with open('svm.pkl', 'rb') as model_file:
        model = pickle.load(model_file)

    if model is None or vectorizer is None:
        return jsonify({'error': 'Model or vectorizer not loaded'}), 500
    data = request.get_json(force=True)  # Force JSON parsing
    text = data.get('Text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    try:
        processed_text = preprocess_text(text)
        transformed_text = vectorizer.transform([processed_text])
        print(f"Transformed text shape: {transformed_text.shape}")
        print(f"Expected feature size: {model.n_features_in_}")
        predictions = model.predict(transformed_text)
        prediction_labels = [prediction_mapping[pred] for pred in predictions]
        return jsonify({'predictions': prediction_labels})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)