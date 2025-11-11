import asyncio
import random
import logging
import json
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence

import requests

from motor.motor_asyncio import AsyncIOMotorCollection

from models.food_model import FoodInDB, MealType
from models.mealplan_model import DailyMeals, MealEntry
from models.user_model import UserInDB
from utils.settings import get_settings

_LOGGER = logging.getLogger(__name__)
_GEMINI_API_ROOT = "https://generativelanguage.googleapis.com/v1"

ACTIVITY_FACTORS: Dict[str, float] = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9,
}

MEAL_DISTRIBUTION: Dict[MealType, float] = {
    "breakfast": 0.25,
    "lunch": 0.35,
    "dinner": 0.30,
    "snacks": 0.10,
}

MACRO_DISTRIBUTION = {
    "protein": 0.3,
    "carbs": 0.45,
    "fat": 0.25,
}

DAYS_OF_WEEK = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def _calculate_daily_calories(user: UserInDB) -> int:
    weight = user.weight
    height = user.height
    age = user.age
    gender_offset = 5 if user.gender == "male" else -161
    bmr = 10 * weight + 6.25 * height - 5 * age + gender_offset
    activity_factor = ACTIVITY_FACTORS.get(user.activityLevel, 1.55)
    tdee = bmr * activity_factor

    if user.goal == "weight_loss":
        tdee -= 500
    elif user.goal == "weight_gain":
        tdee += 500

    return int(max(tdee, 1200))


async def _load_foods_for_user(
    foods_collection: AsyncIOMotorCollection, diet_type: str
) -> Dict[MealType, List[FoodInDB]]:
    meals: Dict[MealType, List[FoodInDB]] = defaultdict(list)
    cursor = foods_collection.find({"type": {"$in": [diet_type, "balanced"]}})
    async for item in cursor:
        food = FoodInDB(**item)
        for meal_type in food.mealType:
            meals[meal_type].append(food)
    return meals


def _choose_meal_items(
    available_foods: Sequence[FoodInDB],
    used_ids: set[str],
    target_calories: float,
) -> List[MealEntry]:
    if not available_foods:
        return []

    candidates = [food for food in available_foods if str(food.id) not in used_ids]
    if not candidates:
        candidates = list(available_foods)

    random.shuffle(candidates)
    selection = []
    total = 0
    available_ids = {str(food.id) for food in available_foods}
    allow_repeats = not (available_ids - used_ids)

    for food in candidates:
        food_id = str(food.id)
        if not allow_repeats and food_id in used_ids:
            continue
        selection.append(food)
        used_ids.add(food_id)
        total += food.calories
        if total >= target_calories * 0.8:
            break

    return [
        MealEntry(
            name=item.food,
            calories=item.calories,
            protein=item.protein,
            carbs=item.carbs,
            fat=item.fat,
        )
        for item in selection
    ]


def _compute_macro_totals(meals: Dict[MealType, List[MealEntry]]) -> Dict[str, float]:
    totals = {"protein": 0.0, "carbs": 0.0, "fat": 0.0}
    for meal_entries in meals.values():
        for entry in meal_entries:
            totals["protein"] += entry.protein or 0
            totals["carbs"] += entry.carbs or 0
            totals["fat"] += entry.fat or 0
    return {macro: round(value, 2) for macro, value in totals.items()}


async def generate_weekly_plan(
    user: UserInDB,
    foods_collection: AsyncIOMotorCollection,
) -> List[DailyMeals]:
    daily_target = _calculate_daily_calories(user)
    foods_by_meal = await _load_foods_for_user(foods_collection, user.dietType)
    missing_meals = [meal for meal in MEAL_DISTRIBUTION if not foods_by_meal.get(meal)]
    if missing_meals:
        missing_str = ", ".join(missing_meals)
        raise ValueError(f"Insufficient food items for: {missing_str}. Seed more options.")
    used_food_ids: set[str] = set()
    week_plan: List[DailyMeals] = []

    for day in DAYS_OF_WEEK:
        daily_meals: Dict[MealType, List[MealEntry]] = {}
        for meal_type, ratio in MEAL_DISTRIBUTION.items():
            target = daily_target * ratio
            entries = _choose_meal_items(foods_by_meal.get(meal_type, []), used_food_ids, target)
            daily_meals[meal_type] = entries

        macro_totals = _compute_macro_totals(daily_meals)
        total_calories = sum(entry.calories for meals in daily_meals.values() for entry in meals)
        if total_calories == 0:
            total_calories = daily_target

        week_plan.append(
            DailyMeals(
                day=day,
                meals=daily_meals,
                totalCalories=total_calories,
                macros=macro_totals,
            )
        )

    return week_plan


async def generate_7day_plan(
    user: UserInDB,
    foods_collection: AsyncIOMotorCollection,
    *,
    include_descriptions: bool = False,
) -> List[Dict[str, Any]]:
    """Generate a 7-day meal schedule tailored to the user's preferences."""

    daily_target = _resolve_calorie_target(user)
    diet_filters = _resolve_diet_filters(getattr(user, "dietType", "balanced"))
    foods_by_meal = await _load_foods_for_preferences(foods_collection, diet_filters)

    missing_meals = [meal for meal in MEAL_DISTRIBUTION if not foods_by_meal.get(meal)]
    if missing_meals:
        missing_str = ", ".join(sorted(missing_meals))
        raise ValueError(f"Insufficient food items for: {missing_str}. Seed more options.")

    used_food_ids: set[str] = set()
    weekly_plan: List[Dict[str, Any]] = []

    for day_name in DAYS_OF_WEEK:
        day_meals: Dict[str, List[str]] = {}
        day_calories = 0

        for meal_type, ratio in MEAL_DISTRIBUTION.items():
            entries = _choose_meal_items(
                foods_by_meal.get(meal_type, []),
                used_food_ids,
                daily_target * ratio,
            )
            meal_names = [entry.name for entry in entries]
            day_meals[meal_type] = meal_names
            day_calories += sum(entry.calories for entry in entries)

        if day_calories == 0:
            day_calories = daily_target

        day_payload: Dict[str, Any] = {
            "day": day_name,
            "meals": day_meals,
            "totalCalories": day_calories,
        }

        if include_descriptions:
            description = await _maybe_generate_day_description(day_payload)
            if description:
                day_payload["description"] = description

        weekly_plan.append(day_payload)

    return weekly_plan


def _resolve_calorie_target(user: UserInDB) -> int:
    explicit_target = getattr(user, "caloriesTarget", None)
    if isinstance(explicit_target, (int, float)) and explicit_target > 0:
        return int(explicit_target)
    return _calculate_daily_calories(user)


def _resolve_diet_filters(diet_type: str) -> List[str]:
    normalized = (diet_type or "balanced").replace("-", "_").lower()
    base_filters = {"balanced"}

    diet_map: Dict[str, List[str]] = {
        "veg": ["veg"],
        "non_veg": ["non_veg"],
        "vegan": ["vegan"],
        "keto": ["keto"],
        "paleo": ["paleo"],
    }

    base_filters.update(diet_map.get(normalized, []))
    return list(base_filters)


async def _load_foods_for_preferences(
    foods_collection: AsyncIOMotorCollection,
    diet_filters: List[str],
) -> Dict[MealType, List[FoodInDB]]:
    meals: Dict[MealType, List[FoodInDB]] = defaultdict(list)
    cursor = foods_collection.find({"type": {"$in": diet_filters}})

    async for item in cursor:
        food = FoodInDB(**item)
        for meal_type in food.mealType:
            meals[meal_type].append(food)

    return meals


async def _maybe_generate_day_description(day_payload: Dict[str, Any]) -> Optional[str]:
    prompt = (
        "Summarize the following daily meal plan in one friendly sentence (max 40 words). "
        "Highlight the variety and how it supports healthy eating.\n"
        f"Plan: {json.dumps(day_payload, ensure_ascii=False)}"
    )

    description = await asyncio.to_thread(_call_gemini, prompt)
    return description


def _call_gemini(prompt: str) -> Optional[str]:
    settings = get_settings()
    if not settings.gemini_api_key or not settings.gemini_model:
        return None

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
        ]
    }

    try:
        response = requests.post(
            endpoint,
            params={"key": settings.gemini_api_key},
            json=payload,
            timeout=30,
        )
    except Exception as exc:  # pragma: no cover
        _LOGGER.warning("Gemini request failed: %s", exc)
        return None

    if response.status_code != 200:
        _LOGGER.warning("Gemini API returned %s: %s", response.status_code, response.text)
        return None

    try:
        data = response.json()
    except ValueError as exc:  # pragma: no cover
        _LOGGER.warning("Failed to decode Gemini response: %s", exc)
        return None

    return _extract_text_from_gemini_response(data)


def _extract_text_from_gemini_response(data: Dict[str, Any]) -> Optional[str]:
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

    top_level = data.get("text")
    if isinstance(top_level, str) and top_level.strip():
        return top_level.strip()

    return None
