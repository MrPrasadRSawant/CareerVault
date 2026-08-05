import { computed, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useQuasar } from "quasar";
import { useAuthStore } from "@/stores/auth";

export function useLogin() {
  const auth = useAuthStore();
  const router = useRouter();
  const route = useRoute();
  const $q = useQuasar();

  const email = ref("");
  const password = ref("");
  const submitting = ref(false);

  const canSubmit = computed(
    () =>
      email.value.trim().length > 0 &&
      password.value.trim().length > 0 &&
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

  async function onSubmit() {
    submitting.value = true;
    try {
      await auth.login(email.value, password.value);
      const redirect =
        typeof route.query.redirect === "string"
          ? route.query.redirect
          : "/dashboard";
      await router.push(redirect);
    } catch {
      $q.notify({
        type: "negative",
        message: "Incorrect email or password"
      });
    } finally {
      submitting.value = false;
    }
  }

  function onReset() {
    email.value = "";
    password.value = "";
  }

  return {
    email,
    password,
    submitting,
    canSubmit,
    isRequired,
    isEmail,
    onSubmit,
    onReset
  };
}
