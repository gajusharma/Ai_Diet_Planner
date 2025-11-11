import { zodResolver } from "@hookform/resolvers/zod";
import { motion } from "framer-motion";
import { UserPlus } from "lucide-react";
import { useForm } from "react-hook-form";
import { Link } from "react-router-dom";
import { z } from "zod";

import { useAuth } from "@/context/AuthContext";

const schema = z.object({
  name: z.string().min(2, "Name is required"),
  email: z.string().email("Enter a valid email"),
  password: z.string().min(8, "Minimum 8 characters"),
  age: z.coerce.number().min(13).max(100),
  height: z.coerce.number().min(120).max(220),
  weight: z.coerce.number().min(35).max(200),
  goal: z.enum(["weight_loss", "maintenance", "weight_gain"]),
  activityLevel: z.enum(["sedentary", "light", "moderate", "active", "very_active"]),
  dietType: z.enum(["veg", "non_veg", "vegan", "keto", "paleo", "balanced"]),
  gender: z.enum(["male", "female"]),
});

type RegisterForm = z.infer<typeof schema>;

const Register = () => {
  const { register: registerUser } = useAuth();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterForm>({
    resolver: zodResolver(schema),
    defaultValues: {
      goal: "weight_loss",
      activityLevel: "moderate",
      dietType: "balanced",
      gender: "male",
    },
  });

  const onSubmit = async (data: RegisterForm) => {
    await registerUser(data);
  };

  return (
    <div className="mx-auto flex w-full max-w-6xl flex-col gap-12 px-4 pb-16 pt-16">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="space-y-4 text-center">
        <span className="inline-flex items-center gap-2 rounded-full bg-emerald-100 px-4 py-1 text-xs font-semibold uppercase tracking-wide text-emerald-700">
          <UserPlus className="h-4 w-4" /> Create your wellness profile
        </span>
        <h2 className="text-3xl font-bold text-slate-900 md:text-4xl">Personalize your 7-day AI diet plan</h2>
        <p className="mx-auto max-w-2xl text-sm text-slate-600">
          We’ll generate calorie targets using Mifflin–St Jeor, adjust per goal, and curate meals from our nutrition
          library. Update anytime in your profile.
        </p>
      </motion.div>

      <motion.form
        onSubmit={handleSubmit(onSubmit)}
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        className="grid gap-8 rounded-3xl border border-emerald-100 bg-white/80 p-8 shadow-xl shadow-emerald-100 md:grid-cols-2"
      >
        <div className="space-y-4">
          <div>
            <label className="text-sm font-semibold text-slate-700" htmlFor="name">
              Full name
            </label>
            <input
              id="name"
              {...register("name")}
              className="mt-2 w-full rounded-xl border border-emerald-100 bg-white px-4 py-3 text-sm outline-none transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
            />
            {errors.name && <p className="mt-1 text-xs text-red-500">{errors.name.message}</p>}
          </div>

          <div>
            <label className="text-sm font-semibold text-slate-700" htmlFor="email">
              Email address
            </label>
            <input
              id="email"
              type="email"
              {...register("email")}
              className="mt-2 w-full rounded-xl border border-emerald-100 bg-white px-4 py-3 text-sm outline-none transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
            />
            {errors.email && <p className="mt-1 text-xs text-red-500">{errors.email.message}</p>}
          </div>

          <div>
            <label className="text-sm font-semibold text-slate-700" htmlFor="password">
              Password
            </label>
            <input
              id="password"
              type="password"
              {...register("password")}
              className="mt-2 w-full rounded-xl border border-emerald-100 bg-white px-4 py-3 text-sm outline-none transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
            />
            {errors.password && <p className="mt-1 text-xs text-red-500">{errors.password.message}</p>}
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="text-sm font-semibold text-slate-700" htmlFor="age">
                Age
              </label>
              <input
                id="age"
                type="number"
                {...register("age")}
                className="mt-2 w-full rounded-xl border border-emerald-100 bg-white px-3 py-3 text-sm outline-none transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
              />
              {errors.age && <p className="mt-1 text-xs text-red-500">{errors.age.message}</p>}
            </div>
            <div>
              <label className="text-sm font-semibold text-slate-700" htmlFor="height">
                Height (cm)
              </label>
              <input
                id="height"
                type="number"
                {...register("height")}
                className="mt-2 w-full rounded-xl border border-emerald-100 bg-white px-3 py-3 text-sm outline-none transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
              />
              {errors.height && <p className="mt-1 text-xs text-red-500">{errors.height.message}</p>}
            </div>
            <div>
              <label className="text-sm font-semibold text-slate-700" htmlFor="weight">
                Weight (kg)
              </label>
              <input
                id="weight"
                type="number"
                {...register("weight")}
                className="mt-2 w-full rounded-xl border border-emerald-100 bg-white px-3 py-3 text-sm outline-none transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
              />
              {errors.weight && <p className="mt-1 text-xs text-red-500">{errors.weight.message}</p>}
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <div>
            <label className="text-sm font-semibold text-slate-700" htmlFor="goal">
              Goal
            </label>
            <select
              id="goal"
              {...register("goal")}
              className="mt-2 w-full rounded-xl border border-emerald-100 bg-white px-4 py-3 text-sm outline-none transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
            >
              <option value="weight_loss">Weight loss</option>
              <option value="maintenance">Maintenance</option>
              <option value="weight_gain">Weight gain</option>
            </select>
          </div>

          <div>
            <label className="text-sm font-semibold text-slate-700" htmlFor="activityLevel">
              Activity level
            </label>
            <select
              id="activityLevel"
              {...register("activityLevel")}
              className="mt-2 w-full rounded-xl border border-emerald-100 bg-white px-4 py-3 text-sm outline-none transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
            >
              <option value="sedentary">Sedentary</option>
              <option value="light">Light</option>
              <option value="moderate">Moderate</option>
              <option value="active">Active</option>
              <option value="very_active">Very active</option>
            </select>
          </div>

          <div>
            <label className="text-sm font-semibold text-slate-700" htmlFor="dietType">
              Diet preference
            </label>
            <select
              id="dietType"
              {...register("dietType")}
              className="mt-2 w-full rounded-xl border border-emerald-100 bg-white px-4 py-3 text-sm outline-none transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
            >
              <option value="veg">Vegetarian</option>
              <option value="non_veg">Non-vegetarian</option>
              <option value="vegan">Vegan</option>
              <option value="keto">Keto</option>
              <option value="paleo">Paleo</option>
              <option value="balanced">Balanced</option>
            </select>
          </div>

          <div>
            <label className="text-sm font-semibold text-slate-700" htmlFor="gender">
              Gender
            </label>
            <select
              id="gender"
              {...register("gender")}
              className="mt-2 w-full rounded-xl border border-emerald-100 bg-white px-4 py-3 text-sm outline-none transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
            >
              <option value="male">Male</option>
              <option value="female">Female</option>
            </select>
          </div>

          <div className="rounded-2xl bg-emerald-50 px-4 py-4 text-xs text-emerald-700">
            We keep your credentials secure using industry-standard hashing and JWT-based sessions.
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full rounded-full bg-emerald-500 py-3 text-sm font-semibold text-white shadow-lg shadow-emerald-200 transition hover:bg-emerald-600 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isSubmitting ? "Creating account..." : "Create my plan"}
          </button>

          <p className="text-xs text-slate-500">
            Already registered?{" "}
            <Link to="/login" className="font-semibold text-emerald-600 hover:text-emerald-700">
              Sign in
            </Link>
          </p>
        </div>
      </motion.form>
    </div>
  );
};

export default Register;
