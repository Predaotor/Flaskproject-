from flask import Flask, jsonify
from flask import request, render_template
import json
import re

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/Rankings')
def rankings():
    return render_template("Rankings.html")

@app.route('/News')
def news():
    # Load news data from json file
    with open("news.json", "r", encoding="utf-8") as f:
        news_data = json.load(f)
    
    # Process news data (clean titles, fix image URLs, normalize special characters)
   
    
    return render_template("news.html", news=news_data)

@app.route('/Events')
def events():
    return render_template("events.html")

if __name__ == "__main__":
    app.run(debug=True)
