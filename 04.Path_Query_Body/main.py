from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()

# PUT /users/101?notify=true
# path + query + body

users = []

class User(BaseModel):
    name:str
    age:int

@app.post("/users")
def create_user(user:User):
    users.append(user)
    return{
        "message":"User Created",
        "data":user
    }

@app.put("/users/{user_id}")
def updated_user(user_id:int,user:User,notify:bool = False):
    if user_id < len(users):
        users[user_id] = user

        return {
            "message":"User Updated Successfully",
            "notify":notify,
            "data":user
        }
    return {"error":"No user found"}

# path decides what to update and for extra option use query 

