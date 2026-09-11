from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI();

# Allowed Origins(Frontend Url)

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origin = origins,
    allow_credential = True,
    allow_methods = ["*"],
    allow_header = ["*"]
)

@app.get("/")
def home():
    return{
        "message":"Cors test only"
    }