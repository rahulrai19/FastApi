## FASTAPI
---
![alt text](image.png)
![alt text](image-1.png)
![alt text](image-2.png)
 
 ### Installation
 ```
 python --version

 pip install uvicorn

uvicorn main:app --reload

python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
* work in virtual env 
->  python -m venv venv 
-> venv\Scripts\activate

* we can see the docs(swaggers)
http://127.0.0.1:8000/docs 

 * basic routes

 ```python

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"Message":"Hello broo"}

```

```python
# Dynamic routes 

@app.get("/users/{user_id}")
def get_user(user_id):
    return {"user_id":user_id}
```

```python
![alt text](image-3.png)
# Data Validation auto 

@app.get("/users/{user_id}")
def get_user(user_id:int):
    return {"user_id":user_id}

   
 ```

![alt text](image-4.png)

### Request body and post request

```python
@app.post("/create-user")
def create_user(name:str,age:int):
    return{
        "name":name,
        "age":age
    }
```

## taking the input in dictionary 

```python
@app.post("/create-user")
def create_user(user:dict):
    return{
        "message":"User Created",
        "data":data
    }
```
`27-07-2026`
## I created a CRUD application 
 notes
 ### Interview questions


## Path + Query  + Body Combo
   * Mix all inputs
   * Real-World API Structure
   * IntervieW questions

## Response Models
* Response Validation 
* Hide Sensitive Data
* Output Formating 
* Interview Questions 

## Status Codes & Responses
* HTTP Code Status
* Custom Responses 
* Error Handling Baics
* Interview Questions 

`28-07-2026`

## Exception Handling 
* HTTPException 
* Custom Exceptions
* Global Error Handler
* Interview Questions

## Dependancy Injection 
* What is depends()
* Reusable Logic 
* Auth example intro 
* Interview Questions

## 





