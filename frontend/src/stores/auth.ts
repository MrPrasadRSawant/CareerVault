import { computed, ref } from "vue";
import { defineStore } from "pinia";
import { authApi } from "@/api/auth";
import type { User } from "@/api/auth";

const TOKEN_KEY = "cv_token";

export const useAuthStore = defineStore("auth", () => {
  const token = ref<string | null>(localStorage.getItem(TOKEN_KEY));
  const user = ref<User | null>(null);

  const isAuthenticated = computed(() => token.value !== null);

  function setSession(accessToken: string, userData: User) {
    token.value = accessToken;
    user.value = userData;
    localStorage.setItem(TOKEN_KEY, accessToken);
  }

  async function login(email: string, password: string) {
    const data = await authApi.login(email, password);
    setSession(data.access_token, data.user);
  }

  async function register(fullName: string, email: string, password: string) {
    const data = await authApi.register(email, fullName, password);
    setSession(data.access_token, data.user);
  }

  async function loadUser() {
    if (token.value !== null && user.value === null) {
      user.value = await authApi.me();
    }
    return user.value;
  }

  function logout() {
    token.value = null;
    user.value = null;
    localStorage.removeItem(TOKEN_KEY);
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    loadUser,
    logout
  };
});
