import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useQuasar } from "quasar";
import { useAuthStore } from "@/stores/auth";
import { axios } from "@/api/client";
import { authApi } from "@/api/auth";
import { legalApi } from "@/api/legal";

export function useRegister() {
  const auth = useAuthStore();
  const router = useRouter();
  const $q = useQuasar();

  const fullName = ref("");
  const email = ref("");
  const password = ref("");
  const confirmPassword = ref("");
  const termsAccepted = ref(false);
  const termsVersion = ref<number | null>(null);
  const termsLoading = ref(true);
  const submitting = ref(false);
  const passwordMinimumLength = ref(8);
  const passwordMaximumLength = ref(20);

  const canSubmit = computed(
    () =>
      fullName.value.trim().length > 0 &&
      email.value.trim().length > 0 &&
      password.value.length >= passwordMinimumLength.value &&
      password.value.length <= passwordMaximumLength.value &&
      confirmPassword.value.length > 0 &&
      password.value === confirmPassword.value &&
      termsAccepted.value &&
      termsVersion.value !== null &&
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

  function passwordMatches(value: string | null) {
    return value === password.value || "Passwords do not match";
  }

  async function onSubmit() {
    if (!termsAccepted.value || termsVersion.value === null) return;
    submitting.value = true;
    try {
      await auth.register(
        fullName.value.trim(),
        email.value,
        password.value,
        termsVersion.value
      );
      $q.notify({
        type: "positive",
        message: "Account created. Welcome to CareerVault!"
      });
      await router.push("/dashboard");
    } catch (error: unknown) {
      const detail = axios.isAxiosError(error)
        ? error.response?.data?.detail
        : null;
      if (axios.isAxiosError(error) && error.response?.status === 409) {
        try {
          const latestTerms = await legalApi.termsOfService();
          termsVersion.value = latestTerms.version;
          termsAccepted.value = false;
        } catch {
          termsVersion.value = null;
        }
      }
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
    termsAccepted.value = false;
  }

  onMounted(async () => {
    try {
      const [policy, terms] = await Promise.all([
        authApi.passwordPolicy(),
        legalApi.termsOfService()
      ]);
      passwordMinimumLength.value = policy.minimum_length;
      passwordMaximumLength.value = policy.maximum_length;
      termsVersion.value = terms.version;
    } catch {
      $q.notify({
        type: "negative",
        message: "Registration details could not be loaded. Please try again."
      });
    } finally {
      termsLoading.value = false;
    }
  });

  return {
    fullName,
    email,
    password,
    confirmPassword,
    termsAccepted,
    termsLoading,
    submitting,
    canSubmit,
    isRequired,
    isEmail,
    passwordLength,
    passwordMinimumLength,
    passwordMaximumLength,
    passwordMatches,
    onSubmit,
    onReset
  };
}
