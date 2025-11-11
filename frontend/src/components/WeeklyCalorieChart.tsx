import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import type { DailyMeals } from "@/types/diet";

interface WeeklyCalorieChartProps {
  data: DailyMeals[];
}

const WeeklyCalorieChart = ({ data }: WeeklyCalorieChartProps) => {
  const chartData = data.map((day) => ({
    name: day.day.slice(0, 3),
    calories: day.totalCalories,
  }));

  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart
        data={chartData}
        margin={{
          top: 20,
          right: 30,
          left: -10,
          bottom: 5,
        }}
      >
        <XAxis dataKey="name" stroke="#9ca3af" fontSize={12} tickLine={false} axisLine={false} />
        <YAxis stroke="#9ca3af" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `${value}`} />
        <Tooltip
          cursor={{ fill: "transparent" }}
          content={({ active, payload }) => {
            if (active && payload && payload.length) {
              return (
                <div className="rounded-lg border border-emerald-200 bg-white/80 p-2 shadow-lg backdrop-blur-sm">
                  <p className="text-sm font-bold text-emerald-600">{`${payload[0].value} kcal`}</p>
                </div>
              );
            }
            return null;
          }}
        />
        <Bar dataKey="calories" fill="#10b981" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default WeeklyCalorieChart;
