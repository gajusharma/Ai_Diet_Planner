import { zodResolver } from "@hookform/resolvers/zod";
import { motion } from "framer-motion";
import { LogIn } from "lucide-react";
import { useForm } from "react-hook-form";
import { Link, useLocation } from "react-router-dom";
import { z } from "zod";

import { useAuth } from "@/context/AuthContext";

const schema = z.object({
  email: z.string().email("Enter a valid email"),
  password: z.string().min(8, "Minimum 8 characters"),
});

type LoginForm = z.infer<typeof schema>;

type LocationState = {
  from?: {
    pathname: string;
  };
};

const Login = () => {
  const { login } = useAuth();
  const location = useLocation();
  const redirectFrom = (location.state as LocationState | undefined)?.from;
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginForm>({
    resolver: zodResolver(schema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const onSubmit = async (data: LoginForm) => {
    await login(data.email, data.password);
  };

  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col justify-center gap-12 px-4 pt-16 md:flex-row md:items-center">
      <motion.div
        initial={{ opacity: 0, x: -30 }}
        animate={{ opacity: 1, x: 0 }}
        className="w-full space-y-4"
      >
        <span className="inline-flex items-center gap-2 rounded-full bg-emerald-100 px-4 py-1 text-xs font-semibold uppercase tracking-wide text-emerald-700">
          <LogIn className="h-4 w-4" /> Welcome back
        </span>
        <h2 className="text-3xl font-bold text-slate-900">Sign in to access your AI diet dashboard</h2>
        <p className="max-w-md text-sm text-slate-600">
          Track your progress, regenerate plans, and chat with the nutrition assistant to keep your goals on track.
        </p>
        <div className="rounded-3xl border border-emerald-100 bg-white/60 p-6 shadow-lg shadow-emerald-100">
          <p className="text-xs uppercase tracking-wider text-emerald-500">Need an account?</p>
          <Link to="/register" className="text-sm font-semibold text-emerald-600 hover:text-emerald-700">
            Create a new profile →
          </Link>
        </div>
      </motion.div>

      <motion.form
        onSubmit={handleSubmit(onSubmit)}
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md rounded-3xl border border-emerald-100 bg-white/80 p-8 shadow-xl shadow-emerald-100"
      >
        <h3 className="text-xl font-semibold text-slate-900">Login</h3>
  {redirectFrom && (
          <p className="mt-2 rounded-lg bg-emerald-50 p-3 text-xs text-emerald-700">
            Please sign in to continue where you left off.
          </p>
        )}

        <div className="mt-6 space-y-5">
          <div>
            <label htmlFor="email" className="text-sm font-semibold text-slate-700">
              Email address
            </label>
            <input
              id="email"
              type="email"
              autoComplete="email"
              {...register("email")}
              className="mt-2 w-full rounded-xl border border-emerald-100 bg-white px-4 py-3 text-sm outline-none transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
            />
            {errors.email && <p className="mt-1 text-xs text-red-500">{errors.email.message}</p>}
          </div>

          <div>
            <label htmlFor="password" className="text-sm font-semibold text-slate-700">
              Password
            </label>
            <input
              id="password"
              type="password"
              autoComplete="current-password"
              {...register("password")}
              className="mt-2 w-full rounded-xl border border-emerald-100 bg-white px-4 py-3 text-sm outline-none transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
            />
            {errors.password && <p className="mt-1 text-xs text-red-500">{errors.password.message}</p>}
          </div>
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className="mt-8 w-full rounded-full bg-emerald-500 py-3 text-sm font-semibold text-white shadow-lg shadow-emerald-200 transition hover:bg-emerald-600 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isSubmitting ? "Signing in..." : "Login"}
        </button>
      </motion.form>
    </div>
  );
};

export default Login;
