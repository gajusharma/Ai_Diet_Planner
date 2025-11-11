export type MealType = "breakfast" | "lunch" | "dinner" | "snacks";

export type MealEntry = {
  name: string;
  calories: number;
  protein?: number;
  carbs?: number;
  fat?: number;
};

export type DailyMeals = {
  day: string;
  meals: Record<MealType, MealEntry[]>;
  totalCalories: number;
  macros: Record<"protein" | "carbs" | "fat", number>;
};

export type MealPlan = {
  _id: string;
  userId: string;
  week: DailyMeals[];
  createdAt: string;
};
