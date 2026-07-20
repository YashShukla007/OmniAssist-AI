import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("omniassist_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("omniassist_token");
      sessionStorage.removeItem("omniassist_role");
      sessionStorage.removeItem("omniassist_username");
      if (!window.location.hash.includes("/login")) window.location.hash = "#/login";
    }
    return Promise.reject(error);
  },
);

export default api;
