from flask import Flask
from flask import request

from junction import text_sentiment


app = Flask(__name__)

@app.route('/', methods=['POST'])
def analyze_text():
    payload = request.json
    return text_sentiment.analyze_text(payload['text'])
