from flask import Flask
from flask import request

from junction import text_sentiment


app = Flask(__name__)

@app.route('/')
def index():
    text = request.args['text']
    return text_sentiment.analyze_text(text)
