import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import { useQuasar } from "quasar";
import { useAuthStore } from "@/stores/auth";
import { axios } from "@/api/client";

export function useRegister() {
  const auth = useAuthStore();
  const router = useRouter();
  const $q = useQuasar();

  const fullName = ref("");
  const email = ref("");
  const password = ref("");
  const confirmPassword = ref("");
  const submitting = ref(false);

  const canSubmit = computed(
    () =>
      fullName.value.trim().length > 0 &&
      email.value.trim().length > 0 &&
      password.value.length >= 8 &&
      confirmPassword.value.length > 0 &&
      password.value === confirmPassword.value &&
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

  function minLength(value: string | null) {
    return (
      (value ?? "").length >= 8 || "Password must be at least 8 characters"
    );
  }

  function passwordMatches(value: string | null) {
    return value === password.value || "Passwords do not match";
  }

  async function onSubmit() {
    submitting.value = true;
    try {
      await auth.register(fullName.value.trim(), email.value, password.value);
      $q.notify({
        type: "positive",
        message: "Account created. Welcome to CareerVault!"
      });
      await router.push("/dashboard");
    } catch (error: unknown) {
      const detail = axios.isAxiosError(error)
        ? error.response?.data?.detail
        : null;
      $q.notify({
        type: "negative",
        message:
          typeof detail === "string"
            ? detail
            : "We could not create your account. Please try again."
      });
    } finally {
      submitting.value = false;
    }
  }

  function onReset() {
    fullName.value = "";
    email.value = "";
    password.value = "";
    confirmPassword.value = "";
  }

  return {
    fullName,
    email,
    password,
    confirmPassword,
    submitting,
    canSubmit,
    isRequired,
    isEmail,
    minLength,
    passwordMatches,
    onSubmit,
    onReset
  };
}
