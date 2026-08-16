import { computed, ref } from "vue";
import { defineStore } from "pinia";
import { authApi } from "@/api/auth";
import { adminApi } from "@/api/admin";
import type { User, UserRole } from "@/api/auth";

const TOKEN_KEY = "cv_token";
const ROLE_KEY = "cv_role";

function storedRole(): UserRole | null {
  const value = localStorage.getItem(ROLE_KEY);
  return value === "job_applicant" || value === "system_admin" ? value : null;
}

export const useAuthStore = defineStore("auth", () => {
  const token = ref<string | null>(localStorage.getItem(TOKEN_KEY));
  const user = ref<User | null>(null);
  const role = ref<UserRole | null>(storedRole());

  const isAuthenticated = computed(() => token.value !== null);
  const isSystemAdmin = computed(() => role.value === "system_admin");
  const isJobApplicant = computed(() => role.value === "job_applicant");

  function setSession(accessToken: string, userData: User) {
    token.value = accessToken;
    user.value = userData;
    role.value = userData.role;
    localStorage.setItem(TOKEN_KEY, accessToken);
    localStorage.setItem(ROLE_KEY, userData.role);
  }

  async function login(email: string, password: string) {
    const data = await authApi.login(email, password);
    setSession(data.access_token, data.user);
  }

  async function register(
    fullName: string,
    email: string,
    password: string,
    termsVersion: number
  ) {
    const data = await authApi.register(
      email,
      fullName,
      password,
      termsVersion
    );
    setSession(data.access_token, data.user);
  }

  async function loadUser() {
    if (token.value !== null && user.value === null) {
      const userData =
        role.value === "system_admin"
          ? await adminApi.me()
          : await authApi.me();
      user.value = userData;
      role.value = userData.role;
      localStorage.setItem(ROLE_KEY, userData.role);
    }
    return user.value;
  }

  async function logout() {
    try {
      if (token.value !== null) await authApi.logout();
    } finally {
      token.value = null;
      user.value = null;
      role.value = null;
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(ROLE_KEY);
    }
  }

  return {
    token,
    user,
    role,
    isAuthenticated,
    isSystemAdmin,
    isJobApplicant,
    login,
    register,
    loadUser,
    logout
  };
});
