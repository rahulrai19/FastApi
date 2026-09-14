from fastapi import FastAPI,Request,status
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

app = FastAPI()

# Limiter Setup 

limitter = Limiter(key_func=get_remote_address)
app.state.limiter = limitter

# Error handle

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request:Request,exc:RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "detail":"Too many request"
        }
    )

# Rate Limiter API 
@app.get("/data")
@limitter.limit("5/minute")
def get_data(request:Request):
    return {
        "message":"Success" 
    }