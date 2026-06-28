import time
import uuid
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from statistics import mean

app = FastAPI()

# 1. CORS Policy: Replace with your specific allowed origin
ALLOWED_ORIGIN = "https://your-assigned-origin.com" 

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Middleware for Headers (X-Request-ID and X-Process-Time)
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    return response

@app.options("/stats")
async def options_stats():
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "https://dash-emlbxz.example.com",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, X-Request-ID",
        }
    )


# 3. Stats Endpoint
@app.get("/stats")
async def get_stats(values: str):
    nums = [float(x) for x in values.split(",")]
    return {
        "email": "your-email@iitm.ac.in",
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": mean(nums)
    }

@app.options("/{path:path}")
async def options_handler(path: str):
    # This specifically handles preflight requests
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "https://dash-emlbxz.example.com",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )
