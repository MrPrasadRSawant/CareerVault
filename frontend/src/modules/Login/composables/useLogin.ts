import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useQuasar } from "quasar";
import { axios } from "@/api/client";
import { authApi } from "@/api/auth";
import { useAuthStore } from "@/stores/auth";

export function useLogin() {
  const auth = useAuthStore();
  const router = useRouter();
  const route = useRoute();
  const $q = useQuasar();

  const email = ref("");
  const password = ref("");
  const submitting = ref(false);
  const passwordMinimumLength = ref(8);
  const passwordMaximumLength = ref(20);

  const canSubmit = computed(
    () =>
      email.value.trim().length > 0 &&
      password.value.length >= passwordMinimumLength.value &&
      password.value.length <= passwordMaximumLength.value &&
      !submitting.value
  );

  function isRequired(value: string | null) {
    return (value ?? "").trim().length > 0 || "This field is required";
  }

  function isEmail(value: string | null) {
    return (
      /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value ?? "") || "Enter a valid email"
    );
  }

  function passwordLength(value: string | null) {
    const length = (value ?? "").length;
    return (
      (length >= passwordMinimumLength.value &&
        length <= passwordMaximumLength.value) ||
      `Password must contain ${passwordMinimumLength.value}–${passwordMaximumLength.value} characters`
    );
  }

  async function onSubmit() {
    submitting.value = true;
    try {
      await auth.login(email.value, password.value);
      const requestedRedirect =
        typeof route.query.redirect === "string"
          ? route.query.redirect
          : undefined;
      const redirect =
        auth.role === "system_admin"
          ? requestedRedirect?.startsWith("/system-admin")
            ? requestedRedirect
            : "/system-admin/overview"
          : requestedRedirect !== undefined &&
              !requestedRedirect.startsWith("/system-admin")
            ? requestedRedirect
            : "/dashboard";
      await router.push(redirect);
    } catch (error: unknown) {
      const detail = axios.isAxiosError(error)
        ? error.response?.data?.detail
        : null;
      $q.notify({
        type: "negative",
        message:
          typeof detail === "string" ? detail : "Incorrect email or password"
      });
    } finally {
      submitting.value = false;
    }
  }

  function onReset() {
    email.value = "";
    password.value = "";
  }

  onMounted(async () => {
    try {
      const policy = await authApi.passwordPolicy();
      passwordMinimumLength.value = policy.minimum_length;
      passwordMaximumLength.value = policy.maximum_length;
    } catch {
      // Keep the secure database defaults when the policy request is unavailable.
    }
  });

  return {
    email,
    password,
    submitting,
    canSubmit,
    isRequired,
    isEmail,
    passwordLength,
    passwordMinimumLength,
    passwordMaximumLength,
    onSubmit,
    onReset
  };
}
