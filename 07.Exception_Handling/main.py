from fastapi import FastAPI,status,HTTPException,Request 
from fastapi.responses import JSONResponse

from pydantic import BaseModel

app = FastAPI()

# custom Error  class
class UserNotFoundException(Exception):
   def __init__(self,name:str):
      self.name = name
      
## Global handler below
@app.exception_handler(UserNotFoundException)
def user_not_found_handler(request:Request,exc:UserNotFoundException):
   return JSONResponse(
      status_code = 404,
      content = {
         "status":"error",
         "message":f"User {exc.name} not found"
      }
   )

@app.get("/user/{name}")
def get_user(name:str):
   if name!="mohit":
      raise UserNotFoundException(name)
   return{
      "name":name
   }




# @app.get("/users/{user_id}")
# def get_user(user_id:int):
#     if user_id !=1: 
#       raise HTTPException(
#          status_code = 404,
#          detail = "User Not Found"
#       )
#     return{
#        "id":1,
#        "name":"Rahul"
#     }  
