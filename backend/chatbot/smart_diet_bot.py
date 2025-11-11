import asyncio
import logging
import re
from collections import Counter
from typing import Any, Dict, Optional

from motor.motor_asyncio import AsyncIOMotorCollection
import requests

from utils.settings import get_settings

_LOGGER = logging.getLogger(__name__)
_GEMINI_API_ROOT = "https://generativelanguage.googleapis.com/v1"


def _tokenize(text: str) -> Counter:
    words = re.findall(r"[\w']+", text.lower())
    return Counter(words)


async def handle_chat_message(message: str, foods_collection: AsyncIOMotorCollection) -> Dict[str, str]:
    # Always try Gemini first for a more natural, comprehensive response
    gemini_response = await _gemini_reply(message, foods_collection)
    if gemini_response:
        return {"reply": gemini_response}

    # Fallback to token-based responses if Gemini is unavailable
    tokens = _tokenize(message)
    token_set = set(tokens)

    if "calories" in token_set and "in" in token_set:
        return {"reply": await _calorie_lookup(message, foods_collection)}

    if "high" in token_set and ({"protein", "proteins"} & token_set):
        return {"reply": await _high_protein_suggestions(foods_collection)}

    if "weight" in token_set and "gain" in token_set:
        return {"reply": await _goal_suggestions(foods_collection, high_calorie=True)}

    if "weight" in token_set and "loss" in token_set:
        return {"reply": await _goal_suggestions(foods_collection, high_calorie=False)}

    return {"reply": _default_tip()}


async def _calorie_lookup(message: str, foods_collection: AsyncIOMotorCollection) -> str:
    food_name = message.lower().split("in", 1)[-1].strip(" ?!.")
    food_doc = await foods_collection.find_one({"food": {"$regex": food_name, "$options": "i"}})
    if food_doc:
        return f"{food_doc['food']} has approximately {food_doc['calories']} calories per serving."
    return "I couldn't find that item, but focusing on whole foods is always a good idea!"


async def _high_protein_suggestions(foods_collection: AsyncIOMotorCollection) -> str:
    cursor = foods_collection.find({"protein": {"$gte": 20}}).sort("protein", -1).limit(3)
    foods = [doc async for doc in cursor]
    if foods:
        suggestions = ", ".join(item["food"] for item in foods)
        return f"High-protein options you might enjoy: {suggestions}."
    return "I did not find high-protein items, try adding legumes, tofu, or dairy products."


async def _goal_suggestions(foods_collection: AsyncIOMotorCollection, *, high_calorie: bool) -> str:
    comparator = {"$gte": 450} if high_calorie else {"$lte": 350}
    sort_order = -1 if high_calorie else 1
    cursor = foods_collection.find({"calories": comparator}).sort("calories", sort_order).limit(3)
    foods = [doc async for doc in cursor]
    if foods:
        prefix = "For weight gain, consider calorie-dense meals like " if high_calorie else "Weight loss-friendly picks: "
        return prefix + ", ".join(item["food"] for item in foods) + "."
    fallback = (
        "Increase calorie intake with healthy fats, whole grains, and strength training."
        if high_calorie
        else "Focus on lean proteins, veggies, and portion control for weight loss."
    )
    return fallback


def _default_tip() -> str:
    settings = get_settings()
    if settings.gemini_api_key:
        return (
            "I'm here to help with all your nutrition and diet questions! As your personal nutrition consultant, "
            "I can assist with meal planning, recipe suggestions, nutritional information, dietary requirements, "
            "weight management strategies, and much more. Feel free to ask me anything about healthy eating, "
            "specific foods, cooking methods, or personalized diet advice."
        )
    return (
        "Welcome to SmartDiet! I can help you with:\n"
        "• Calorie and nutrition information for specific foods\n"
        "• High protein meal suggestions\n"
        "• Weight loss or weight gain strategies\n"
        "• Meal planning and recipe ideas\n"
        "• Dietary requirements (vegan, keto, paleo, etc.)\n\n"
        "What would you like to know about nutrition today?"
    )


async def _gemini_reply(message: str, foods_collection: AsyncIOMotorCollection) -> Optional[str]:
    settings = get_settings()
    if not settings.gemini_api_key or not settings.gemini_model:
        return None

    # Fetch more food samples for better context
    food_cursor = foods_collection.find(
        {}, {"food": 1, "calories": 1, "protein": 1, "carbs": 1, "fat": 1, "type": 1, "mealType": 1}
    ).limit(50)
    foods = [doc async for doc in food_cursor]
    food_context = _format_food_context(foods)
    prompt = _build_prompt(message, food_context)

    endpoint = f"{_GEMINI_API_ROOT}/models/{settings.gemini_model}:generateContent"
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": prompt,
                    }
                ],
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 1024,
        }
    }

    def _post_request():
        return requests.post(endpoint, params={"key": settings.gemini_api_key}, json=payload, timeout=30)

    try:
        response = await asyncio.to_thread(_post_request)
    except Exception as exc:  # pragma: no cover - network/runtime issues
        _LOGGER.warning("Gemini request failed: %s", exc)
        return None

    if response.status_code != 200:
        _LOGGER.warning("Gemini API returned %s: %s", response.status_code, response.text)
        return None

    try:
        data = response.json()
    except ValueError as exc:
        _LOGGER.warning("Failed to decode Gemini response: %s", exc)
        return None

    parsed = _extract_text_from_gemini(data)
    if parsed:
        return parsed

    _LOGGER.info("Gemini API returned no usable text: %s", data)
    return None


def _build_prompt(message: str, food_context: str) -> str:
    return (
        "You are SmartDiet AI, a professional nutrition and diet consultant with expertise in meal planning, "
        "nutrition science, and healthy eating habits. Your role is to provide comprehensive, accurate, and "
        "personalized dietary guidance.\n\n"
        
        "EXPERTISE AREAS:\n"
        "- Nutrition facts and calorie information\n"
        "- Meal planning and recipe suggestions\n"
        "- Dietary requirements (vegetarian, vegan, keto, paleo, etc.)\n"
        "- Weight management strategies\n"
        "- Macronutrient balance and portion control\n"
        "- Healthy cooking methods and food preparation\n"
        "- Meal timing and eating schedules\n"
        "- Food substitutions and alternatives\n\n"
        
        "COMMUNICATION STYLE:\n"
        "- Professional yet warm and approachable\n"
        "- Evidence-based recommendations\n"
        "- Clear explanations without jargon\n"
        "- Encouraging and motivational\n"
        "- Practical and actionable advice\n\n"
        
        "RESPONSE GUIDELINES:\n"
        "- Provide detailed, thorough answers (150-250 words)\n"
        "- Include specific meal suggestions, recipes, or food recommendations when relevant\n"
        "- Reference nutritional values (calories, protein, carbs, fats) when discussing foods\n"
        "- Offer alternatives and variations to suit different preferences\n"
        "- Give practical tips for implementation\n"
        "- If asked about recipes, provide step-by-step cooking instructions\n"
        "- Always consider health, balance, and sustainability\n\n"
        
        f"AVAILABLE FOOD DATABASE (use when relevant):\n{food_context or 'No specific food data available.'}\n\n"
        
        f"USER QUESTION: {message}\n\n"
        
        "Provide a comprehensive, professional response that fully addresses the user's question. "
        "If discussing specific foods from the database, include their nutritional information. "
        "If suggesting recipes or meal ideas, provide detailed descriptions and preparation tips."
    )


def _format_food_context(foods: list[dict]) -> str:
    if not foods:
        return "No specific food data available."
    
    formatted_items = []
    for item in foods:
        meal_types = ", ".join(item.get("mealType", [])) if item.get("mealType") else "Any"
        diet_type = item.get("type", "balanced")
        formatted_items.append(
            f"{item['food']} - {item.get('calories', 'n/a')} cal "
            f"(Protein: {item.get('protein', 'n/a')}g, Carbs: {item.get('carbs', 'n/a')}g, "
            f"Fat: {item.get('fat', 'n/a')}g) [Meal: {meal_types}, Type: {diet_type}]"
        )
    return "\n".join(formatted_items)


def _extract_text_from_gemini(data: dict[str, Any]) -> Optional[str]:
    candidates = data.get("candidates", []) or []
    for candidate in candidates:
        content = candidate.get("content") or {}
        parts = content.get("parts") or []
        texts = [part.get("text", "").strip() for part in parts if isinstance(part.get("text"), str)]
        combined = " ".join(filter(None, texts))
        if combined:
            return combined

        candidate_text = candidate.get("text")
        if isinstance(candidate_text, str) and candidate_text.strip():
            return candidate_text.strip()

    top_level_text = data.get("text")
    if isinstance(top_level_text, str) and top_level_text.strip():
        return top_level_text.strip()

    return None
