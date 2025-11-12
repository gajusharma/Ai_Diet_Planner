import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from motor.motor_asyncio import AsyncIOMotorCollection
from typing import Optional

from database import get_database
from models.user_model import PyObjectId, UserInDB
from utils.jwt_handler import JWTException, decode_access_token

# Use HTTPBearer instead of OAuth2PasswordBearer for better CORS compatibility
security = HTTPBearer(auto_error=False)
logger = logging.getLogger(__name__)


def get_user_collection() -> AsyncIOMotorCollection:
    db = get_database()
    return db["users"]


async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> UserInDB:
    # Enhanced authentication with better error messages
    if not credentials:
        logger.warning("No authorization header provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    if not token:
        logger.warning("No token provided in authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing from authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = decode_access_token(token)
        logger.info(f"Token decoded successfully for user: {payload.get('email')}")
    except JWTException as exc:
        logger.error(f"JWT decode error: {exc}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    user_id = payload.get("sub")
    if not user_id:
        logger.error("No user ID found in token payload")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload - missing user ID",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        users_collection = get_user_collection()
        user_data = await users_collection.find_one({"_id": PyObjectId(user_id)})
        if not user_data:
            logger.error(f"User not found in database: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logger.info(f"User authenticated successfully: {user_data.get('email')}")
        return UserInDB(**user_data)
        
    except Exception as e:
        logger.error(f"Database error during user lookup: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication service error"
        )
