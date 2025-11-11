import { motion } from "framer-motion";
import { Flame } from "lucide-react";

import type { MealEntry } from "@/types/diet";

const container = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

type MealCardProps = {
  title: string;
  entries: MealEntry[];
  accentBgClass?: string;
  accentTextClass?: string;
};

const MealCard = ({ title, entries, accentBgClass = "bg-emerald-100", accentTextClass = "text-emerald-700" }: MealCardProps) => {
  const totalCalories = entries.reduce((sum, entry) => sum + entry.calories, 0);
  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="visible"
      transition={{ type: "spring", stiffness: 120, damping: 14 }}
      className="flex h-full flex-col rounded-2xl border border-emerald-100/60 bg-white/80 p-5 shadow-lg shadow-emerald-100/50 backdrop-blur"
    >
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-slate-800">{title}</h3>
  <span className={`rounded-full px-3 py-1 text-xs font-semibold ${accentBgClass} ${accentTextClass}`}>
          {totalCalories} kcal
        </span>
      </div>
      <div className="mt-4 space-y-3">
        {entries.map((entry) => (
          <div
            key={`${entry.name}-${entry.calories}`}
            className="rounded-xl border border-emerald-50 bg-gradient-to-br from-white to-emerald-50/40 p-3 shadow-sm"
          >
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-semibold text-slate-800">{entry.name}</p>
                <div className="mt-1 grid grid-cols-3 gap-2 text-xs text-slate-500">
                  {entry.protein !== undefined && (
                    <span>Protein: {entry.protein}g</span>
                  )}
                  {entry.carbs !== undefined && (
                    <span>Carbs: {entry.carbs}g</span>
                  )}
                  {entry.fat !== undefined && <span>Fat: {entry.fat}g</span>}
                </div>
              </div>
              <div className="flex items-center gap-1 text-xs font-semibold text-emerald-600">
                <Flame className="h-3.5 w-3.5" />
                <span>{entry.calories} kcal</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  );
};

export default MealCard;
