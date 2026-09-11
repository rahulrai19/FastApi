from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()


@app.get("/news")
def get_news(page: int = 1, limit: int = 5):
    url = "https://indianexpress.com/"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    headings = []

    for item in soup.find_all(["h1", "h2", "h3"]):
        heading = item.get_text(strip=True)

        if heading:
            headings.append(heading)

    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "headings": headings[start:end]
    }


@app.get("/home")
def home():
    return {
        "message": "News web crawler is running"
    }