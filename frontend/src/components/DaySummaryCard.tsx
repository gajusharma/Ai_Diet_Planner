import { Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";

const COLORS = ["#34d399", "#22d3ee", "#facc15"];

type DaySummaryCardProps = {
  day?: string;
  totalCalories: number;
  macros: Record<string, number>;
};

const DaySummaryCard = ({ day, totalCalories, macros }: DaySummaryCardProps) => {
  const data = Object.entries(macros || {}).map(([key, value], index) => ({
    name: key,
    value,
    fill: COLORS[index % COLORS.length],
  }));

  return (
    <div className="flex flex-col gap-6 rounded-3xl border border-emerald-100 bg-white/80 p-6 shadow-lg shadow-emerald-100/40 backdrop-blur">
      <div>
        <p className="text-sm font-medium text-emerald-500">Daily Summary</p>
        <p className="text-3xl font-semibold text-slate-900">{totalCalories} kcal</p>
        <p className="text-xs text-slate-500">
          {day ? `Target calories for ${day}` : "Target calories for the selected day"}
        </p>
      </div>
      <div className="h-48">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Tooltip
              contentStyle={{
                borderRadius: 12,
                borderColor: "#d1fae5",
                fontSize: 12,
              }}
            />
            <Pie
              data={data}
              dataKey="value"
              nameKey="name"
              innerRadius={50}
              outerRadius={80}
              paddingAngle={3}
              strokeWidth={2}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="grid grid-cols-3 gap-3 text-xs text-slate-600">
        {data.map((item) => (
          <div key={item.name} className="rounded-xl bg-emerald-50/60 px-3 py-2">
            <p className="font-semibold capitalize text-emerald-700">{item.name}</p>
            <p className="text-slate-500">{item.value} g</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DaySummaryCard;
