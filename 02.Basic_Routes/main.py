from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

@app.get("/")
def home():
    return {"Message":"Hello broo"}

#about
@app.get("/about")
def about():
    return {"Message":"About section"}

# @app.get("/users")
# def users():
#     return {
#         "Users":{"Mohit","Rohit"}
#     }

# Dynamic routes and validation

# @app.get("/users/{user_id}")
# def get_user(user_id:str):
#     return {"user_id":user_id}

# Query Params 
# /users?name=mohit&age=22
# /products?name=mohit&age=22


# optional parameters(str="None")

@app.get("/users")
def get_users(name:str="None"):
    return {"name":name}

@app.get("/products")
def get_users(limit:int = 10):
    return {"limit":limit}

# default and optional parameter both 
@app.get("/items")
def get_users(name:str=None,price:int=0):
    return {
            "name":name,
            "price":price
            }

## Pydantic Validation

class User(BaseModel):
    name:str
    age:int

## Request body and post request

@app.post("/create-user")
def create_user(user:User): # we can use User:dict
    return{
       "message":"User Created",
       "data":user
    }

# @app.post()
# def create_user():
#     return{

#     }



