import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Brain, HeartPulse, Salad, Sparkles } from "lucide-react";

import FoodCard from "@/components/FoodCard";
import { useAuth } from "@/context/AuthContext";

const Home = () => {
  const { user } = useAuth();

  return (
    <div className="mx-auto flex w-full max-w-6xl flex-col gap-16 px-4">
      <section className="grid gap-10 pt-10 lg:grid-cols-[1.2fr_1fr] lg:items-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="space-y-6"
        >
          <span className="inline-flex items-center gap-2 rounded-full bg-emerald-100 px-4 py-1 text-sm font-semibold text-emerald-700">
            <Sparkles className="h-4 w-4" /> AI Personalized Wellness
          </span>
          <h1 className="text-4xl font-bold text-slate-900 md:text-5xl">
            Design your week with a smart, adaptive diet plan tailored to your goals.
          </h1>
          <p className="max-w-xl text-lg text-slate-600">
            Combine science-backed calorie targets with delicious meal ideas curated from our nutrition library.
            Your plan adapts as you do—day after day.
          </p>
          <div className="flex flex-wrap items-center gap-4">
            <Link
              to={user ? "/diet-plan" : "/register"}
              className="rounded-full bg-emerald-500 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-emerald-200 transition hover:scale-105 hover:bg-emerald-600"
            >
              {user ? "View My Plan" : "Generate My Diet Plan"}
            </Link>
            <Link
              to="/dashboard"
              className="inline-flex items-center gap-2 text-sm font-semibold text-emerald-600 transition hover:text-emerald-700"
            >
              Explore Dashboard →
            </Link>
          </div>
          <div className="grid gap-6 rounded-3xl border border-emerald-100 bg-white/70 p-6 shadow-lg shadow-emerald-100/50 lg:grid-cols-3">
            <div>
              <p className="text-2xl font-semibold text-slate-900">7-day</p>
              <p className="text-sm text-slate-500">Unique rotating meal plans</p>
            </div>
            <div>
              <p className="text-2xl font-semibold text-slate-900">Macro smart</p>
              <p className="text-sm text-slate-500">Auto-balanced macros each day</p>
            </div>
            <div>
              <p className="text-2xl font-semibold text-slate-900">Chatbot</p>
              <p className="text-sm text-slate-500">Ask food + nutrition questions anytime</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2, duration: 0.8 }}
          className="relative overflow-hidden rounded-3xl border border-emerald-100 bg-white shadow-xl shadow-emerald-200"
        >
          <div className="absolute -top-10 -left-10 h-40 w-40 rounded-full bg-gradient-to-br from-emerald-200 to-emerald-100" />
          <div className="absolute -bottom-12 -right-8 h-44 w-44 rounded-full bg-gradient-to-br from-lime-200 to-emerald-100" />
          <div className="relative p-8">
            <h3 className="text-xl font-semibold text-slate-900">Your wellness snapshot</h3>
            <p className="mt-2 text-sm text-slate-500">
              Combine your biometrics, goals, and food preferences to shape an adaptive meal journey.
            </p>
            <div className="mt-6 space-y-4">
              {[
                { label: "Current goal", value: user?.goal ?? "Not set" },
                { label: "Activity", value: user?.activityLevel ?? "moderate" },
                { label: "Diet preference", value: user?.dietType ?? "balanced" },
              ].map((item) => (
                <div key={item.label} className="flex items-center justify-between rounded-2xl bg-emerald-50 px-4 py-3">
                  <span className="text-sm font-medium text-emerald-700">{item.label}</span>
                  <span className="text-sm font-semibold capitalize text-emerald-600">{item.value}</span>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      </section>

      <section className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <FoodCard
          title="AI meal intelligence"
          description="We analyze hundreds of foods to build non-repetitive, macro-balanced plans for your entire week."
          icon={<Brain className="h-6 w-6" />}
        />
        <FoodCard
          title="Macro tracking"
          description="Each day is portioned with calories, protein, carbs, and fats distributed for your target."
          icon={<HeartPulse className="h-6 w-6" />}
        />
        <FoodCard
          title="Goal-based adjustments"
          description="Weight loss or gain? Calorie offsets are auto-applied using Mifflin-St Jeor and activity multipliers."
          icon={<Salad className="h-6 w-6" />}
        />
        <FoodCard
          title="Conversational support"
          description="Ask about ingredients, portion swaps, or nutrition tips via the built-in chatbot."
          icon={<Sparkles className="h-6 w-6" />}
        />
      </section>

      <section className="overflow-hidden rounded-3xl border border-emerald-100 bg-white/80 p-6 shadow-lg shadow-emerald-100">
        <div className="grid gap-6 lg:grid-cols-[1.2fr_1fr] lg:items-center">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wider text-emerald-500">Testimonials</p>
            <h2 className="mt-2 text-3xl font-bold text-slate-900">Trusted by mindful eaters</h2>
            <p className="mt-4 text-sm text-slate-600">
              “I regenerated my diet plan each week and never hit a boring meal. The macro summary keeps me on track.”
            </p>
            <p className="mt-2 text-xs font-semibold text-emerald-600">— Alisha, fitness creator</p>
          </div>
          <div className="rounded-2xl bg-gradient-to-br from-emerald-500 to-lime-500 p-6 text-white">
            <p className="text-sm font-medium uppercase tracking-wider text-emerald-50">Plan highlight</p>
            <p className="mt-2 text-3xl font-bold">1,850 kcal / day</p>
            <div className="mt-4 grid gap-3 text-sm">
              <div className="flex items-center justify-between">
                <span>Breakfast</span>
                <span>25%</span>
              </div>
              <div className="flex items-center justify-between">
                <span>Lunch</span>
                <span>35%</span>
              </div>
              <div className="flex items-center justify-between">
                <span>Dinner</span>
                <span>30%</span>
              </div>
              <div className="flex items-center justify-between">
                <span>Snacks</span>
                <span>10%</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
