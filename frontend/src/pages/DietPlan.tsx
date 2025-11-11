import { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import { RefreshCw } from "lucide-react";

import DayTabs from "@/components/DayTabs";
import MealCard from "@/components/MealCard";
import Spinner from "@/components/Spinner";
import useDietPlan from "@/hooks/useDietPlan";
import type { DailyMeals, MealEntry, MealType } from "@/types/diet";

const DietPlan = () => {
  const { plan, loading, error, generatePlan, regeneratePlan } = useDietPlan();
  const [activeDay, setActiveDay] = useState<string | null>(null);

  useEffect(() => {
    if (plan && plan.week.length > 0) {
      setActiveDay((previous) => {
        if (previous && plan.week.some((day: DailyMeals) => day.day === previous)) {
          return previous;
        }
        return plan.week[0].day;
      });
    } else {
      setActiveDay(null);
    }
  }, [plan]);

  const days = useMemo(() => {
    if (!plan || plan.week.length === 0) {
      return [];
    }
    return plan.week.map((day: DailyMeals) => day.day);
  }, [plan]);

  const selectedDay: DailyMeals | null = useMemo(() => {
    if (!plan || plan.week.length === 0) {
      return null;
    }
    if (!activeDay) {
      return plan.week[0];
    }
    return plan.week.find((day: DailyMeals) => day.day === activeDay) ?? plan.week[0];
  }, [plan, activeDay]);

  if (loading) {
    return (
      <div className="flex min-h-[70vh] items-center justify-center">
        <Spinner />
      </div>
    );
  }

  return (
    <div className="mx-auto w-full max-w-6xl px-4">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col items-center justify-between gap-4 text-center md:flex-row md:text-left"
      >
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Your 7-Day Meal Plan</h1>
          <p className="mt-1 text-slate-600">
            Here is your personalized diet, balanced for your goals and preferences.
          </p>
          {plan?.createdAt && (
            <p className="mt-2 text-xs font-medium text-emerald-600">
              Last saved on {new Date(plan.createdAt).toLocaleString()}
            </p>
          )}
        </div>
        <div className="flex flex-col items-center gap-3 sm:flex-row">
          <button
            onClick={() => generatePlan()}
            disabled={loading}
            className="inline-flex items-center gap-2 rounded-full border border-emerald-300 px-5 py-2.5 text-sm font-semibold text-emerald-600 transition hover:bg-emerald-50 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Generate Plan
          </button>
          <button
            onClick={() => regeneratePlan()}
            disabled={loading || !plan}
            className="inline-flex items-center gap-2 rounded-full bg-emerald-500 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-emerald-200 transition hover:bg-emerald-600 disabled:cursor-not-allowed disabled:opacity-50"
          >
            <RefreshCw className="h-4 w-4" />
            Regenerate Plan
          </button>
        </div>
      </motion.div>

      {error && (
        <div className="mt-8 rounded-2xl border-2 border-red-200 bg-red-50 p-8 text-center text-red-700">
          <h3 className="text-xl font-semibold">Could not load diet plan</h3>
          <p className="mt-2">{error}</p>
        </div>
      )}

      {!plan && !error && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-10 rounded-2xl border border-dashed border-emerald-200 bg-emerald-50/40 p-10 text-center text-emerald-700"
        >
          No saved meal plan yet. Click &quot;Generate Plan&quot; to craft a personalized 7-day menu.
        </motion.div>
      )}

      {plan?.week && plan.week.length > 0 && (
        <motion.div
          key={plan.createdAt}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mt-8"
        >
          <DayTabs days={days} activeDay={activeDay} onChange={setActiveDay} />
          <div className="mt-8 space-y-6">
            {selectedDay ? (
              (Object.entries(selectedDay.meals) as [MealType, MealEntry[]][]).map(
                ([mealType, entries]) => {
                  const prettyTitle = mealType.charAt(0).toUpperCase() + mealType.slice(1);
                  return <MealCard key={mealType} title={prettyTitle} entries={entries} />;
                },
              )
            ) : (
              <div className="rounded-2xl border border-emerald-100 bg-emerald-50/60 p-6 text-center text-emerald-700">
                No meals available for the selected day yet. Try generating a new plan.
              </div>
            )}
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default DietPlan;
