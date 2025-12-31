from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from rate_limiter import TokenBucket
from fastapi.responses import JSONResponse

app = FastAPI()

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, bucket: TokenBucket):
        super().__init__(app)
        self.bucket = bucket

    async def dispatch(self, request: Request, call_next):
        if self.bucket.handle():
            return await call_next(request)
        
        return JSONResponse(
            status_code=429, 
            content={"detail": "Rate Limit Exceeded"}
        )

# Initialize bucket: 1 token per 1 second
bucket = TokenBucket(tokens=2, time_unit=1)

app.add_middleware(RateLimiterMiddleware, bucket=bucket)

@app.get("/")
async def read_root():
    return {"message": "Dummy Request"}