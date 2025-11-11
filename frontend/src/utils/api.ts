import type { AxiosError, AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from "axios";
import axios from "axios";

import { getToken, clearToken } from "./auth";

const createApiClient = (): AxiosInstance =>
  axios.create({
    baseURL: import.meta.env.VITE_API_URL ?? "http://localhost:8000",
    headers: {
      "Content-Type": "application/json",
    },
  });

const api = createApiClient();

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = getToken();
  if (token) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      clearToken();
    }
    return Promise.reject(error);
  }
);

type ErrorResponse = {
  detail?: string;
  message?: string;
};

export const extractErrorMessage = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<ErrorResponse | string | undefined>;
    const responseData = axiosError.response?.data;

    if (typeof responseData === "string") {
      return responseData;
    }

    if (responseData?.detail) {
      return responseData.detail;
    }

    if (responseData?.message) {
      return responseData.message;
    }

    return axiosError.message;
  }

  if (error instanceof Error) {
    return error.message;
  }

  return "Something went wrong";
};

export default api;
