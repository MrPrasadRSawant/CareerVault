<template>
  <q-avatar
    :size="size"
    class="account-avatar"
    :class="{ 'account-avatar--solid': variant === 'solid' }"
    :aria-label="`${name} initials`"
  >
    <span class="avatar-initials">{{ initials }}</span>
  </q-avatar>
</template>

<script setup lang="ts">
import { computed } from "vue";

defineOptions({ name: "UserInitialsAvatar" });

const props = withDefaults(
  defineProps<{
    name: string;
    size?: string;
    fontSize?: string;
    variant?: "soft" | "solid";
  }>(),
  {
    size: "40px",
    fontSize: "11px",
    variant: "soft"
  }
);

const initials = computed(() =>
  props.name
    .trim()
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map(part => part.charAt(0))
    .join("")
    .toUpperCase()
);
</script>

<style lang="scss" scoped>
.account-avatar {
  flex: 0 0 auto;
  color: #1769e0;
  background: #e9f1ff;
}

.account-avatar--solid {
  color: #fff;
  background: linear-gradient(135deg, #1769e0, #635bdf);
  box-shadow: 0 4px 10px rgba(23, 105, 224, 0.2);
}

.avatar-initials {
  display: grid;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  font-size: v-bind(fontSize);
  font-weight: 800;
  line-height: 1;
  letter-spacing: 0.25px;
  text-align: center;
  white-space: nowrap;
}
</style>
