import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";
import axios from "axios";

import api, { extractErrorMessage } from "@/utils/api";
import { clearToken, setToken } from "@/utils/auth";

export type UserProfile = {
  _id: string;
  name: string;
  email: string;
  age: number;
  height: number;
  weight: number;
  goal: string;
  activityLevel: string;
  dietType: string;
  gender: string;
};

type AuthContextValue = {
  user: UserProfile | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (data: RegisterPayload) => Promise<void>;
  logout: () => void;
  refreshProfile: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

const defaultProfile: Partial<UserProfile> = {
  goal: "maintenance",
  activityLevel: "moderate",
  dietType: "balanced",
  gender: "male",
};

type RegisterPayload = {
  name: string;
  email: string;
  password: string;
  age: number;
  height: number;
  weight: number;
  goal: string;
  activityLevel: string;
  dietType: string;
  gender: string;
};

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const fetchProfile = useCallback(async () => {
    try {
      const { data } = await api.get<UserProfile>("/user/me");
      setUser({ ...defaultProfile, ...data } as UserProfile);
    } catch (error) {
      // 401 is expected when not logged in, don't log as error
      if (axios.isAxiosError(error) && error.response?.status === 401) {
        console.log("User not authenticated");
      } else {
        console.error("Failed to load profile", error);
      }
      clearToken();
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchProfile().catch(() => undefined);
  }, [fetchProfile]);

  const login = useCallback(
    async (email: string, password: string) => {
      try {
        const { data } = await api.post<{ access_token: string; user: UserProfile }>(
          "/auth/login",
          { email, password }
        );
        setToken(data.access_token);
        setUser({ ...defaultProfile, ...data.user } as UserProfile);
        toast.success("Welcome back!" + (data.user.name ? `, ${data.user.name}` : ""));
        navigate("/dashboard");
      } catch (error: unknown) {
        toast.error(extractErrorMessage(error));
        throw error;
      }
    },
    [navigate]
  );

  const register = useCallback(
    async (payload: RegisterPayload) => {
      try {
        const { data } = await api.post<{ access_token: string; user: UserProfile }>(
          "/auth/register",
          payload
        );
        setToken(data.access_token);
        setUser({ ...defaultProfile, ...data.user } as UserProfile);
        toast.success("Account created! Let's build your plan.");
        navigate("/dashboard");
      } catch (error: unknown) {
        toast.error(extractErrorMessage(error));
        throw error;
      }
    },
    [navigate]
  );

  const logout = useCallback(() => {
    clearToken();
    setUser(null);
    navigate("/login");
  }, [navigate]);

  const refreshProfile = useCallback(async () => {
    setLoading(true);
    await fetchProfile();
  }, [fetchProfile]);

  const value = useMemo(
    () => ({ user, loading, login, register, logout, refreshProfile }),
    [user, loading, login, register, logout, refreshProfile]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
