import logging
import time
import traceback
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database import close_mongo_connection, connect_to_mongo
from routes.auth_routes import router as auth_router
from routes.diet_routes import router as diet_router
from routes.chatbot_routes import router as chatbot_router
from routes.user_routes import router as user_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up AI Diet Planner API...")
    connect_to_mongo()
    yield
    logger.info("Shutting down AI Diet Planner API...")
    close_mongo_connection()


app = FastAPI(
    title="Smart AI Diet Planner", 
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)


# Custom middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Request: {request.method} {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} in {process_time:.2f}s")
    
    return response


# Enhanced exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    logger.error(f"Request URL: {request.url}")
    logger.error(f"Request method: {request.method}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url.path)
        },
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true"
        }
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Log the exception traceback for debugging in Railway logs
    logger.error("=== UNHANDLED EXCEPTION ===")
    logger.error(f"Request: {request.method} {request.url}")
    logger.error(f"Exception Type: {type(exc).__name__}")
    logger.error(f"Exception Message: {str(exc)}")
    logger.error("Traceback:")
    logger.error(traceback.format_exc())
    logger.error("===========================")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "Internal server error occurred",
            "details": str(exc) if app.debug else "Contact support if issue persists",
            "status_code": 500,
            "path": str(request.url.path)
        },
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true"
        }
    )


# Enhanced CORS configuration for Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000", 
        "http://127.0.0.1:5173",
        "https://aidietplanner.vercel.app",
        "https://aidietplanner-gajusharms-projects.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Accept",
        "Accept-Language", 
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
    ],
    expose_headers=["*"],
    max_age=86400  # 24 hours
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(diet_router, prefix="/diet", tags=["Diet"])
app.include_router(chatbot_router, prefix="/chat", tags=["Chatbot"])


@app.get("/", tags=["Health"])
async def read_root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Smart AI Diet Planner API"}
