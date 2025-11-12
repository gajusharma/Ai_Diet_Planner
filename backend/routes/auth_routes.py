import logging
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, status, Response
from motor.motor_asyncio import AsyncIOMotorCollection

from database import get_database
from models.user_model import PyObjectId, UserCreate, UserInDB, UserLogin
from utils.jwt_handler import create_access_token
from utils.security import hash_password, verify_password
from utils.settings import get_settings

router = APIRouter()
logger = logging.getLogger(__name__)


def _get_user_collection() -> AsyncIOMotorCollection:
    return get_database()["users"]


@router.post("/register")
async def register_user(payload: UserCreate, response: Response):
    try:
        logger.info(f"Registration attempt for email: {payload.email}")
        users_collection = _get_user_collection()
        
        existing = await users_collection.find_one({"email": payload.email})
        if existing:
            logger.warning(f"Registration failed - email already exists: {payload.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Email already registered"
            )

        user_data = payload.model_dump()
        user_data["password"] = hash_password(user_data["password"])
        now = datetime.now(tz=timezone.utc)
        user_data["createdAt"] = now
        user_data["updatedAt"] = now

        result = await users_collection.insert_one(user_data)
        new_user = await users_collection.find_one({"_id": result.inserted_id})
        user = UserInDB(**new_user)

        token = create_access_token({"sub": str(user.id), "email": user.email})
        
        logger.info(f"User registered successfully: {payload.email}")
        
        # Set CORS headers explicitly
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        
        return {
            "success": True,
            "access_token": token,
            "token_type": "bearer",
            "user": user.model_dump(by_alias=True, exclude={"password"}),
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error for {payload.email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed due to server error"
        )


@router.post("/login")
async def login_user(payload: UserLogin, response: Response):
    try:
        logger.info(f"Login attempt for email: {payload.email}")
        users_collection = _get_user_collection()
        
        user_data = await users_collection.find_one({"email": payload.email})
        if not user_data:
            logger.warning(f"Login failed - user not found: {payload.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid email or password"
            )

        user = UserInDB(**user_data)
        if not verify_password(payload.password, user.password):
            logger.warning(f"Login failed - invalid password: {payload.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid email or password"
            )

        settings = get_settings()
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
        )
        
        logger.info(f"User logged in successfully: {payload.email}")
        
        # Set CORS headers explicitly
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        
        return {
            "success": True,
            "access_token": access_token,
            "token_type": "bearer",
            "user": user.model_dump(by_alias=True, exclude={"password"}),
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error for {payload.email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed due to server error"
        )
