"""Seed the MongoDB foods collection with starter data."""

import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from pymongo import MongoClient

# Sample food data
SAMPLE_FOODS = [
    # Breakfast items
    {"food": "Oatmeal with Banana", "calories": 300, "protein": 10, "carbs": 54, "fat": 6, "type": "balanced", "mealType": ["breakfast"]},
    {"food": "Greek Yogurt with Berries", "calories": 250, "protein": 20, "carbs": 35, "fat": 5, "type": "balanced", "mealType": ["breakfast", "snacks"]},
    {"food": "Scrambled Eggs with Toast", "calories": 350, "protein": 22, "carbs": 30, "fat": 15, "type": "non_veg", "mealType": ["breakfast"]},
    {"food": "Avocado Toast", "calories": 320, "protein": 8, "carbs": 40, "fat": 16, "type": "veg", "mealType": ["breakfast"]},
    {"food": "Protein Smoothie", "calories": 280, "protein": 25, "carbs": 35, "fat": 6, "type": "balanced", "mealType": ["breakfast", "snacks"]},
    
    # Lunch items
    {"food": "Grilled Chicken Salad", "calories": 450, "protein": 40, "carbs": 25, "fat": 20, "type": "non_veg", "mealType": ["lunch"]},
    {"food": "Quinoa Buddha Bowl", "calories": 500, "protein": 15, "carbs": 70, "fat": 18, "type": "veg", "mealType": ["lunch"]},
    {"food": "Turkey Sandwich", "calories": 480, "protein": 30, "carbs": 50, "fat": 15, "type": "non_veg", "mealType": ["lunch"]},
    {"food": "Lentil Soup with Bread", "calories": 420, "protein": 18, "carbs": 65, "fat": 10, "type": "veg", "mealType": ["lunch"]},
    {"food": "Salmon with Rice", "calories": 550, "protein": 35, "carbs": 60, "fat": 18, "type": "non_veg", "mealType": ["lunch", "dinner"]},
    
    # Dinner items
    {"food": "Grilled Steak with Veggies", "calories": 600, "protein": 45, "carbs": 30, "fat": 32, "type": "non_veg", "mealType": ["dinner"]},
    {"food": "Pasta Primavera", "calories": 520, "protein": 15, "carbs": 75, "fat": 18, "type": "veg", "mealType": ["dinner"]},
    {"food": "Baked Chicken Breast", "calories": 480, "protein": 50, "carbs": 20, "fat": 20, "type": "non_veg", "mealType": ["dinner"]},
    {"food": "Tofu Stir-Fry", "calories": 450, "protein": 20, "carbs": 55, "fat": 16, "type": "veg", "mealType": ["dinner"]},
    {"food": "Fish Tacos", "calories": 500, "protein": 30, "carbs": 50, "fat": 20, "type": "non_veg", "mealType": ["dinner"]},
    
    # Snacks
    {"food": "Mixed Nuts", "calories": 180, "protein": 6, "carbs": 8, "fat": 16, "type": "balanced", "mealType": ["snacks"]},
    {"food": "Apple with Peanut Butter", "calories": 200, "protein": 7, "carbs": 25, "fat": 10, "type": "balanced", "mealType": ["snacks"]},
    {"food": "Protein Bar", "calories": 220, "protein": 20, "carbs": 24, "fat": 8, "type": "balanced", "mealType": ["snacks"]},
    {"food": "Hummus with Carrots", "calories": 150, "protein": 6, "carbs": 18, "fat": 7, "type": "veg", "mealType": ["snacks"]},
    {"food": "String Cheese", "calories": 80, "protein": 7, "carbs": 1, "fat": 6, "type": "balanced", "mealType": ["snacks"]},
    
    # Vegan specific
    {"food": "Vegan Protein Bowl", "calories": 480, "protein": 22, "carbs": 65, "fat": 14, "type": "vegan", "mealType": ["lunch", "dinner"]},
    {"food": "Chia Pudding", "calories": 240, "protein": 8, "carbs": 30, "fat": 11, "type": "vegan", "mealType": ["breakfast", "snacks"]},
    {"food": "Tempeh Curry", "calories": 420, "protein": 25, "carbs": 45, "fat": 16, "type": "vegan", "mealType": ["dinner"]},
    
    # Keto options
    {"food": "Keto Egg Muffins", "calories": 280, "protein": 20, "carbs": 5, "fat": 20, "type": "keto", "mealType": ["breakfast"]},
    {"food": "Bacon and Avocado Salad", "calories": 450, "protein": 25, "carbs": 8, "fat": 36, "type": "keto", "mealType": ["lunch"]},
    {"food": "Ribeye Steak with Butter", "calories": 650, "protein": 48, "carbs": 2, "fat": 50, "type": "keto", "mealType": ["dinner"]},
]


def seed_foods() -> None:
    """Seed the foods collection with sample data."""
    load_dotenv()
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise RuntimeError("MONGO_URI is not set in the environment")

    client = MongoClient(mongo_uri)
    try:
        db = client["diet_planner"]
        foods_collection = db["foods"]
        print("✅ Connected to MongoDB")

        existing_count = foods_collection.count_documents({})
        if existing_count > 0:
            print(f"Database already contains {existing_count} food items. Skipping seed.")
            return

        now = datetime.now(tz=timezone.utc)
        for food in SAMPLE_FOODS:
            food["createdAt"] = now
            food["updatedAt"] = now

        result = foods_collection.insert_many(SAMPLE_FOODS)
        print(f"✅ Inserted {len(result.inserted_ids)} foods successfully")
    finally:
        client.close()


if __name__ == "__main__":
    seed_foods()
