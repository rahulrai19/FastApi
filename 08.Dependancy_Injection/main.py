from fastapi import FastAPI,Depends,Header,HTTPException
from pydantic import BaseModel

app = FastAPI()

# Dependency Injection

# def common_logic():
#     return {
#         "message":"common logic executed"
#     }

# @app.get("/home")
# def home(data = Depends(common_logic)):
#     return data 

# Reusable Logic

# def get_current_user():
#     return {
#         "user":"Guest"
#     }

# @app.get("/profile")
# def profile(user = Depends(get_current_user)):
#     return user

# @app.get("/dashboard")
# def dashboard(user = Depends(get_current_user)):
#     return user

# Auth Example

def verify_token(token:str=Header(None)):
    if token!= "mysecrettoken":
        raise HTTPException(
            status_code=401,
            detail = "Unauthorized"
        )
    return {
        "user":"Authorized User"
    }

@app.get("/secure-data")
def secure_data(user = Depends(verify_token)):
    return {
      "message":"secure data Accessed",
      "user":user
    }

