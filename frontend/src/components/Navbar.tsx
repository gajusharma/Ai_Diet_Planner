import { useMemo, useState } from "react";
import { Link, NavLink, useLocation } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { Menu, X } from "lucide-react";

import { useAuth } from "@/context/AuthContext";

const navLinks = [
  { path: "/", label: "Home" },
  { path: "/dashboard", label: "Dashboard" },
  { path: "/diet-plan", label: "Diet Plan" },
  { path: "/profile", label: "Profile" },
];

const Navbar = () => {
  const { user, logout } = useAuth();
  const location = useLocation();
  const [open, setOpen] = useState(false);

  const activePath = useMemo(() => location.pathname, [location.pathname]);

  const handleNavigate = () => {
    setOpen(false);
  };

  return (
    <header className="fixed inset-x-0 top-0 z-50 border-b border-emerald-100 bg-white/80 backdrop-blur">
      <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-4 py-4">
        <Link to="/" className="flex items-center gap-2 text-lg font-semibold">
          <span className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-emerald-500 text-white shadow-lg shadow-emerald-200">
            AI
          </span>
          <span className="hidden sm:block">Smart Diet Planner</span>
        </Link>

        <nav className="hidden items-center gap-6 md:flex">
          {navLinks.map(({ path, label }) => (
            <NavLink
              key={path}
              to={path}
              className={({ isActive }) =>
                `relative text-sm font-medium transition-colors ${
                  isActive ? "text-emerald-600" : "text-slate-600 hover:text-emerald-500"
                }`
              }
            >
              {label}
              {activePath === path && (
                <motion.span
                  layoutId="active-link"
                  className="absolute inset-x-0 -bottom-1 h-0.5 rounded-full bg-emerald-500"
                />
              )}
            </NavLink>
          ))}
        </nav>

        <div className="hidden items-center gap-3 md:flex">
          {user ? (
            <>
              <span className="text-sm text-slate-600">Hi, {user.name.split(" ")[0]}</span>
              <button
                onClick={logout}
                className="rounded-full bg-emerald-500 px-5 py-2 text-sm font-semibold text-white shadow-md transition hover:bg-emerald-600"
              >
                Logout
              </button>
            </>
          ) : (
            <div className="flex gap-3">
              <Link
                to="/login"
                className="rounded-full border border-emerald-100 px-5 py-2 text-sm font-semibold text-emerald-600 transition hover:border-emerald-500"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="rounded-full bg-emerald-500 px-5 py-2 text-sm font-semibold text-white shadow-md transition hover:bg-emerald-600"
              >
                Sign Up
              </Link>
            </div>
          )}
        </div>

        <button className="md:hidden" onClick={() => setOpen((prev) => !prev)} aria-label="Toggle menu">
          {open ? <X className="h-6 w-6 text-emerald-600" /> : <Menu className="h-6 w-6 text-emerald-600" />}
        </button>
      </div>

      <AnimatePresence>
        {open && (
          <motion.nav
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="md:hidden"
          >
            <div className="space-y-2 border-t border-emerald-100 bg-white px-4 py-4">
              {navLinks.map(({ path, label }) => (
                <Link
                  key={path}
                  to={path}
                  onClick={handleNavigate}
                  className={`block rounded-lg px-4 py-3 text-sm font-semibold transition ${
                    activePath === path ? "bg-emerald-50 text-emerald-600" : "text-slate-600 hover:bg-emerald-50"
                  }`}
                >
                  {label}
                </Link>
              ))}
              <div className="flex gap-3 pt-2">
                {user ? (
                  <button
                    onClick={() => {
                      logout();
                      handleNavigate();
                    }}
                    className="flex-1 rounded-full bg-emerald-500 px-5 py-2 text-sm font-semibold text-white shadow-md transition hover:bg-emerald-600"
                  >
                    Logout
                  </button>
                ) : (
                  <>
                    <Link
                      to="/login"
                      onClick={handleNavigate}
                      className="flex-1 rounded-full border border-emerald-100 px-5 py-2 text-sm font-semibold text-emerald-600 transition hover:border-emerald-500"
                    >
                      Login
                    </Link>
                    <Link
                      to="/register"
                      onClick={handleNavigate}
                      className="flex-1 rounded-full bg-emerald-500 px-5 py-2 text-sm font-semibold text-white shadow-md transition hover:bg-emerald-600"
                    >
                      Sign Up
                    </Link>
                  </>
                )}
              </div>
            </div>
          </motion.nav>
        )}
      </AnimatePresence>
    </header>
  );
};

export default Navbar;
