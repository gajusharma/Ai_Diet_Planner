import { motion } from "framer-motion";
import { BarChart, Calendar, RefreshCw } from "lucide-react";
import { Link } from "react-router-dom";

import DaySummaryCard from "@/components/DaySummaryCard";
import Spinner from "@/components/Spinner";
import WeeklyCalorieChart from "@/components/WeeklyCalorieChart";
import { useAuth } from "@/context/AuthContext";
import useDietPlan from "@/hooks/useDietPlan";
import type { DailyMeals } from "@/types/diet";

const Dashboard = () => {
  const { user } = useAuth();
  const { plan, loading, error, generatePlan, regeneratePlan } = useDietPlan();

  if (loading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <Spinner />
      </div>
    );
  }

  return (
    <div className="mx-auto flex w-full max-w-6xl flex-col gap-8 px-4">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-bold text-slate-900">
          Welcome back, <span className="text-emerald-600">{user?.name?.split(" ")[0]}</span>!
        </h1>
        <p className="mt-2 text-slate-600">Here’s your wellness dashboard for the week.</p>
      </motion.div>

      {error && (
        <div className="rounded-2xl border-2 border-red-200 bg-red-50 p-6 text-center text-red-700">
          <h3 className="font-semibold">Could not load diet plan</h3>
          <p className="mt-1 text-sm">{error}</p>
          <button
            onClick={() => regeneratePlan()}
            className="mt-4 inline-flex items-center gap-2 rounded-full bg-red-500 px-5 py-2 text-sm font-semibold text-white shadow-lg shadow-red-200 transition hover:bg-red-600"
          >
            <RefreshCw className="h-4 w-4" />
            Try regenerating
          </button>
        </div>
      )}

      {plan && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="grid gap-6 lg:grid-cols-3"
        >
          <div className="space-y-6 lg:col-span-2">
            <div className="grid gap-6 sm:grid-cols-2">
              {plan.week.slice(0, 2).map((day: DailyMeals) => (
                <DaySummaryCard key={day.day} day={day.day} totalCalories={day.totalCalories} macros={day.macros} />
              ))}
            </div>
            <div className="rounded-2xl border border-emerald-100 bg-white/80 p-6 shadow-lg shadow-emerald-100/50">
              <h3 className="text-lg font-semibold text-slate-800">Weekly Calorie Distribution</h3>
              <p className="text-sm text-slate-500">A look at your planned intake across the week.</p>
              <div className="mt-4 h-60">
                <WeeklyCalorieChart data={plan.week} />
              </div>
            </div>
          </div>

          <div className="rounded-2xl border border-emerald-100 bg-white/80 p-6 shadow-lg shadow-emerald-100/50 lg:col-span-1">
            <h3 className="text-lg font-semibold text-slate-800">Quick Actions</h3>
            <div className="mt-4 space-y-3">
              <Link
                to="/diet-plan"
                className="flex w-full items-center gap-3 rounded-xl bg-emerald-50 p-4 text-left text-sm font-semibold text-emerald-700 transition hover:bg-emerald-100"
              >
                <Calendar className="h-5 w-5" />
                View Full 7-Day Plan
              </Link>
              <button
                onClick={() => generatePlan()}
                className="flex w-full items-center gap-3 rounded-xl bg-emerald-50 p-4 text-left text-sm font-semibold text-emerald-700 transition hover:bg-emerald-100"
              >
                <RefreshCw className="h-5 w-5" />
                Generate New Plan
              </button>
              <button
                onClick={() => regeneratePlan()}
                className="flex w-full items-center gap-3 rounded-xl bg-emerald-50 p-4 text-left text-sm font-semibold text-emerald-700 transition hover:bg-emerald-100"
              >
                <RefreshCw className="h-5 w-5" />
                Regenerate My Plan
              </button>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default Dashboard;
