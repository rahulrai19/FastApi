## Basic Python code below 

# import requests

# response = requests.get("https://jsonplaceholder.typicode.com/posts")

# data = response.json()
# print(data[:2])


from fastapi import FastAPI,HTTPException,status
import requests

app = FastAPI()

@app.get("/posts")
def get_posts():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    return response.json()

# get single post
@app.get("/posts/{post_id}")
def get_post(post_id:int):
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    response = requests.get(url)
    if response.status_code !=200:
       raise HTTPException(status.HTTP_404_NOT_FOUND)
    return response.json()
