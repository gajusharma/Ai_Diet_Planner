import { zodResolver } from "@hookform/resolvers/zod";
import { motion } from "framer-motion";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { toast } from "sonner";

import { useAuth, type UserProfile } from "@/context/AuthContext";
import api, { extractErrorMessage } from "@/utils/api";
import Spinner from "@/components/Spinner";

const schema = z.object({
  name: z.string().min(2, "Name is required"),
  email: z.string().email("Enter a valid email"),
  age: z.coerce.number().min(13).max(100),
  height: z.coerce.number().min(120).max(220),
  weight: z.coerce.number().min(35).max(200),
  goal: z.enum(["weight_loss", "maintenance", "weight_gain"]),
  activityLevel: z.enum(["sedentary", "light", "moderate", "active", "very_active"]),
  dietType: z.enum(["veg", "non_veg", "vegan", "keto", "paleo", "balanced"]),
  gender: z.enum(["male", "female"]),
});

type ProfileForm = z.infer<typeof schema>;

const Profile = () => {
  const { user, loading, refreshProfile } = useAuth();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting, isDirty },
  } = useForm<ProfileForm>({
    resolver: zodResolver(schema),
    values: user ?? undefined,
  });

  const onSubmit = async (data: ProfileForm) => {
    try {
      await api.put<UserProfile>("/user/me", data);
      await refreshProfile();
      toast.success("Profile updated successfully!");
    } catch (error) {
      toast.error(extractErrorMessage(error));
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <Spinner />
      </div>
    );
  }

  return (
    <div className="mx-auto w-full max-w-3xl px-4">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-bold text-slate-900">Your Profile</h1>
        <p className="mt-1 text-slate-600">
          Update your personal details and preferences. Changes will affect future diet plans.
        </p>
      </motion.div>

      <motion.form
        onSubmit={handleSubmit(onSubmit)}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="mt-8 grid gap-6 rounded-2xl border border-emerald-100 bg-white/80 p-8 shadow-lg shadow-emerald-100/50"
      >
        <div className="grid gap-6 md:grid-cols-2">
          <div className="space-y-1">
            <label className="text-sm font-semibold text-slate-700" htmlFor="name">
              Full name
            </label>
            <input
              id="name"
              {...register("name")}
              className="w-full rounded-xl border-emerald-200 bg-white shadow-sm transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
            />
            {errors.name && <p className="text-xs text-red-500">{errors.name.message}</p>}
          </div>
          <div className="space-y-1">
            <label className="text-sm font-semibold text-slate-700" htmlFor="email">
              Email address
            </label>
            <input
              id="email"
              type="email"
              {...register("email")}
              className="w-full rounded-xl border-emerald-200 bg-white shadow-sm transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
            />
            {errors.email && <p className="text-xs text-red-500">{errors.email.message}</p>}
          </div>
        </div>

        <div className="grid gap-6 md:grid-cols-3">
          <div className="space-y-1">
            <label className="text-sm font-semibold text-slate-700" htmlFor="age">
              Age
            </label>
            <input
              id="age"
              type="number"
              {...register("age")}
              className="w-full rounded-xl border-emerald-200 bg-white shadow-sm transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
            />
            {errors.age && <p className="text-xs text-red-500">{errors.age.message}</p>}
          </div>
          <div className="space-y-1">
            <label className="text-sm font-semibold text-slate-700" htmlFor="height">
              Height (cm)
            </label>
            <input
              id="height"
              type="number"
              {...register("height")}
              className="w-full rounded-xl border-emerald-200 bg-white shadow-sm transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
            />
            {errors.height && <p className="text-xs text-red-500">{errors.height.message}</p>}
          </div>
          <div className="space-y-1">
            <label className="text-sm font-semibold text-slate-700" htmlFor="weight">
              Weight (kg)
            </label>
            <input
              id="weight"
              type="number"
              {...register("weight")}
              className="w-full rounded-xl border-emerald-200 bg-white shadow-sm transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
            />
            {errors.weight && <p className="text-xs text-red-500">{errors.weight.message}</p>}
          </div>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          <div className="space-y-1">
            <label className="text-sm font-semibold text-slate-700" htmlFor="goal">
              Goal
            </label>
            <select
              id="goal"
              {...register("goal")}
              className="w-full rounded-xl border-emerald-200 bg-white shadow-sm transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
            >
              <option value="weight_loss">Weight loss</option>
              <option value="maintenance">Maintenance</option>
              <option value="weight_gain">Weight gain</option>
            </select>
          </div>
          <div className="space-y-1">
            <label className="text-sm font-semibold text-slate-700" htmlFor="activityLevel">
              Activity level
            </label>
            <select
              id="activityLevel"
              {...register("activityLevel")}
              className="w-full rounded-xl border-emerald-200 bg-white shadow-sm transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
            >
              <option value="sedentary">Sedentary</option>
              <option value="light">Light</option>
              <option value="moderate">Moderate</option>
              <option value="active">Active</option>
              <option value="very_active">Very active</option>
            </select>
          </div>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          <div className="space-y-1">
            <label className="text-sm font-semibold text-slate-700" htmlFor="dietType">
              Diet preference
            </label>
            <select
              id="dietType"
              {...register("dietType")}
              className="w-full rounded-xl border-emerald-200 bg-white shadow-sm transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
            >
              <option value="veg">Vegetarian</option>
              <option value="non_veg">Non-vegetarian</option>
              <option value="vegan">Vegan</option>
              <option value="keto">Keto</option>
              <option value="paleo">Paleo</option>
              <option value="balanced">Balanced</option>
            </select>
          </div>
          <div className="space-y-1">
            <label className="text-sm font-semibold text-slate-700" htmlFor="gender">
              Gender
            </label>
            <select
              id="gender"
              {...register("gender")}
              className="w-full rounded-xl border-emerald-200 bg-white shadow-sm transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
            >
              <option value="male">Male</option>
              <option value="female">Female</option>
            </select>
          </div>
        </div>

        <div className="mt-4 flex justify-end">
          <button
            type="submit"
            disabled={isSubmitting || !isDirty}
            className="rounded-full bg-emerald-500 px-6 py-2.5 text-sm font-semibold text-white shadow-lg shadow-emerald-200 transition hover:bg-emerald-600 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isSubmitting ? "Saving..." : "Save Changes"}
          </button>
        </div>
      </motion.form>
    </div>
  );
};

export default Profile;
