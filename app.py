import os
import requests
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    # Get API key from environment variable
    api_key = os.environ.get("NEWS_API_KEY")

    # Check if API key is found
    if not api_key:
        return "API key not found. Please set NEWS_API_KEY in environment variables."

    # Build the URL
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"

    # Make the API request
    try:
        response = requests.get(url)
        data = response.json()

        # DEBUGGING
        print("RESPONSE STATUS:", response.status_code)
        print("RESPONSE JSON:", data)

        # Extract articles or return empty list
        articles = data.get("articles", [])

        return render_template("index.html", articles=articles)

    except Exception as e:
        return f"Something went wrong while fetching news: {e}"

# Run the app locally (optional)
if __name__ == "__main__":
    app.run(debug=True)
