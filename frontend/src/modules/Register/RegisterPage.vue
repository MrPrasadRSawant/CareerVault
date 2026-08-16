<template>
  <AuthLayout
    title="Create your account"
    subtitle="Start organizing your job search"
    footer-text="Your acceptance is recorded with the exact Terms version shown at registration."
  >
    <RegisterForm />
  </AuthLayout>
</template>

<script setup lang="ts">
import AuthLayout from "@/modules/shared/components/AuthLayout.vue";
import RegisterForm from "./components/RegisterForm.vue";
</script>
