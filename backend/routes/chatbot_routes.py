from fastapi import APIRouter, Depends
from pydantic import BaseModel

from chatbot.smart_diet_bot import handle_chat_message
from database import get_database
from models.user_model import UserInDB
from utils.dependencies import get_current_user

router = APIRouter()


def _get_food_collection():
	return get_database()["foods"]


class ChatRequest(BaseModel):
	message: str


@router.post("")
async def chat_with_bot(
	payload: ChatRequest,
	_: UserInDB = Depends(get_current_user),
):
	foods_collection = _get_food_collection()
	return await handle_chat_message(payload.message, foods_collection)
