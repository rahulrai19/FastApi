from fastapi import FastAPI,UploadFile,File,HTTPException
from fastapi.staticfiles import StaticFiles
import os
import shutil

app = FastAPI()

# step 1 : Ensure Uploads Folder Exist

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# step 2 : Static File Setup

app.mount("/file",StaticFiles(directory=UPLOAD_DIR),name="files")


# step 3: Upload file api 
@app.post("/upload")
def upload_file(file:UploadFile=File(...)):
    filename = file.filename
    file_path = os.path.join(UPLOAD_DIR,filename)

    if not filename:
        raise HTTPException(status_code=400,detail="File not Selected")
    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)

        return{
            "message":"File Uploaded Successfully",
            "fileName":filename,
            "file_url": f"http://127.0.0.1:8080/file/{filename}"
        }

# step-4 :Get File URL API

@app.get("/file/{filename}")
def get_file(filename:str):
    file_path = os.path.join(UPLOAD_DIR,filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404,detail="File not found")

    return{
        "file_url": f"http://127.0.0.1:8080/file/{filename}"
        }
    

@app.get("/")
def home():
    return{
        "message":"File upload api Runnning"
    }

    

