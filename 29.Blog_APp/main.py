from fastapi import FastAPI,Depends,HTTPException,status,Query
from sqlalchemy.orm import Session
from database import engine,SessionLocal
import models,schemas
from auth import create_token,verify_token

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Home Route

@app.get("/")
def home():
    return{
        "message":"App started"
    }

#login api
@app.post("/login")
def login():
    return {
        "access_token":create_token({"user":"admin"}),
        "token_type":"bearer"
    }

# Blog 
@app.post("/blogs",response_model=schemas.BlogResponse)
def create_blog(blog:schemas.BlogCreate,db:Session = Depends(get_db),user = Depends(verify_token)):

    new_blog =models.Blog(
        title = blog.title,
        content = blog.content
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

# Read_all Blog

@app.get("/blogs",response_model=list[schemas.BlogResponse])
def get_blogs(page:int=1,      # pagination
              limit:int = 5,
              search:str= Query(default=""),   #searching
    db:Session = Depends(get_db)):
    query = db.query(models.Blog)
    if search:
        query = query.filter(models.Blog.title.ilike(f"%{search}%"))

    total = query.count()
    start = (page-1)*limit
    blogs = query.offset(start).limit(limit).all()
    return{
        "page":page,
        "limit":limit,
        "total":total,
        "data":blogs
    }

# Read by ID

@app.get("/blogs/{id}",response_model=schemas.BlogResponse)
def get_blog(id:int,db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not Found")
    return blog

# Update Blog API
@app.put("/blogs/{id}",response_model=schemas.BlogResponse)
def update_blog(id:int,blog:schemas.BlogCreate,db:Session = Depends(get_db),user = Depends(verify_token)):
    existing_blog = db.query(models.Blog).filter(models.Blog.id==id).first()

    if not existing_blog:
        raise HTTPException(status_code=404,detail="Blog not Found")
    existing_blog.title = blog.title
    existing_blog.content = blog.content

    db.commit()

    return existing_blog

# Delete
@app.delete("/blogs/{id}")
def delete_blog(id:int,db:Session = Depends(get_db),user=Depends(verify_token)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=404,detail="Blog not found")

    blog.delete()
    db.commit()

    return{
        "message":"Blog Deleted Successfully"
    }