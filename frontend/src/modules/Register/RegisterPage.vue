<template>
  <AuthLayout
    title="Create your account"
    subtitle="Start organizing your job search"
    footer-text="By creating an account you agree to the Terms of Service and Privacy Policy."
  >
    <RegisterForm />
  </AuthLayout>
</template>

<script setup lang="ts">
import AuthLayout from "@/modules/shared/components/AuthLayout.vue";
import RegisterForm from "./components/RegisterForm.vue";
</script>
