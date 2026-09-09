from fastapi import FastAPI,HTTPException,Depends,status
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime,timedelta,timezone
from passlib.context import CryptContext

app = FastAPI()

# JWT Config
SECRET_KEY = 'my_secret' 
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTE = 30

# password hashing Setup 
pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

#Oauth Setup
oauth2_schema = OAuth2PasswordBearer(tokenUrl = "login")

# Dummy User
fake_user_db = {
    "admin":{
        "username":"admin",
        "hashed_password":pwd_context.hash("1234")
    }
}

# hashing Paswword
def hash_password(password:str):
    return pwd_context.hash(password)

# verify password
def verify_password(plain_password,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)

# create token 
def create_token(data:dict):
     to_encode = data.copy()
     expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTE)
     to_encode.update({
          "exp":expire
     })
     token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

     return token

# Login API(Token Generate)
@app.post("/login")
def login(form_data:OAuth2PasswordRequestForm = Depends()):
    user = fake_user_db.get(form_data.username)
    if not user or not verify_password(form_data.password,user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Invalid credentials"
        )

    access_token = create_token({"sub":form_data.username})

    return{
        "access_token":access_token,
        "token_type":"bearer"
    }

# verify token

def verify_token(token:str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return username
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )    

# proctected Route
@app.get("/protected")
def protected_route(username:str = Depends(verify_token)):
    return{
       "message":f"hello {username},you havr access to username and protected route",
       "User":username
    }