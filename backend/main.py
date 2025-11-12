from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import close_mongo_connection, connect_to_mongo
from routes.auth_routes import router as auth_router
from routes.diet_routes import router as diet_router
from routes.chatbot_routes import router as chatbot_router
from routes.user_routes import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_to_mongo()
    yield
    close_mongo_connection()


app = FastAPI(title="Smart AI Diet Planner", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://ai-diet-planner-rho.vercel.app",
        "https://aidietplanner.vercel.app",
        "https://ai-diet-planner-git-main-gajusharmas-projects.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(diet_router, prefix="/diet", tags=["Diet"])
app.include_router(chatbot_router, prefix="/chat", tags=["Chatbot"])


@app.get("/", tags=["Health"])
async def read_root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Smart AI Diet Planner API"}
