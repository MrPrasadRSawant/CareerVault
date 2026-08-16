import axios from "axios";

function defaultApiBaseUrl(): string {
  return "/api/v1";
}

const api = axios.create({
  baseURL:
    (import.meta.env.VITE_API_URL as string | undefined) || defaultApiBaseUrl()
});

api.interceptors.request.use(config => {
  const token = localStorage.getItem("cv_token");
  if (token !== null) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  response => response,
  error => {
    if (
      error?.response?.status === 401 &&
      error?.config?.url !== "/auth/login" &&
      error?.config?.url !== "/auth/register"
    ) {
      localStorage.removeItem("cv_token");
      const adminContext =
        localStorage.getItem("cv_role") === "system_admin" ||
        window.location.pathname.startsWith("/system-admin");
      localStorage.removeItem("cv_role");
      const redirect = adminContext
        ? `/login?redirect=${encodeURIComponent("/system-admin/overview")}`
        : "/login";
      window.location.assign(redirect);
    }
    return Promise.reject(error);
  }
);

export { api, axios };
