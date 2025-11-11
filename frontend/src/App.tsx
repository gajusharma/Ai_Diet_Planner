import { Navigate, Route, Routes } from "react-router-dom";

import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";
import ChatBotWidget from "./components/ChatBotWidget";
import Dashboard from "./pages/Dashboard";
import DietPlan from "./pages/DietPlan";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Profile from "./pages/Profile";
import Register from "./pages/Register";

const App = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-lime-100 text-slate-900">
      <Navbar />
      <main className="pt-20 pb-12">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/diet-plan"
            element={
              <ProtectedRoute>
                <DietPlan />
              </ProtectedRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </main>
      <ChatBotWidget />
    </div>
  );
};

export default App;
