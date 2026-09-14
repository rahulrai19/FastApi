from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import time

app = FastAPI()

# Cache storage
cache_data = []
last_fetch = 0


@app.get("/news")
def get_news(page: int = 1, limit: int = 5):
    global cache_data, last_fetch

    start_time = time.time()

    if time.time() - last_fetch > 60:
        print("Fetching fresh data...")

        url = "https://indianexpress.com/"
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        cache_data = [
            item.get_text(strip=True)
            for item in soup.find_all(["h1", "h2", "h3"])
            if item.get_text(strip=True)
        ]

        last_fetch = time.time()

    else:
        print("Using cached data...")

    start = (page - 1) * limit
    end = start + limit
    time_taken = time.time() - start_time

    return {
        "page": page,
        "limit": limit,
        "headings": cache_data[start:end],
        "time_taken": f"{time_taken:.2f} seconds"
    }