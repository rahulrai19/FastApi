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

app.mount("/files",StaticFiles(directory=UPLOAD_DIR),name="files")


# step 3:
