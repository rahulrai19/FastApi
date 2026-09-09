from fastapi import FastAPI

import time
import asyncio

app = FastAPI()

@app.get("/")
async def home():
    await asyncio.sleep(10)
    return{
        "message":"Async API"
    }
# def task():
#     time.sleep(3)
#     return "Done"

async def task():
    await asyncio.sleep(3)
    return "done"