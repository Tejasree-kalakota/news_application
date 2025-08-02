import os
from flask import Flask, render_template
from dotenv import load_dotenv
import requests
from newspaper import Article
from datetime import datetime

load_dotenv()
app = Flask(__name__)
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

@app.route('/')
def index():
    try:
        url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}'
        response = requests.get(url)
        data = response.json()
        articles = []

        for item in data.get("articles", []):
            article_url = item.get("url")
            try:
                article = Article(article_url)
                article.download()
                article.parse()
                article.nlp()

                articles.append({
                    'title': item.get("title", "No Title"),
                    'url': article_url,
                    'content': article.summary[:200] + "...",
                    'source': item['source']['name'],
                    'image': item.get("urlToImage"),
                    'publishedAt': datetime.strptime(item['publishedAt'], "%Y-%m-%dT%H:%M:%SZ").strftime("%b %d, %Y %I:%M %p")
                })

            except Exception as e:
                print(f"⚠️ Skipping article due to parse error: {e}")
                continue

        return render_template('index.html', articles=articles)

    except Exception as e:
        return f"<h1>Something went wrong: {e}</h1>"

if __name__ == '__main__':
    app.run(debug=True)
