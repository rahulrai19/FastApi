from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base,Session
from sqlalchemy import Column,Integer,String
from fastapi import FastAPI,Depends

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine (
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)

sessionLocal = sessionmaker(bind = engine)

Base = declarative_base()

class Todo(Base):
    __tablename__="todos"

    id=Column(Integer,primary_key=True,index=True)
    title = Column(String)
    completed = Column(String)


# Table Created by this
Base.metadata.create_all(bind=engine)

# Dependency (DB session provide karega)
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/todos")
def create_todo(title:str,db:Session = Depends(get_db)):
    todo = Todo(title = title,completed='False') 
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return{
        "message":"Todo Created",
        "data":todo
    }
