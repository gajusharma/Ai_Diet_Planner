import { motion } from "framer-motion";

type DayTabsProps = {
  days?: string[];
  activeDay?: string | null;
  onChange: (day: string) => void;
};

const DayTabs = ({ days = [], activeDay, onChange }: DayTabsProps) => {
  if (days.length === 0) {
    return null;
  }

  return (
    <div className="flex flex-wrap gap-3">
      {days.map((day) => {
        const isActive = day === activeDay;
        return (
          <button
            key={day}
            onClick={() => onChange(day)}
            className={`relative overflow-hidden rounded-full border px-5 py-2 text-sm font-semibold transition ${
              isActive
                ? "border-transparent text-white"
                : "border-emerald-100 bg-white/60 text-emerald-700 hover:border-emerald-300"
            }`}
          >
            {isActive && (
              <motion.span
                layoutId="day-highlight"
                className="absolute inset-0 bg-gradient-to-r from-emerald-500 to-lime-500"
                transition={{ type: "spring", stiffness: 300, damping: 30 }}
              />
            )}
            <span className="relative z-10 mix-blend-plus-lighter">{day}</span>
          </button>
        );
      })}
    </div>
  );
};

export default DayTabs;
