import os
import requests
from flask import Flask, render_template

app = Flask(__name__)

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/top-headlines?country=in&apiKey=" + NEWS_API_KEY

@app.route("/")
def index():
    articles = []
    try:
        response = requests.get(NEWS_API_URL)
        data = response.json()
        print(data)  # Logs to Render

        if data.get("status") == "ok" and data.get("articles"):
            articles = data["articles"]
    except Exception as e:
        print(f"Error: {e}")

    return render_template("index.html", articles=articles)
