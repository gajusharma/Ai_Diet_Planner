import type { ReactNode } from "react";
import { motion } from "framer-motion";

const FoodCard = ({ title, description, icon }: { title: string; description: string; icon: ReactNode }) => {
  return (
    <motion.article
      whileHover={{ y: -6, scale: 1.01 }}
      className="relative overflow-hidden rounded-3xl border border-emerald-100 bg-white/70 p-6 shadow-lg shadow-emerald-100/40 backdrop-blur"
    >
      <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-emerald-100 text-emerald-700">
        {icon}
      </div>
      <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
      <p className="mt-2 text-sm text-slate-600">{description}</p>
      <div className="pointer-events-none absolute inset-0 bg-gradient-to-br from-transparent via-transparent to-emerald-50" />
    </motion.article>
  );
};

export default FoodCard;
