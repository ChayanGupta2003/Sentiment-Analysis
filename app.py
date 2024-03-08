from flask import Flask, render_template, request
import string
from collections import Counter

app = Flask(__name__)

stop_words = [
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no",
    "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our",
    "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd",
    "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that",
    "that's", "the", "their", "theirs", "them", "themselves", "then", "there",
    "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this",
    "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't",
    "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's",
    "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom",
    "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll",
    "you're", "you've", "your", "yours", "yourself", "yourselves"
]

def analyze_text(text):
    if not text.strip():
        return "neutral"

    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.split()

    final_text = [word for word in text if word not in stop_words]

    emotion_list = []
    with open('emotions.txt', 'r') as file:
        for line in file:
            clear_line = line.replace(',', '').replace("'", '').replace('\n', '').strip()
            w, emotion = clear_line.split(':')
            if w in final_text:
                emotion_list.append(emotion)

    if not emotion_list:
        return "neutral"

    emotion_counts = Counter(emotion_list)
    most_common_emotion = max(emotion_counts, key=emotion_counts.get)

    if len(emotion_counts) == 1:
        return most_common_emotion
    else:
        return most_common_emotion, emotion_counts

@app.route('/')
def index():
    return render_template('templates/index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']
    result = analyze_text(text)
    if isinstance(result, tuple):
        most_common_emotion, emotion_counts = result
        return render_template('templates/result.html', emotion=most_common_emotion, emotion_counts=emotion_counts)
    else:
        return render_template('templates/result.html', emotion=result)

if __name__ == '__main__':
    app.run(debug=True)
