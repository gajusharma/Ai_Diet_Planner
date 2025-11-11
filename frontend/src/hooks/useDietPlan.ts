import { useCallback, useEffect, useState } from "react";
import { toast } from "sonner";

import { useAuth } from "@/context/AuthContext";
import api, { extractErrorMessage } from "@/utils/api";
import type { MealPlan } from "@/types/diet";

type MealPlanResponse = {
  success: boolean;
  plan: MealPlan;
};

const useDietPlan = () => {
  const [plan, setPlan] = useState<MealPlan | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user, loading: userLoading } = useAuth();

  const userId = user?._id;

  const fetchPlan = useCallback(async () => {
    if (!userId) {
      if (!userLoading) {
        setPlan(null);
        setLoading(false);
      }
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const { data } = await api.get<MealPlanResponse>(`/diet/user/${userId}`);
      setPlan(data.plan);
    } catch (err: unknown) {
      const errorMessage = extractErrorMessage(err);
      if (errorMessage.toLowerCase().includes("meal plan not found")) {
        setPlan(null);
        setError(null);
      } else {
        setError(errorMessage);
        setPlan(null);
        toast.error(errorMessage);
      }
    } finally {
      setLoading(false);
    }
  }, [userId, userLoading]);

  const generatePlan = useCallback(async () => {
    setLoading(true);
    setError(null);
    if (!userId) {
      toast.error("Please log in to generate a meal plan.");
      setLoading(false);
      return;
    }
    try {
      const { data } = await api.post<MealPlanResponse>("/diet/generate");
      setPlan(data.plan);
      toast.success("Diet plan saved successfully!");
    } catch (err: unknown) {
      const errorMessage = extractErrorMessage(err);
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [userId]);

  const regeneratePlan = useCallback(async () => {
    if (!userId) {
      toast.error("Please log in to regenerate your plan.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      await api.delete(`/diet/user/${userId}`);
      const { data } = await api.post<MealPlanResponse>("/diet/generate");
      setPlan(data.plan);
      toast.success("Your diet plan has been regenerated and saved!");
    } catch (err: unknown) {
      const errorMessage = extractErrorMessage(err);
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    fetchPlan().catch(() => {
      /* handled in fetchPlan */
    });
  }, [fetchPlan]);

  return { plan, loading, error, generatePlan, regeneratePlan, fetchPlan };
};

export default useDietPlan;
