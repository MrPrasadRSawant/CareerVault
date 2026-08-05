<template>
  <AuthLayout
    title="Welcome back"
    subtitle="Sign in to continue to CareerVault"
  >
    <LoginForm />
  </AuthLayout>
</template>

<script setup lang="ts">
import AuthLayout from "@/modules/shared/components/AuthLayout.vue";
import LoginForm from "./components/LoginForm.vue";
</script>
