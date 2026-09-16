# FastAPI --- Complete Notes

> A structured set of FastAPI notes covering the topics in the learning
> roadmap, with practical code, request/response flow diagrams,
> installation commands, testing examples, and **2--3 interview
> questions per section**.
>
> The installation commands supplied in the original notes are preserved
> as written.

------------------------------------------------------------------------

## Table of Contents

1.  [Introduction & Setup](#1-introduction--setup)
2.  [Basic Routes](#2-basic-routes)
3.  [Pydantic Basics, Path, Query &
    Body](#3-pydantic-basics-path-query--body)
4.  [Response Models](#4-response-models)
5.  [Status Codes & Responses](#5-status-codes--responses)
6.  [Exception Handling](#6-exception-handling)
7.  [Dependency Injection](#7-dependency-injection)
8.  [Middleware](#8-middleware)
9.  [Database Integration --- SQLite](#9-database-integration--sqlite)
10. [Database Integration ---
    SQLAlchemy](#10-database-integration--sqlalchemy)
11. [CRUD --- Create](#11-crud--create)
12. [CRUD --- Read](#12-crud--read)
13. [CRUD --- Update](#13-crud--update)
14. [CRUD --- Delete](#14-crud--delete)
15. [Async Programming](#15-async-programming)
16. [Authentication Basics --- JWT](#16-authentication-basics--jwt)
17. [OAuth2 + JWT](#17-oauth2--jwt)
18. [File Upload & Static Files](#18-file-upload--static-files)
19. [CORS Handling](#19-cors-handling)
20. [Environment Variables](#20-environment-variables)
21. [Testing APIs](#21-testing-apis)
22. [Third-Party API Integration](#22-third-party-api-integration)
23. [Web Crawling using FastAPI](#23-web-crawling-using-fastapi)
24. [Pagination](#24-pagination)
25. [Caching](#25-caching)
26. [Rate Limiting](#26-rate-limiting)
27. [Project Deployment](#27-project-deployment)
28. [Blog API Project](#28-blog-api-project)
29. [FastAPI Interview Cheat Sheet](#29-fastapi-interview-cheat-sheet)

------------------------------------------------------------------------

<details>
<summary><strong>1. Introduction & Setup</strong></summary>


## What is FastAPI?

FastAPI is a modern Python framework for building APIs.

It is designed around:

-   Python type hints
-   Automatic validation
-   Automatic OpenAPI documentation
-   Async programming support
-   Dependency injection
-   Pydantic models
-   Starlette for the web layer

### Why FastAPI?

-   High performance
-   Automatic Swagger UI and ReDoc
-   Automatic request validation
-   Automatic response serialization
-   Strong editor/autocomplete support
-   Less boilerplate
-   Easy integration with databases and external services
-   Supports both `def` and `async def`

### Core architecture

``` text
                    FastAPI Application
                           |
          +----------------+----------------+
          |                                 |
      Starlette                         Pydantic
   Web / HTTP layer                 Data validation
          |                                 |
          +----------------+----------------+
                           |
                    Python Type Hints
                           |
                Automatic OpenAPI Docs
```

## Installation

``` bash
python --version

pip install fastapi

pip install "uvicorn[standard]"
```

## Virtual Environment

``` bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

## Basic Application

``` python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello broo"}
```

## Run the Server

``` bash
uvicorn main:app --reload

python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Meaning of the command

``` text
main:app
  |
  +-- main -> main.py
  |
  +-- app  -> FastAPI instance

--reload
  |
  +-- Restart server automatically when code changes
      Use during development, not production.
```

## Automatic Documentation

After starting the server:

| URL | Purpose |
|---|---|
| `http://127.0.0.1:8000/docs` | Swagger UI |
| `http://127.0.0.1:8000/redoc` | ReDoc |
| `http://127.0.0.1:8000/openapi.json` | OpenAPI schema |

### Request flow

``` text
Client
  |
  v
HTTP Request
  |
  v
Uvicorn
  |
  v
FastAPI
  |
  +--> Routing
  +--> Validation
  +--> Dependencies
  +--> Endpoint
  |
  v
Response
  |
  v
Client
```

## Interview Questions

### Q1. Why is FastAPI considered fast?

**Answer:** FastAPI uses Starlette for the web layer and supports
asynchronous request handling through Python's `asyncio` ecosystem. Its
performance is especially useful for I/O-bound APIs.

### Q2. What is the role of Pydantic in FastAPI?

**Answer:** Pydantic is used for data validation, parsing and
serialization based on Python type hints and models.

### Q3. What is Uvicorn?

**Answer:** Uvicorn is an ASGI server commonly used to run FastAPI
applications.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>2. Basic Routes</strong></summary>


A route maps an HTTP method and URL path to a Python function.

``` python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/about")
def about():
    return {"message": "About API"}

@app.post("/users")
def create_user():
    return {"message": "User created"}
```

## HTTP Methods

| Method | Typical purpose       |
|--------|-----------------------|
| GET    | Read data             |
| POST   | Create data           |
| PUT    | Replace/update data   |
| PATCH  | Partially update data |
| DELETE | Delete data           |

## Path Operation Decorator

``` python
@app.get("/users")
```

This tells FastAPI:

-   HTTP method = `GET`
-   Path = `/users`
-   Function below it handles the request

## Dynamic Routes

``` python
@app.get("/users/{user_id}")
def get_user(user_id):
    return {"user_id": user_id}
```

`{user_id}` is a path parameter.

### With validation

``` python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

A request such as:

``` text
GET /users/10
```

works.

A request such as:

``` text
GET /users/abc
```

fails validation.

### Why type hints matter

``` text
URL value
   |
   v
"user_id": "10"
   |
   v
FastAPI validation
   |
   v
int -> 10
   |
   v
Python function
```

## Query Parameters

``` python
@app.get("/users")
def get_users(limit: int = 10):
    return {"limit": limit}
```

Request:

``` text
GET /users?limit=20
```

Optional query parameter:

``` python
@app.get("/search")
def search(q: str | None = None):
    return {"q": q}
```

## Path + Query Parameters

``` python
@app.get("/users/{user_id}")
def get_user(user_id: int, details: bool = False):
    return {
        "user_id": user_id,
        "details": details
    }
```

Request:

``` text
GET /users/5?details=true
```

------------------------------------------------------------------------


</details>

<details>
<summary><strong>3. Pydantic Basics, Path, Query & Body</strong></summary>


## Request Data Sources

FastAPI determines where data comes from based on the parameter
declaration.

  | Declaration | Source |
  |---|---|
  | Parameter matching `{}` in path | Path |
  | Simple parameter not in path | Query |
  | Pydantic `BaseModel` | JSON body |
  | `Body()` | Request body |
  | `Header()` | HTTP header |
  | `Cookie()` | Cookie |

## Pydantic Model

``` python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str | None = None
```

## POST Request Body

``` python
@app.post("/create-user")
def create_user(user: User):
    return {
        "message": "User Created",
        "data": user
    }
```

Example JSON:

``` json
{
  "name": "Rahul",
  "age": 22,
  "email": "rahul@example.com"
}
```

## Why not just use `dict`?

This works:

``` python
@app.post("/create-user")
def create_user(user: dict):
    return user
```

But a Pydantic model is preferable because it gives:

-   Validation
-   Schema generation
-   Better editor support
-   Documentation
-   Structured nested data
-   Consistent serialization

## Optional Fields

``` python
class User(BaseModel):
    name: str
    age: int
    email: str | None = None
```

`email` is optional because it has a default value of `None`.

## Validation Example

``` python
class Product(BaseModel):
    name: str
    price: float
    quantity: int
```

Invalid input:

``` json
{
  "name": "Keyboard",
  "price": "wrong",
  "quantity": 2
}
```

FastAPI/Pydantic validates the request before the endpoint logic
proceeds.

## Query Validation

``` python
from fastapi import Query

@app.get("/items")
def get_items(
    q: str | None = Query(default=None, max_length=50)
):
    return {"q": q}
```

## Path + Query + Body

``` python
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

@app.put("/items/{item_id}")
def update_item(
    item_id: int,
    q: str | None = Query(default=None, max_length=50),
    item: Item | None = None
):
    result = {"item_id": item_id}

    if q:
        result["q"] = q

    if item:
        result["item"] = item

    return result
```

Example:

``` text
PUT /items/5?q=discount
```

``` json
{
  "name": "Keyboard",
  "price": 999.0
}
```

### Input flow

``` text
                    Request
                       |
        +--------------+--------------+
        |              |              |
        v              v              v
      Path           Query           Body
   item_id=5     q=discount       JSON object
        |              |              |
        +--------------+--------------+
                       |
                       v
                  Validation
                       |
                       v
                 Endpoint logic
```

## Interview Questions

### Q1. How does FastAPI decide whether a parameter is path, query or body?

**Answer:** A parameter matching a `{}` placeholder is a path parameter.
Simple parameters generally become query parameters, while Pydantic
models are interpreted as request bodies.

### Q2. Why are Pydantic models preferred over `dict`?

**Answer:** They provide validation, generated schemas, documentation,
type safety and structured serialization.

### Q3. What happens when validation fails?

**Answer:** FastAPI rejects the request before normal endpoint logic
runs and returns a validation error response describing the invalid
field.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>4. Response Models</strong></summary>


A request model describes incoming data. A response model describes the
public structure of outgoing data.

## Example

``` python
from pydantic import BaseModel

class UserIn(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    username: str
    email: str

@app.post("/signup", response_model=UserOut)
def signup(user: UserIn):
    # Save user to database here.
    return user
```

Even though `user` contains `password`, the response model does not
expose it.

## Response Model Flow

``` text
Database / Internal Object
          |
          v
   Endpoint returns data
          |
          v
   response_model
          |
          +--> validate
          +--> serialize
          +--> filter fields
          |
          v
      API Response
```

## List Response

``` python
@app.get("/items", response_model=list[Item])
def list_items():
    return items
```

## Excluding Unset Fields

``` python
@app.get(
    "/user/{id}",
    response_model=UserOut,
    response_model_exclude_unset=True
)
def get_user(id: int):
    ...
```

This can be useful when you want fields that were explicitly set to
appear while default/unset fields are omitted.

## Key Benefits

-   Protect sensitive fields
-   Validate outgoing data
-   Keep a stable API contract
-   Generate accurate OpenAPI documentation
-   Separate internal and external representations

## Interview Questions

### Q1. Why should request and response models often be different?

**Answer:** Incoming data may contain fields such as passwords that the
API needs to accept but must never expose in its response.

### Q2. What does `response_model` do?

**Answer:** It defines, validates and serializes the expected response
shape and can filter fields that should not be exposed.

### Q3. What is `response_model_exclude_unset=True`?

**Answer:** It excludes fields that were not explicitly set, which is
useful when working with partial/default-based response data.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>5. Status Codes & Responses</strong></summary>


HTTP status codes communicate the result of an API operation.

## Common Status Codes

  | Code | Meaning | Typical API use |
  | --- | --- | --- |
  | 200 | OK | Successful read/update |
  | 201 | Created | Resource successfully created |
  | 204 | No Content | Successful operation with no response body |
  | 400 | Bad Request | Invalid client request |
  | 401 | Unauthorized | Missing/invalid authentication |
  | 403 | Forbidden | Authenticated but not permitted |
  | 404 | Not Found | Resource does not exist |
  | 422 | Validation error | Input validation failed |
  | 500 | Internal Server Error | Unexpected server-side failure |

## Setting Status Code

``` python
from fastapi import FastAPI, status

app = FastAPI()

@app.post(
    "/create-user",
    status_code=status.HTTP_201_CREATED
)
def create_user(user: User):
    return user
```

## Custom JSON Response

``` python
from fastapi.responses import JSONResponse

@app.get("/custom")
def custom_response():
    return JSONResponse(
        status_code=201,
        content={"message": "Custom response"}
    )
```

## Other Response Classes

FastAPI provides response classes such as:

-   `JSONResponse`
-   `HTMLResponse`
-   `PlainTextResponse`
-   `RedirectResponse`
-   `StreamingResponse`
-   `FileResponse`

## HTTPException

``` python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return items_db[item_id]
```

## Interview Questions

### Q1. When should you return `201 Created`?

**Answer:** When a request successfully creates a new resource.

### Q2. What is the difference between `401` and `403`?

**Answer:** `401` means authentication is missing or invalid. `403`
means the requester is authenticated but does not have permission to
perform the operation.

### Q3. Why is returning an error dictionary with status `200` usually wrong?

**Answer:** HTTP clients and infrastructure rely on status codes to
understand success/failure. An error payload with `200` incorrectly
communicates that the operation succeeded.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>6. Exception Handling</strong></summary>


## HTTPException

``` python
from fastapi import HTTPException

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in db:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return db[user_id]
```

`raise` immediately stops normal execution.

## Custom Exceptions

``` python
class ItemNotFoundError(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id
```

Register a handler:

``` python
from fastapi.responses import JSONResponse

@app.exception_handler(ItemNotFoundError)
def item_not_found_handler(request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "message": f"Item {exc.item_id} not found"
        }
    )
```

Use it:

``` python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items_db:
        raise ItemNotFoundError(item_id)

    return items_db[item_id]
```

## Global Exception Handler

``` python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
def global_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error",
            "detail": str(exc)
        }
    )
```

### Production consideration

Do not expose internal exception details to clients in production.

Prefer:

``` text
Client -> Generic safe error
Server -> Detailed logs
```

## Exception Flow

``` text
Endpoint
   |
   v
Exception raised
   |
   +--------------------+
   |                    |
Known exception      Unknown exception
   |                    |
   v                    v
Specific handler     Global handler
   |                    |
   +---------+----------+
             |
             v
       HTTP Response
```

## Interview Questions

### Q1. Why use custom exception handlers?

**Answer:** They centralize error formatting and keep business logic
from repeatedly constructing HTTP responses.

### Q2. What is the purpose of a global exception handler?

**Answer:** It provides a consistent fallback response for unexpected
exceptions and helps prevent accidental leakage of internal details.

### Q3. What is the difference between `raise HTTPException(...)` and `return {"error": ...}`?

**Answer:** `HTTPException` changes the HTTP error status and stops
execution. Returning a dictionary normally produces a successful
response unless another status is explicitly set.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>7. Dependency Injection</strong></summary>


## What is `Depends()`?

`Depends()` allows FastAPI to call reusable dependency functions and
inject their results into endpoint functions.

``` python
from fastapi import Depends

def get_query_param(q: str | None = None):
    return q

@app.get("/search")
def search(q: str = Depends(get_query_param)):
    return {"q": q}
```

## Database Session Dependency

``` python
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

Use it:

``` python
@app.get("/items")
def list_items(db=Depends(get_db)):
    return db.query(Item).all()
```

## Why `yield`?

``` text
Dependency starts
      |
      v
Create resource
      |
      v
    yield
      |
      v
Endpoint executes
      |
      v
Cleanup code
      |
      v
Close resource
```

This pattern is useful for:

-   Database sessions
-   Temporary resources
-   Connections
-   Cleanup operations

## Authentication Dependency

``` python
from fastapi import Depends, Header, HTTPException

def verify_token(authorization: str = Header(...)):
    if authorization != "Bearer secrettoken":
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return authorization

@app.get("/protected")
def protected_route(
    token: str = Depends(verify_token)
):
    return {"message": "Access granted"}
```

## Nested Dependencies

Dependencies can depend on other dependencies.

``` text
Route
  |
  v
get_current_user
  |
  v
verify_token
  |
  v
decode token
  |
  v
find user
```

## Router-Level Dependencies

For a group of protected endpoints, dependencies can be attached at
router level rather than repeated on every endpoint.

``` python
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(verify_token)]
)
```

## Interview Questions

### Q1. What problem does `Depends()` solve?

**Answer:** It removes repeated logic and makes reusable services such
as authentication, database sessions and common parameters injectable
into endpoints.

### Q2. Why use `yield` in a database dependency?

**Answer:** Code before `yield` performs setup, while code after `yield`
performs cleanup after the request lifecycle.

### Q3. Can dependencies depend on other dependencies?

**Answer:** Yes. FastAPI resolves dependency chains automatically.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>8. Middleware</strong></summary>


## What is Middleware?

Middleware is logic that wraps the request/response lifecycle.

Typical uses:

-   Logging
-   Request timing
-   CORS
-   Authentication-related processing
-   Headers
-   Compression
-   Metrics

## Process-Time Middleware

``` python
import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(
    request: Request,
    call_next
):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response
```

## Logging Middleware

``` python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(
        f"Incoming request: "
        f"{request.method} {request.url}"
    )

    response = await call_next(request)

    print(
        f"Response status: "
        f"{response.status_code}"
    )

    return response
```

## Request/Response Flow

``` text
Client Request
      |
      v
+----------------------+
| Middleware - Before  |
| logging/auth/timing  |
+----------------------+
      |
      v
 call_next(request)
      |
      v
+----------------------+
| Route Handler        |
+----------------------+
      |
      v
+----------------------+
| Middleware - After   |
| headers/timing/logs  |
+----------------------+
      |
      v
Client Response
```

## CORS Middleware

``` python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

For production, replace `["*"]` with the specific frontend origins that
should be allowed.

## Middleware vs Dependency

| Middleware | Dependency |
| --- | --- |
| Wraps requests globally | Usually attached to selected routes |
| Runs before/after route processing | Injects reusable values/logic |
| Good for logging/CORS/timing | Good for auth/DB/user context |
| Does not primarily inject endpoint arguments | Designed for dependency injection |

## Interview Questions

### Q1. What is the difference between middleware and a dependency?

**Answer:** Middleware wraps the request/response lifecycle and can run
globally. Dependencies are resolved by FastAPI and are normally attached
to specific routes or routers.

### Q2. What does `call_next(request)` do?

**Answer:** It passes the request to the next middleware or the route
handler and returns the resulting response.

### Q3. Give one use case for middleware.

**Answer:** Request logging and timing for every request are common
middleware use cases.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>9. Database Integration --- SQLite</strong></summary>


## What is SQLite?

SQLite is a lightweight, file-based relational database.

It is useful for:

-   Learning
-   Prototypes
-   Small applications
-   Local development
-   Testing

A SQLite database can exist as a local file such as:

``` text
app.db
```

## SQLite vs Server Databases

| SQLite | PostgreSQL/MySQL |
| --- | --- |
| File-based | Server/database service |
| Very easy setup | More infrastructure |
| Good for small/local apps | Better for larger multi-user workloads |
| Minimal configuration | More production features |

## Basic SQLite with Python

``` python
import sqlite3

connection = sqlite3.connect("app.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
)
""")

connection.commit()
connection.close()
```

## FastAPI + SQLite Concept

``` text
FastAPI
   |
   v
Endpoint
   |
   v
Database access layer
   |
   v
SQLite
   |
   v
app.db
```

SQLite is the database. SQLAlchemy is a separate database toolkit/ORM
discussed next.

## Interview Questions

### Q1. Is SQLite the same as SQLAlchemy?

**Answer:** No. SQLite is a database engine. SQLAlchemy is a Python SQL
toolkit and ORM that can work with SQLite and other databases.

### Q2. When is SQLite useful?

**Answer:** It is useful for learning, prototypes, local applications
and lightweight deployments where a full database server is unnecessary.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>10. Database Integration --- SQLAlchemy</strong></summary>


## What is SQLAlchemy?

SQLAlchemy is a Python SQL toolkit and ORM.

It provides:

-   Database connections
-   SQL expression tools
-   ORM mapping
-   Sessions
-   Transactions
-   Model-to-table mapping

## Install SQLAlchemy

``` bash
pip install sqlalchemy
```

## Database Setup

``` python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
```

## Why `check_same_thread=False`?

For this SQLite/FastAPI setup, it allows the SQLite connection to be
used across the request handling pattern commonly used by FastAPI.

## Create a Model

``` python
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
```

## Create Tables

``` python
Base.metadata.create_all(bind=engine)
```

## Database Session Dependency

``` python
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

## Connect FastAPI

``` python
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

## SQLAlchemy Architecture

``` text
FastAPI Endpoint
       |
       v
Depends(get_db)
       |
       v
SQLAlchemy Session
       |
       v
SQLAlchemy ORM
       |
       v
Database Driver
       |
       v
SQLite / PostgreSQL / MySQL
```

## Interview Questions

### Q1. What is an ORM?

**Answer:** An Object Relational Mapper lets application code work with
database records through objects/models rather than manually writing SQL
for every operation.

### Q2. What is the purpose of `Session` in SQLAlchemy?

**Answer:** A session manages database interaction, including queries
and transaction-related operations for ORM objects.

### Q3. Why should a FastAPI database session be closed?

**Answer:** Sessions hold database resources. Closing them after the
request prevents resource leaks and keeps database connections
manageable.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>11. CRUD --- Create</strong></summary>


## What is CREATE?

CREATE adds a new record to the database.

Typical HTTP mapping:

``` text
POST /users
```

## Example

``` python
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

@app.post("/users")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    db_user = User(
        name=user.name,
        email=user.email
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
```

## CREATE Flow

``` text
Client
  |
  | POST /users
  | JSON body
  v
FastAPI
  |
  v
Pydantic validation
  |
  v
Endpoint
  |
  v
SQLAlchemy Model
  |
  v
db.add()
  |
  v
db.commit()
  |
  v
Database
  |
  v
db.refresh()
  |
  v
Response
```

## Why `db.refresh()`?

After insertion, the database may generate values such as an
auto-incremented ID. `refresh()` loads the current database state back
into the ORM object.

## Testing

Swagger UI:

``` text
http://127.0.0.1:8000/docs
```

Test:

``` json
{
  "name": "Rahul",
  "email": "rahul@example.com"
}
```

Then verify the record in the database.

## Interview Questions

### Q1. What is the difference between `db.add()` and `db.commit()`?

**Answer:** `db.add()` places the ORM object into the session.
`db.commit()` commits the pending transaction to the database.

### Q2. Why call `db.refresh()` after creating a record?

**Answer:** It refreshes the ORM object with values generated or changed
by the database, such as an automatically generated ID.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>12. CRUD --- Read</strong></summary>


READ retrieves data.

Common endpoints:

``` text
GET /users
GET /users/{user_id}
```

## Read All

``` python
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

## Read by ID

``` python
from fastapi import HTTPException

@app.get("/users/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user
```

## READ Flow

``` text
Client
  |
  v
GET /users/10
  |
  v
Path parameter validation
  |
  v
SQLAlchemy query
  |
  v
Database
  |
  +--> Record found -> Response
  |
  +--> Not found -> 404
```

## Interview Questions

### Q1. Why should a missing database record usually return `404`?

**Answer:** The requested resource does not exist, so `404 Not Found`
communicates that condition correctly.

### Q2. What is the difference between `.all()` and `.first()`?

**Answer:** `.all()` returns all matching records, while `.first()`
returns the first matching record or `None` if there is no match.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>13. CRUD --- Update</strong></summary>


## What is UPDATE?

Update modifies an existing database record.

Typical endpoint:

``` text
PUT /users/{user_id}
```

or for partial updates:

``` text
PATCH /users/{user_id}
```

## Update Example

``` python
@app.put("/users/{user_id}")
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.name = user_data.name
    user.email = user_data.email

    db.commit()
    db.refresh(user)

    return user
```

## Update Flow

``` text
Client
  |
  | PUT /users/10
  v
Validate path + body
  |
  v
Find record
  |
  +---- Not found ----> 404
  |
  v
Modify ORM object
  |
  v
db.commit()
  |
  v
db.refresh()
  |
  v
Response
```

## PUT vs PATCH

-   `PUT` is commonly used for replacing/updating the representation as
    a whole.
-   `PATCH` is used for partial modifications.

## Interview Questions

### Q1. What is the difference between PUT and PATCH?

**Answer:** PUT generally represents a complete replacement/update,
while PATCH represents a partial update.

### Q2. Why check whether the record exists before updating?

**Answer:** Without the check, the endpoint cannot correctly distinguish
a successful update from an attempt to update a non-existent resource.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>14. CRUD --- Delete</strong></summary>


## What is DELETE?

DELETE removes a resource.

Typical endpoint:

``` text
DELETE /users/{user_id}
```

## Example

``` python
@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {"message": "User deleted"}
```

For a successful operation with no response body, `204 No Content` can
be used.

## DELETE Flow

``` text
Client
  |
  v
DELETE /users/10
  |
  v
Find user
  |
  +---- Not found ----> 404
  |
  v
db.delete()
  |
  v
db.commit()
  |
  v
Response
```

## Testing

Use Swagger UI:

``` text
http://127.0.0.1:8000/docs
```

Then verify that the record no longer exists.

## Interview Questions

### Q1. Which status code can represent a successful DELETE with no response body?

**Answer:** `204 No Content`.

### Q2. Why call `db.commit()` after `db.delete()`?

**Answer:** `db.delete()` marks the ORM object for deletion in the
session. The transaction must be committed for the change to persist in
the database.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>15. Async Programming</strong></summary>


## What is `async` / `await`?

Python asynchronous programming allows an application to perform other
work while waiting for I/O operations.

``` python
import asyncio

async def fetch_data():
    await asyncio.sleep(2)
    return "data"
```

## FastAPI Endpoint

``` python
@app.get("/data")
async def get_data():
    data = await fetch_data()
    return {"data": data}
```

## Why Async Matters

Many APIs spend time waiting for:

-   Database I/O
-   HTTP requests
-   File I/O
-   Network services

With asynchronous code, the event loop can handle other work while an
awaited operation is waiting.

## Sync vs Async

``` text
Synchronous

Request A -> wait -> result
Request B -------------> waits


Asynchronous

Request A -> wait
              |
Request B -> work -> result
              |
Request A -> result
```

## Important rule

`async def` does not automatically make blocking code non-blocking.

Bad example:

``` python
@app.get("/bad")
async def bad():
    time.sleep(5)  # blocking
    return {"message": "done"}
```

Use an async-compatible operation when appropriate:

``` python
await asyncio.sleep(5)
```

## When to use `def`

Normal synchronous functions are still valid.

Use synchronous code when the libraries/operations you call are
synchronous and there is no benefit from converting them to async
without changing the underlying I/O behavior.

## Interview Questions

### Q1. Why does async help API performance?

**Answer:** It can improve concurrency for I/O-bound workloads by
allowing the event loop to handle other tasks while an awaited operation
is waiting.

### Q2. Does `async def` make blocking code asynchronous?

**Answer:** No. Blocking operations can still block the event loop.

### Q3. What does `await` do?

**Answer:** It suspends the current coroutine while an awaitable
operation is in progress, allowing the event loop to execute other work.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>16. Authentication Basics --- JWT</strong></summary>


## Authentication vs Authorization

**Authentication:**

> Who are you?

**Authorization:**

> Are you allowed to perform this action?

## JWT

JWT stands for JSON Web Token.

A JWT commonly contains:

``` text
Header.Payload.Signature
```

Conceptually:

``` text
Client
  |
  | Login credentials
  v
Login API
  |
  v
Validate user
  |
  v
Generate JWT
  |
  v
Client stores token
  |
  | Authorization: Bearer <token>
  v
Protected API
  |
  v
Validate JWT
  |
  v
Allow / Reject
```

## Installation

``` bash
pip install python-jose
```

## Basic Token Creation

``` python
from jose import jwt

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

token = jwt.encode(
    {"sub": "user123"},
    SECRET_KEY,
    algorithm=ALGORITHM
)
```

## Token Validation

``` python
payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM]
)

user_id = payload.get("sub")
```

## Important JWT Concepts

-   Header: algorithm/type information
-   Payload: claims
-   Signature: verifies token integrity
-   `sub`: commonly used for subject/user identity
-   Expiration: should be used for access tokens
-   Secret key/private key: must be protected

JWT payloads are encoded, **not inherently encrypted**. Do not place
sensitive secrets/passwords in the payload.

## Login API Concept

``` python
@app.post("/login")
def login(username: str, password: str):
    # 1. Find user
    # 2. Verify password
    # 3. Create JWT
    # 4. Return token

    return {
        "access_token": token,
        "token_type": "bearer"
    }
```

## Interview Questions

### Q1. What is a JWT?

**Answer:** JWT is a signed token format commonly used to carry claims
between a client and server and to represent authenticated sessions.

### Q2. Is JWT encrypted?

**Answer:** Not by default. Standard JWTs are encoded and signed. Their
payload should not be treated as secret data.

### Q3. What is the purpose of the signature?

**Answer:** It allows the server to verify that the token was created by
a trusted party and has not been modified.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>17. OAuth2 + JWT</strong></summary>


## What is OAuth2?

OAuth2 is an authorization framework. FastAPI provides utilities for
implementing OAuth2-style authentication flows.

JWT can be used as the access-token format.

These are related but not identical concepts:

``` text
OAuth2 -> authorization framework
JWT    -> token format
```

## Installation

``` bash
pip install "python-jose" "passlib[bcrypt]" "python-multipart"
```

## Password Hashing

Never store plain-text passwords.

Concept:

``` text
Plain Password
      |
      v
Password Hashing
      |
      v
Stored Hash
```

During login:

``` text
Entered password
      |
      v
Verify against stored hash
      |
      +---- Invalid -> Reject
      |
      v
Generate access token
```

## OAuth2 Password Flow Components

``` text
POST /token
   |
   v
Username + Password
   |
   v
Authenticate
   |
   v
Access Token
   |
   v
Authorization: Bearer <token>
   |
   v
Protected endpoint
```

## OAuth2PasswordBearer

``` python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token"
)
```

## Protected Route Concept

``` python
from fastapi import Depends

@app.get("/protected")
def protected(
    token: str = Depends(oauth2_scheme)
):
    return {"token": token}
```

In a real application, the token should then be decoded, validated,
checked for expiration and mapped to a user.

## Password Hashing Example

``` python
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

hashed_password = pwd_context.hash("mypassword")

is_valid = pwd_context.verify(
    "mypassword",
    hashed_password
)
```

## Security Checklist

-   Hash passwords
-   Never return passwords
-   Keep JWT secrets outside source code
-   Use expiration times
-   Validate token signature
-   Validate token claims
-   Use HTTPS in production
-   Use appropriate token storage on the client
-   Return correct `401`/`403` responses

## Interview Questions

### Q1. What is the difference between OAuth2 and JWT?

**Answer:** OAuth2 is an authorization framework, while JWT is a token
format. OAuth2 systems can use JWTs as access tokens, but they are not
the same thing.

### Q2. Why hash passwords?

**Answer:** Password hashing ensures that the original password is not
stored directly. A secure password hash can be verified without storing
the plain-text password.

### Q3. What does `OAuth2PasswordBearer` do?

**Answer:** It extracts a bearer token from the Authorization header and
integrates that token dependency into FastAPI's dependency system.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>18. File Upload & Static Files</strong></summary>


## Upload Files

FastAPI can receive uploaded files using `UploadFile`.

``` python
from fastapi import File, UploadFile

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents)
    }
```

## Multiple Files

``` python
@app.post("/upload-multiple")
async def upload_multiple(
    files: list[UploadFile] = File(...)
):
    return {
        "files": [file.filename for file in files]
    }
```

## Why `UploadFile`?

`UploadFile` is generally preferable for uploaded files because it
provides file metadata and a file-like interface.

## Saving a File

``` python
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    destination = UPLOAD_DIR / file.filename

    with destination.open("wb") as buffer:
        while chunk := await file.read(1024 * 1024):
            buffer.write(chunk)

    return {"filename": file.filename}
```

For production, validate filenames, file size and file type, and
consider object storage rather than blindly writing user-controlled
paths to disk.

## Static Files

``` python
from fastapi.staticfiles import StaticFiles

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)
```

A file:

``` text
static/image.jpg
```

can be exposed under:

``` text
/static/image.jpg
```

## Interview Questions

### Q1. What is `UploadFile` used for?

**Answer:** It represents an uploaded file and provides metadata plus a
file-like interface for reading the upload.

### Q2. Why should uploaded filenames be handled carefully?

**Answer:** User-controlled filenames can cause path traversal or unsafe
file handling if they are directly used to construct filesystem paths.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>19. CORS Handling</strong></summary>


## What is CORS?

CORS stands for Cross-Origin Resource Sharing.

A browser restricts frontend JavaScript from freely accessing resources
on another origin unless the server allows the cross-origin request.

An origin is based on:

``` text
scheme + host + port
```

For example:

``` text
Frontend: http://localhost:3000
Backend:  http://localhost:8000
```

These are different origins because their ports differ.

## Enable CORS

``` python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Production Configuration

Instead of:

``` python
allow_origins=["*"]
```

prefer:

``` python
allow_origins=[
    "http://localhost:3000",
    "https://your-frontend.example"
]
```

## React + FastAPI

``` text
React Frontend
   |
   | fetch / axios
   v
Browser CORS policy
   |
   v
FastAPI
   |
   v
Response + CORS headers
   |
   v
Browser
```

## Preflight

Some cross-origin requests cause the browser to send an `OPTIONS`
preflight request before the actual request.

The server uses CORS headers to tell the browser whether the request is
allowed.

## Interview Questions

### Q1. What problem does CORS solve?

**Answer:** It controls whether browser-based frontend code from one
origin can access resources from another origin.

### Q2. Why is `allow_origins=["*"]` not always appropriate?

**Answer:** It allows requests from any origin and is often too
permissive for production applications.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>20. Environment Variables</strong></summary>


## What are Environment Variables?

Environment variables store configuration outside the source code.

Examples:

``` text
DATABASE_URL
SECRET_KEY
API_KEY
DEBUG
```

## Why use them?

Do not hard-code secrets:

``` python
SECRET_KEY = "super-secret-value"
```

Instead:

``` python
import os

SECRET_KEY = os.getenv("SECRET_KEY")
```

## Installation

``` bash
pip install python-dotenv
```

## `.env`

``` env
SECRET_KEY=my-secret-key
DATABASE_URL=sqlite:///./app.db
DEBUG=True
```

## Loading `.env`

``` python
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
```

## Configuration Flow

``` text
.env / Environment
       |
       v
Configuration loader
       |
       v
Application settings
       |
       +--> Database
       +--> JWT
       +--> External APIs
       +--> Debug/config
```

## Important Practices

-   Add `.env` to `.gitignore`
-   Do not commit secrets
-   Use platform/environment secrets in production
-   Validate required configuration
-   Separate development and production configuration

## Interview Questions

### Q1. Why should secrets be stored in environment variables?

**Answer:** They can be separated from source code and changed per
environment without modifying the application code.

### Q2. Why should `.env` usually be in `.gitignore`?

**Answer:** `.env` files often contain credentials, API keys or secrets
that should not be committed to a public or shared repository.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>21. Testing APIs</strong></summary>


## Why Testing?

API tests help verify:

-   Endpoint behavior
-   Validation
-   Status codes
-   Authentication
-   Error handling
-   CRUD operations
-   Regression safety

## Installation

``` bash
pip install pytest

pip install httpx2
```

Run tests:

``` bash
pytest
```

## Basic Test

``` python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Hello World"
```

## POST Test

``` python
def test_create_user():
    response = client.post(
        "/users",
        json={
            "name": "Rahul",
            "email": "rahul@example.com"
        }
    )

    assert response.status_code == 201
```

## Validation Test

``` python
def test_invalid_user():
    response = client.post(
        "/users",
        json={
            "name": "Rahul",
            "email": 123
        }
    )

    assert response.status_code == 422
```

## Testing Flow

``` text
pytest
  |
  v
TestClient
  |
  v
FastAPI application
  |
  v
Endpoint
  |
  v
Response
  |
  v
Assertions
```

## What to Test

For an endpoint:

``` text
Happy path
    +
Invalid input
    +
Missing resource
    +
Unauthorized request
    +
Forbidden request
    +
Edge cases
```

## Interview Questions

### Q1. Why test status codes as well as response data?

**Answer:** Status codes are part of the API contract. Correct data with
an incorrect HTTP status can still break clients and integrations.

### Q2. What is `TestClient` used for?

**Answer:** It allows tests to make HTTP-like requests against the
FastAPI application and inspect the resulting responses.

### Q3. What command runs pytest?

**Answer:**

``` bash
pytest
```

------------------------------------------------------------------------


</details>

<details>
<summary><strong>22. Third-Party API Integration</strong></summary>


## What is an External API?

An external API is an API provided by another service.

Examples:

``` text
FastAPI
   |
   | HTTP request
   v
External Service
   |
   v
JSON response
   |
   v
FastAPI
   |
   v
Frontend
```

## Installation

``` bash
pip install requests
```

## Basic Request

``` python
import requests

response = requests.get(
    "https://example.com/api/data"
)

data = response.json()
```

## Check Status

``` python
response = requests.get(
    "https://example.com/api/data",
    timeout=10
)

response.raise_for_status()

data = response.json()
```

## FastAPI Integration

``` python
@app.get("/external-data")
def external_data():
    response = requests.get(
        "https://example.com/api/data",
        timeout=10
    )

    response.raise_for_status()

    return response.json()
```

## Production Consideration

For async endpoints, using synchronous `requests` directly can block the
event loop. For a fully asynchronous design, use an async HTTP client.

Conceptually:

``` text
Client
  |
  v
FastAPI
  |
  v
External API call
  |
  +--> Success -> transform -> response
  |
  +--> Timeout -> handle error
  |
  +--> 4xx/5xx -> handle error
```

## Interview Questions

### Q1. Why should external API calls have a timeout?

**Answer:** Without a timeout, a slow/unresponsive external service can
keep your request waiting indefinitely and consume application
resources.

### Q2. What should happen if an external API fails?

**Answer:** The application should handle the failure explicitly, log
useful information and return an appropriate safe response rather than
exposing raw exceptions.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>23. Web Crawling using FastAPI</strong></summary>


## What is Web Crawling?

Web crawling means fetching web pages and processing their content
programmatically.

FastAPI can expose crawling functionality through an API endpoint.

## Installation

``` bash
pip install beautifulsoup4
```

## Basic HTML Parsing

``` python
import requests
from bs4 import BeautifulSoup

url = "https://example.com"

response = requests.get(
    url,
    timeout=10
)

response.raise_for_status()

soup = BeautifulSoup(
    response.text,
    "html.parser"
)

title = soup.title.get_text(strip=True)

print(title)
```

## Extract Links

``` python
links = []

for link in soup.find_all("a", href=True):
    links.append({
        "text": link.get_text(strip=True),
        "href": link["href"]
    })
```

## FastAPI Integration

``` python
@app.get("/crawl")
def crawl(url: str):
    response = requests.get(
        url,
        timeout=10
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    return {
        "title": (
            soup.title.get_text(strip=True)
            if soup.title
            else None
        )
    }
```

## Crawling Flow

``` text
Client
  |
  | GET /crawl?url=...
  v
FastAPI
  |
  v
HTTP request
  |
  v
HTML page
  |
  v
BeautifulSoup
  |
  +--> Parse title
  +--> Parse links
  +--> Extract content
  |
  v
JSON response
```

## Important Considerations

-   Respect website terms and robots policies
-   Use timeouts
-   Avoid aggressive request rates
-   Validate URLs
-   Handle redirects/errors
-   Avoid SSRF vulnerabilities when users can supply arbitrary URLs
-   Do not crawl private/internal network addresses

## Interview Questions

### Q1. What is BeautifulSoup used for?

**Answer:** It parses HTML/XML and makes it easier to navigate and
extract elements from a document.

### Q2. What is a major security risk when exposing arbitrary URL crawling through an API?

**Answer:** Server-Side Request Forgery (SSRF). An attacker may attempt
to make the server access internal services or private network
resources.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>24. Pagination in FastAPI</strong></summary>


## What is Pagination?

Pagination divides a large result set into smaller pages.

Instead of:

``` text
GET /users
-> 100,000 records
```

use:

``` text
GET /users?page=1&limit=20
```

## Basic Logic

``` python
@app.get("/users")
def get_users(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit

    users = (
        db.query(User)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return users
```

## Formula

``` text
offset = (page - 1) × limit
```

Example:

``` text
page 1, limit 10
offset = 0

page 2, limit 10
offset = 10

page 3, limit 10
offset = 20
```

## Better API Response

``` json
{
  "page": 2,
  "limit": 10,
  "total": 125,
  "items": []
}
```

## Pagination Flow

``` text
Request
  |
  +--> page
  +--> limit
  |
  v
Calculate offset
  |
  v
Database query
  |
  v
Return page + metadata
```

## Interview Questions

### Q1. What is pagination?

**Answer:** Pagination splits a large dataset into smaller result sets
so clients retrieve only a manageable portion at a time.

### Q2. How is offset calculated?

**Answer:**

``` text
offset = (page - 1) * limit
```

### Q3. Why is pagination important?

**Answer:** It reduces response size, database work per request and
client-side processing, making APIs more scalable.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>25. Caching in FastAPI</strong></summary>


## What is Caching?

Caching stores frequently used results so future requests can be served
faster without repeating expensive work.

``` text
Request
  |
  v
Cache?
  |
  +---- Hit ----> Return cached data
  |
  +---- Miss
          |
          v
      Expensive work
          |
          v
       Store cache
          |
          v
       Response
```

## TTL

TTL means **Time-To-Live**.

It determines how long cached data remains valid.

Example:

``` text
TTL = 60 seconds

t=0     cache created
t=30    cache valid
t=60    cache expires
t=61    fetch fresh data
```

## Simple In-Memory Concept

``` python
import time

cache = {}

def get_cached(key):
    item = cache.get(key)

    if not item:
        return None

    value, expires_at = item

    if time.time() >= expires_at:
        del cache[key]
        return None

    return value

def set_cached(key, value, ttl=60):
    cache[key] = (
        value,
        time.time() + ttl
    )
```

## FastAPI Integration

``` python
@app.get("/expensive")
def expensive_operation():
    cached = get_cached("expensive")

    if cached is not None:
        return cached

    result = perform_expensive_operation()

    set_cached(
        "expensive",
        result,
        ttl=60
    )

    return result
```

## Production Caching

In-memory caching is simple but has limitations with multiple
application instances.

A distributed cache such as Redis can be used when shared cache state is
required.

## Interview Questions

### Q1. What is a cache hit?

**Answer:** A cache hit occurs when requested data already exists in the
cache and can be returned without performing the original expensive
operation.

### Q2. What is TTL?

**Answer:** Time-To-Live defines how long cached data remains valid
before it expires.

### Q3. Why can process-local memory caching be problematic in production?

**Answer:** Multiple application instances have separate memory, so a
value cached in one instance may not exist in another.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>26. Rate Limiting in FastAPI</strong></summary>


## What is Rate Limiting?

Rate limiting restricts how many requests a client can make during a
period.

Example:

``` text
100 requests / minute / client
```

Purpose:

-   Prevent abuse
-   Protect resources
-   Reduce accidental overload
-   Control API usage

## Installation

``` bash
pip install slowapi
```

## Basic Concept

``` python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address
)
```

A route can then be limited using the library's limiter
decorator/configuration.

Conceptually:

``` text
Client
  |
  v
Rate Limiter
  |
  +---- Under limit ----> FastAPI endpoint
  |
  +---- Over limit -----> 429 Too Many Requests
```

## Status Code

``` text
429 Too Many Requests
```

is commonly used when the rate limit is exceeded.

## Testing

A basic test strategy:

``` text
Send request repeatedly
        |
        v
Within limit?
        |
   +----+----+
   |         |
  Yes        No
   |         |
   v         v
  2xx       429
```

## Production Consideration

If the application runs across multiple instances, rate-limit state may
need to be shared through an external store rather than local process
memory.

## Interview Questions

### Q1. Why use rate limiting?

**Answer:** To protect an API from excessive or abusive traffic and keep
resources available for legitimate users.

### Q2. Which HTTP status code commonly represents an exceeded rate limit?

**Answer:** `429 Too Many Requests`.

### Q3. Why can local rate limiting be insufficient with multiple servers?

**Answer:** Each server may maintain separate counters, so a client can
exceed the intended global limit across multiple instances.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>27. Project Deployment</strong></summary>


## Deployment Goal

The goal is to make the FastAPI application accessible outside the local
development environment.

Typical flow:

``` text
Local Development
       |
       v
Git Repository
       |
       v
Deployment Platform
       |
       v
Build / Install dependencies
       |
       v
Start FastAPI application
       |
       v
Public API
```

## Create a Simple Project

Typical structure:

``` text
project/
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

Larger projects may use:

``` text
app/
├── main.py
├── routers/
├── models/
├── schemas/
├── services/
├── database/
└── core/
```

## Requirements File

``` bash
pip freeze > requirements.txt
```

This records installed Python packages.

## Git

``` bash
git init
git add .
git commit -m "Initial commit"
```

Then push to GitHub.

## Production Start Command

A typical ASGI deployment uses Uvicorn:

``` bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The exact command may depend on the hosting platform.

## Environment Variables

Configure production values through the deployment platform rather than
committing secrets.

Typical variables:

``` text
DATABASE_URL
SECRET_KEY
API_KEY
```

## Production Checklist

-   Do not use `--reload`
-   Configure environment variables
-   Use HTTPS
-   Configure CORS correctly
-   Use a production database where required
-   Add logging
-   Add health checks
-   Validate file uploads
-   Add authentication/authorization
-   Add rate limiting where needed
-   Test production endpoints
-   Do not expose secrets

## Deployment Testing

``` text
Deploy
  |
  v
Health check
  |
  v
Swagger / OpenAPI
  |
  v
CRUD test
  |
  v
Authentication test
  |
  v
Database test
  |
  v
Production monitoring
```

## Interview Questions

### Q1. Why should `--reload` not be used as a production setting?

**Answer:** It is intended for development and automatically restarts
the process when code changes, adding unnecessary behavior and overhead
in production.

### Q2. Why is `requirements.txt` important?

**Answer:** It provides a reproducible list of Python dependencies
needed to install the application's environment.

### Q3. What is the purpose of `0.0.0.0` in a deployment command?

**Answer:** It tells the server to listen on all network interfaces
rather than only the local loopback interface.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>28. Blog API Project</strong></summary>


The Blog API brings together the major concepts from the roadmap.

## Project Requirements

### Backend

-   FastAPI
-   PostgreSQL
-   SQLAlchemy
-   Pydantic
-   JWT authentication
-   Password hashing
-   Pagination
-   Search
-   Error handling
-   Environment variables
-   Testing

## Core Features

``` text
                 Blog API
                    |
      +-------------+-------------+
      |             |             |
   Auth           Posts         Users
      |             |             |
    JWT        CRUD APIs      User data
      |             |
      +------+------+
             |
        Pagination
             |
          Search
             |
        PostgreSQL
```

## Suggested API Design

### Authentication

``` text
POST /auth/register
POST /auth/login
GET  /auth/me
```

### Posts

``` text
POST   /posts
GET    /posts
GET    /posts/{post_id}
PUT    /posts/{post_id}
PATCH  /posts/{post_id}
DELETE /posts/{post_id}
```

### Search

``` text
GET /posts?search=fastapi
```

### Pagination

``` text
GET /posts?page=1&limit=10
```

## Blog Post Model

Example conceptual fields:

``` text
Post
├── id
├── title
├── content
├── author_id
├── created_at
└── updated_at
```

## User Model

``` text
User
├── id
├── username
├── email
├── password_hash
└── created_at
```

## Authentication Flow

``` text
Register
   |
   v
Hash password
   |
   v
Store user
   |
   v
Login
   |
   v
Verify password
   |
   v
Create JWT
   |
   v
Client
   |
   | Bearer token
   v
Protected endpoint
   |
   v
Decode + validate JWT
   |
   v
Current user
```

## Create Post Flow

``` text
Authenticated Client
        |
        | POST /posts
        v
JWT validation
        |
        v
Current user
        |
        v
Validate request body
        |
        v
Create SQLAlchemy Post
        |
        v
PostgreSQL
        |
        v
Response model
        |
        v
JSON response
```

## Search + Pagination

A production-style request could look conceptually like:

``` text
GET /posts?search=fastapi&page=2&limit=10
```

Processing:

``` text
Search term
    |
    v
Build database filter
    |
    v
Count matching records
    |
    v
Apply offset + limit
    |
    v
Return items + metadata
```

## Suggested Response

``` json
{
  "page": 2,
  "limit": 10,
  "total": 37,
  "items": [
    {
      "id": 11,
      "title": "Learning FastAPI",
      "content": "..."
    }
  ]
}
```

## Project Structure

``` text
blog-api/
│
├── app/
│   ├── main.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   └── post.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   └── post.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── users.py
│   │   └── posts.py
│   │
│   ├── services/
│   │   └── auth.py
│   │
│   └── core/
│       └── config.py
│
├── tests/
│   ├── test_auth.py
│   └── test_posts.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Development Sequence

``` text
1. PostgreSQL setup
        |
2. Database connection
        |
3. User model
        |
4. Post model
        |
5. Schemas
        |
6. Register API
        |
7. Login + JWT
        |
8. Protected routes
        |
9. Post CRUD
        |
10. Pagination
        |
11. Search
        |
12. Error handling
        |
13. Tests
        |
14. GitHub
        |
15. Deployment
```

## Blog API Interview Questions

### Q1. How would you prevent one user from editing another user's post?

**Answer:** Authenticate the request, identify the current user from the
validated JWT, load the post, and verify that
`post.author_id == current_user.id` before allowing the update.

### Q2. Where should password hashes be stored?

**Answer:** In the user table as secure password hashes. Plain-text
passwords should never be stored.

### Q3. How would you design pagination and search together?

**Answer:** Apply the search/filter condition first, calculate the total
matching records, then apply offset/limit to the filtered query and
return pagination metadata with the results.

------------------------------------------------------------------------


</details>

<details>
<summary><strong>29. FastAPI Interview Cheat Sheet</strong></summary>


## FastAPI Fundamentals

``` text
FastAPI
├── Starlette -> HTTP/web layer
├── Pydantic  -> validation/data models
├── OpenAPI   -> API schema
└── Uvicorn   -> ASGI server commonly used to run app
```

## Request Sources

``` text
Path      -> /users/{user_id}
Query     -> /users?limit=10
Body      -> Pydantic model / Body()
Header    -> Header()
Cookie    -> Cookie()
```

## CRUD Mapping

| Operation | HTTP method | Example |
|-----------|-------------|---------|
| Create    | POST        | `/posts` |
| Read      | GET         | `/posts` |
| Read one  | GET         | `/posts/10` |
| Update    | PUT/PATCH   | `/posts/10` |
| Delete    | DELETE      | `/posts/10` |

## Important Status Codes

``` text
200 -> Success
201 -> Created
204 -> No Content
400 -> Bad Request
401 -> Unauthorized
403 -> Forbidden
404 -> Not Found
422 -> Validation Error
429 -> Too Many Requests
500 -> Server Error
```

## Security Concepts

``` text
Authentication
      |
      v
Who are you?

Authorization
      |
      v
Are you allowed?

Password
      |
      v
Hash it

JWT
      |
      v
Signed access token

Secret
      |
      v
Environment variable
```

## Performance Concepts

``` text
Async
  -> Better I/O concurrency

Caching
  -> Avoid repeated expensive work

Pagination
  -> Avoid huge responses

Rate Limiting
  -> Protect resources
```

## Middleware vs Dependency

``` text
Middleware
    |
    +--> Global request/response behavior
    +--> Logging
    +--> CORS
    +--> Timing

Dependency
    |
    +--> Reusable route logic
    +--> Authentication
    +--> Database session
    +--> Current user
```

## Complete FastAPI Request Lifecycle

``` text
                    CLIENT
                      |
                      v
                HTTP Request
                      |
                      v
                 Middleware
                      |
                      v
                  Routing
                      |
                      v
             Parameter Validation
                      |
          +-----------+-----------+
          |                       |
       Path/Query             Body Model
          |                       |
          +-----------+-----------+
                      |
                      v
                 Dependencies
                      |
                      v
                Endpoint Logic
                      |
          +-----------+-----------+
          |                       |
       Database             External API
          |                       |
          +-----------+-----------+
                      |
                      v
                Response Model
                      |
                      v
                 HTTP Response
                      |
                      v
                 Middleware
                      |
                      v
                    CLIENT
```

------------------------------------------------------------------------

# Final Revision Checklist

Before considering the FastAPI fundamentals complete, you should be able
to explain and implement:

-   [ ] FastAPI application creation
-   [ ] Uvicorn
-   [ ] Basic routes
-   [ ] Path parameters
-   [ ] Query parameters
-   [ ] Request bodies
-   [ ] Pydantic models
-   [ ] Validation
-   [ ] Response models
-   [ ] HTTP status codes
-   [ ] `HTTPException`
-   [ ] Custom exception handlers
-   [ ] Dependency injection
-   [ ] `yield` dependencies
-   [ ] Middleware
-   [ ] SQLite
-   [ ] SQLAlchemy
-   [ ] Database sessions
-   [ ] CREATE
-   [ ] READ
-   [ ] UPDATE
-   [ ] DELETE
-   [ ] Async/await
-   [ ] JWT
-   [ ] OAuth2
-   [ ] Password hashing
-   [ ] Protected routes
-   [ ] File uploads
-   [ ] Static files
-   [ ] CORS
-   [ ] Environment variables
-   [ ] Pytest
-   [ ] API testing
-   [ ] Third-party APIs
-   [ ] Web crawling
-   [ ] Pagination
-   [ ] Caching
-   [ ] Rate limiting
-   [ ] Deployment
-   [ ] PostgreSQL + FastAPI
-   [ ] Blog API architecture

------------------------------------------------------------------------

# Quick Commands Reference

## FastAPI Setup

``` bash
python --version

pip install fastapi

pip install "uvicorn[standard]"
```

## Virtual Environment

``` bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

## Run

``` bash
uvicorn main:app --reload

python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## JWT

``` bash
pip install python-jose
```

## OAuth2 + Password Hashing

``` bash
pip install "python-jose" "passlib[bcrypt]" "python-multipart"
```

## Environment Variables

``` bash
pip install python-dotenv
```

## Testing

``` bash
pip install pytest

pip install httpx2

pytest
```

## Web Crawling

``` bash
pip install beautifulsoup4
```

## Rate Limiting

``` bash
pip install slowapi
```

## Deployment Dependencies

``` bash
pip freeze > requirements.txt
```

------------------------------------------------------------------------

# End

These notes follow the FastAPI topic progression from fundamentals
through database CRUD, authentication, integrations, performance,
deployment and the final Blog API project.

</details>
