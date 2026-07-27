from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()

todos = []

class Todo(BaseModel):
    id:int
    title:str
    completed:bool



@app.post("/todos")
def create_todo(todo:Todo):
    todos.append(todo)
    return{
          "message":"Todo added",
          "data":todo
    }

@app.get("/todos")
def get_todos():
    return todos

@app.get("/todos/{todo_id}")
def get_todo(todo_id:int):
    for todo in todos:
        if todo.id == todo_id:
         return todo
    return{"error"}

@app.put("/todos/{todo_id}")
def updated_todo(todo_id:int,updated_todo:Todo):
    for index,todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = updated_todo
            return {
                "message":"Data Updated",
                "data": updated_todo
            }
    return {"error":"Todo not Found"}


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int):
    for index,todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return {"message":"Data Deleted"}
    return {"error":"todo not found"}
         