import os
from itertools import product
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from pymongo import MongoClient

TARGET_DATASET_SIZE = 500

CUISINES = [
    "Mediterranean",
    "Indian",
    "Mexican",
    "Italian",
    "Thai",
    "Japanese",
    "Middle Eastern",
    "American",
    "Vietnamese",
    "Greek",
]

BREAKFAST_FLAVORS = [
    "Cinnamon",
    "Berry",
    "Cacao",
    "Vanilla",
    "Nutty",
    "Citrus",
    "Maple",
    "Spiced",
]

BREAKFAST_ACCENTS = [
    "Toasted Almonds",
    "Chia Swirl",
    "Banana Slices",
    "Pumpkin Seeds",
    "Blueberry Compote",
    "Roasted Coconut",
    "Honey Drizzle",
    "Apple Crunch",
]

VEG_PROTEINS = [
    "Paneer Tikka",
    "Tofu Masala",
    "Halloumi Grill",
    "Chickpea Falafel",
    "Lentil Kofta",
    "Mushroom Stroganoff",
    "Black Bean Patty",
    "Soy Curl Roast",
]

VEG_GRAINS = [
    "Quinoa",
    "Brown Rice",
    "Millet",
    "Barley",
    "Farro",
    "Buckwheat",
    "Bulgur",
]

VEG_SAUCES = [
    "Herb Yogurt",
    "Tomato Basil",
    "Coconut Curry",
    "Sesame Ginger",
    "Tahini Lime",
    "Spicy Peanut",
    "Green Chutney",
]

VEGAN_PROTEINS = [
    "Tofu Cubes",
    "Tempeh Strips",
    "Chickpea Cakes",
    "Black Bean Crumble",
    "Lentil Medallions",
    "Seitan Bites",
    "Edamame Mix",
    "Jackfruit Shreds",
]

VEGAN_GRAINS = [
    "Wild Rice",
    "Quinoa",
    "Brown Rice",
    "Barley",
    "Freekeh",
    "Buckwheat",
    "Sorghum",
]

VEGAN_SAUCES = [
    "Cashew Cream",
    "Miso Sesame",
    "Chimichurri",
    "Maple Mustard",
    "Avocado Lime",
    "Roasted Pepper",
    "Smoky Walnut",
]

NONVEG_BREAKFAST_PROTEINS = [
    "Egg White",
    "Smoked Salmon",
    "Turkey Sausage",
    "Chicken Sausage",
    "Ham Spinach",
    "Prosciutto",
    "Bacon Spinach",
]

NONVEG_PROTEINS = [
    "Grilled Chicken Breast",
    "Roasted Turkey",
    "Salmon Fillet",
    "Seared Tuna",
    "Garlic Shrimp",
    "Herb Tilapia",
    "Lean Beef Steak",
    "Lamb Skewer",
]

NONVEG_SIDES = [
    "Quinoa Pilaf",
    "Brown Rice",
    "Roasted Vegetables",
    "Sweet Potato Mash",
    "Grilled Asparagus",
    "Sauteed Greens",
    "Farro Salad",
]

NONVEG_SAUCES = [
    "Lemon Herb",
    "Smoky Paprika",
    "Garlic Butter",
    "Teriyaki Glaze",
    "Chipotle Yogurt",
    "Mustard Dill",
    "Pesto Drizzle",
]

SNACK_BASES = [
    "Energy Bites",
    "Trail Mix",
    "Roasted Chickpeas",
    "Protein Yogurt Bowl",
    "Veggie Sticks",
    "Edamame Cups",
    "Fruit Salsa",
    "Stuffed Dates",
]

SNACK_FLAVORS = [
    "Cocoa",
    "Spiced",
    "Citrus",
    "Savory",
    "Maple",
    "Herbed",
    "Chili Lime",
    "Ginger",
]

SNACK_ACCENTS = [
    "Pumpkin Seeds",
    "Almond Dust",
    "Coconut Flakes",
    "Dark Chocolate Shavings",
    "Dried Cranberries",
    "Sesame Crunch",
    "Pomegranate",
    "Toasted Pecans",
]

KETO_PROTEINS = [
    "Grilled Chicken Thigh",
    "Salmon Steak",
    "Pork Tenderloin",
    "Garlic Shrimp",
    "Beef Skewers",
    "Turkey Meatballs",
    "Mahi Mahi",
]

KETO_SIDES = [
    "Cauliflower Mash",
    "Zucchini Noodles",
    "Sauteed Spinach",
    "Grilled Zucchini",
    "Roasted Brussels Sprouts",
    "Avocado Salad",
    "Garlic Mushrooms",
]

KETO_TOPPINGS = [
    "Herb Butter",
    "Garlic Aioli",
    "Parmesan Dust",
    "Pesto Drizzle",
    "Chipotle Mayo",
    "Lemon Butter",
    "Basil Cream",
]

PALEO_PROTEINS = [
    "Grass-Fed Steak",
    "Roast Chicken",
    "Wild Salmon",
    "Pork Chop",
    "Bison Burger",
    "Turkey Cutlet",
    "Venison Medallions",
]

PALEO_VEGETABLES = [
    "Roasted Root Veggies",
    "Garlic Broccoli",
    "Charred Peppers",
    "Herb Cauliflower",
    "Citrus Greens",
    "Brussels Hash",
    "Sweet Potato Wedges",
]

PALEO_SAUCES = [
    "Rosemary Jus",
    "Citrus Vinaigrette",
    "Garlic Mushroom Sauce",
    "Smoky Tomato Relish",
    "Herb Ghee",
    "Chile Lime Sauce",
    "Walnut Pesto",
]


Blueprint = Dict[str, Any]


BLUEPRINTS: List[Blueprint] = [
    {
        "diet_type": "balanced",
        "meal_types": ["breakfast"],
        "name_pattern": "{cuisine} {flavor} Oat Power Bowl with {accent}",
        "placeholders": {
            "cuisine": CUISINES,
            "flavor": BREAKFAST_FLAVORS,
            "accent": BREAKFAST_ACCENTS,
        },
        "base": {"calories": 340, "protein": 18, "carbs": 48, "fat": 12},
        "limit": 70,
    },
    {
        "diet_type": "balanced",
        "meal_types": ["lunch", "dinner"],
        "name_pattern": "{cuisine} {protein} Grain Bowl with {sauce}",
        "placeholders": {
            "cuisine": CUISINES,
            "protein": [
                "Grilled Chicken",
                "Seared Tofu",
                "Roasted Salmon",
                "Chickpea Falafel",
                "Turkey Meatballs",
                "Paneer Cubes",
                "Tempeh Strips",
                "Shrimp",
            ],
            "sauce": [
                "Herb Yogurt",
                "Smoky Paprika",
                "Sesame Ginger",
                "Lemon Tahini",
                "Garlic Chimichurri",
                "Maple Mustard",
                "Pesto Drizzle",
            ],
        },
        "base": {"calories": 520, "protein": 34, "carbs": 55, "fat": 18},
        "limit": 80,
    },
    {
        "diet_type": "balanced",
        "meal_types": ["snacks"],
        "name_pattern": "{flavor} {base} Snack Cup with {accent}",
        "placeholders": {
            "flavor": SNACK_FLAVORS,
            "base": SNACK_BASES,
            "accent": SNACK_ACCENTS,
        },
        "base": {"calories": 220, "protein": 10, "carbs": 26, "fat": 9},
        "limit": 50,
    },
    {
        "diet_type": "veg",
        "meal_types": ["breakfast"],
        "name_pattern": "{cuisine} Veggie Scramble with {accent}",
        "placeholders": {
            "cuisine": CUISINES,
            "accent": BREAKFAST_ACCENTS,
        },
        "base": {"calories": 310, "protein": 17, "carbs": 38, "fat": 11},
        "limit": 60,
    },
    {
        "diet_type": "veg",
        "meal_types": ["lunch", "dinner"],
        "name_pattern": "{cuisine} {protein} Bowl with {grain} and {sauce}",
        "placeholders": {
            "cuisine": CUISINES,
            "protein": VEG_PROTEINS,
            "grain": VEG_GRAINS,
            "sauce": VEG_SAUCES,
        },
        "base": {"calories": 500, "protein": 28, "carbs": 60, "fat": 17},
        "limit": 70,
    },
    {
        "diet_type": "veg",
        "meal_types": ["snacks"],
        "name_pattern": "{flavor} Paneer Snack Bites with {accent}",
        "placeholders": {
            "flavor": SNACK_FLAVORS,
            "accent": SNACK_ACCENTS,
        },
        "base": {"calories": 210, "protein": 12, "carbs": 18, "fat": 12},
        "limit": 40,
    },
    {
        "diet_type": "vegan",
        "meal_types": ["breakfast"],
        "name_pattern": "{cuisine} {flavor} Vegan Power Oats with {accent}",
        "placeholders": {
            "cuisine": CUISINES,
            "flavor": BREAKFAST_FLAVORS,
            "accent": BREAKFAST_ACCENTS,
        },
        "base": {"calories": 330, "protein": 16, "carbs": 50, "fat": 11},
        "limit": 60,
    },
    {
        "diet_type": "vegan",
        "meal_types": ["lunch", "dinner"],
        "name_pattern": "{cuisine} {protein} Glow Bowl with {grain} and {sauce}",
        "placeholders": {
            "cuisine": CUISINES,
            "protein": VEGAN_PROTEINS,
            "grain": VEGAN_GRAINS,
            "sauce": VEGAN_SAUCES,
        },
        "base": {"calories": 490, "protein": 24, "carbs": 62, "fat": 16},
        "limit": 70,
    },
    {
        "diet_type": "vegan",
        "meal_types": ["snacks"],
        "name_pattern": "{flavor} Plant Power Snack Mix with {accent}",
        "placeholders": {
            "flavor": SNACK_FLAVORS,
            "accent": SNACK_ACCENTS,
        },
        "base": {"calories": 205, "protein": 11, "carbs": 22, "fat": 10},
        "limit": 40,
    },
    {
        "diet_type": "non_veg",
        "meal_types": ["breakfast"],
        "name_pattern": "{cuisine} {protein} Egg Scramble with {accent}",
        "placeholders": {
            "cuisine": CUISINES,
            "protein": NONVEG_BREAKFAST_PROTEINS,
            "accent": BREAKFAST_ACCENTS,
        },
        "base": {"calories": 320, "protein": 24, "carbs": 18, "fat": 16},
        "limit": 50,
    },
    {
        "diet_type": "non_veg",
        "meal_types": ["lunch", "dinner"],
        "name_pattern": "{cuisine} {protein} Plate with {side} and {sauce}",
        "placeholders": {
            "cuisine": CUISINES,
            "protein": NONVEG_PROTEINS,
            "side": NONVEG_SIDES,
            "sauce": NONVEG_SAUCES,
        },
        "base": {"calories": 560, "protein": 42, "carbs": 45, "fat": 22},
        "limit": 90,
    },
    {
        "diet_type": "non_veg",
        "meal_types": ["snacks"],
        "name_pattern": "{flavor} Protein Snack Cup with {accent}",
        "placeholders": {
            "flavor": SNACK_FLAVORS,
            "accent": SNACK_ACCENTS,
        },
        "base": {"calories": 230, "protein": 15, "carbs": 16, "fat": 12},
        "limit": 30,
    },
    {
        "diet_type": "keto",
        "meal_types": ["breakfast"],
        "name_pattern": "{cuisine} Keto Breakfast Bowl with {accent}",
        "placeholders": {
            "cuisine": CUISINES,
            "accent": [
                "Avocado",
                "Herb Butter",
                "Cheddar",
                "Smoked Bacon",
                "Spinach",
                "Pepper Jack",
                "Turkey Bits",
            ],
        },
        "base": {"calories": 360, "protein": 22, "carbs": 8, "fat": 26},
        "limit": 50,
        "carb_cap": 12,
    },
    {
        "diet_type": "keto",
        "meal_types": ["lunch", "dinner"],
        "name_pattern": "{cuisine} {protein} Keto Plate with {side} and {topping}",
        "placeholders": {
            "cuisine": CUISINES,
            "protein": KETO_PROTEINS,
            "side": KETO_SIDES,
            "topping": KETO_TOPPINGS,
        },
        "base": {"calories": 540, "protein": 36, "carbs": 10, "fat": 36},
        "limit": 80,
        "carb_cap": 15,
    },
    {
        "diet_type": "keto",
        "meal_types": ["snacks"],
        "name_pattern": "{flavor} Keto Snack Pack with {accent}",
        "placeholders": {
            "flavor": [
                "Herb",
                "Garlic",
                "Smoked",
                "Chili",
                "Lemon",
                "Truffle",
                "Rosemary",
            ],
            "accent": [
                "Cheddar Cubes",
                "Almonds",
                "Walnuts",
                "Pecans",
                "Olives",
                "Parmesan Crisps",
                "Macadamia",
            ],
        },
        "base": {"calories": 210, "protein": 10, "carbs": 6, "fat": 18},
        "limit": 30,
        "carb_cap": 9,
    },
    {
        "diet_type": "paleo",
        "meal_types": ["lunch", "dinner"],
        "name_pattern": "{cuisine} {protein} Paleo Skillet with {vegetable} and {sauce}",
        "placeholders": {
            "cuisine": CUISINES,
            "protein": PALEO_PROTEINS,
            "vegetable": PALEO_VEGETABLES,
            "sauce": PALEO_SAUCES,
        },
        "base": {"calories": 520, "protein": 38, "carbs": 28, "fat": 24},
        "limit": 60,
        "carb_cap": 35,
    },
]


def _apply_variation(value: int, index: int, step: int, minimum: int = 0, maximum: Optional[int] = None) -> int:
    offsets = [-2, -1, 0, 1, 2, 3]
    adjusted = value + offsets[index % len(offsets)] * step
    if maximum is not None:
        adjusted = min(adjusted, maximum)
    adjusted = max(adjusted, minimum)
    return int(adjusted)


def _nutrition_variation(base: Dict[str, int], index: int, blueprint: Blueprint) -> Dict[str, int]:
    calories = _apply_variation(base["calories"], index, blueprint.get("calorie_step", 25), minimum=150)
    protein = _apply_variation(base["protein"], index // 2, blueprint.get("protein_step", 3), minimum=4)
    carbs = _apply_variation(
        base["carbs"],
        index // 3,
        blueprint.get("carb_step", 5),
        minimum=0,
        maximum=blueprint.get("carb_cap"),
    )
    fat = _apply_variation(base["fat"], index // 4, blueprint.get("fat_step", 2), minimum=2)

    return {
        "calories": calories,
        "protein": protein,
        "carbs": carbs,
        "fat": fat,
    }


def _expand_blueprint(blueprint: Blueprint) -> List[Dict[str, Any]]:
    keys = list(blueprint["placeholders"].keys())
    values_product = product(*(blueprint["placeholders"][key] for key in keys))
    documents: List[Dict[str, Any]] = []

    for idx, combination in enumerate(values_product):
        if idx >= blueprint["limit"]:
            break

        context = dict(zip(keys, combination))
        name = blueprint["name_pattern"].format(**context)
        nutrition = _nutrition_variation(blueprint["base"], idx, blueprint)

        documents.append(
            {
                "food": name,
                "calories": nutrition["calories"],
                "protein": nutrition["protein"],
                "carbs": nutrition["carbs"],
                "fat": nutrition["fat"],
                "mealType": list(blueprint["meal_types"]),
                "type": blueprint["diet_type"],
            }
        )

    return documents


def _generate_food_documents() -> List[Dict[str, Any]]:
    documents: List[Dict[str, Any]] = []
    for blueprint in BLUEPRINTS:
        documents.extend(_expand_blueprint(blueprint))

    unique_docs: List[Dict[str, Any]] = []
    seen = set()
    for doc in documents:
        key = (doc["food"], tuple(doc["mealType"]), doc["type"])
        if key in seen:
            continue
        seen.add(key)
        unique_docs.append(doc)

    return unique_docs


def seed_foods() -> None:
    load_dotenv()
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise RuntimeError("MONGO_URI environment variable is not set")

    database_name = os.getenv("MONGO_DB_NAME", "aiplanner")
    collection_name = os.getenv("FOOD_COLLECTION_NAME", "foods")

    documents = _generate_food_documents()
    print(f"Generated {len(documents)} meal templates")

    force_refresh = os.getenv("FORCE_REFRESH_FOODS", "false").lower() == "true"

    client = MongoClient(mongo_uri)
    try:
        db = client[database_name]
        collection = db[collection_name]
        print(f"✅ Connected to MongoDB ({database_name}/{collection_name})")

        existing = collection.count_documents({})
        if existing >= TARGET_DATASET_SIZE and not force_refresh:
            print(
                f"Collection already contains {existing} items (>= {TARGET_DATASET_SIZE}). Skipping bulk insert."
            )
            return

        if existing:
            reason = "force flag" if force_refresh else f"only {existing} items (< {TARGET_DATASET_SIZE})"
            print(f"Refreshing collection because {reason}...")
            collection.delete_many({})

        result = collection.insert_many(documents)
        print(f"✅ Inserted {len(result.inserted_ids)} foods successfully")
    finally:
        client.close()


if __name__ == "__main__":
    seed_foods()

