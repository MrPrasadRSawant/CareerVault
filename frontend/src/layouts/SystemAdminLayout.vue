<template>
  <q-layout view="hHh Lpr lFf">
    <q-header class="admin-header">
      <q-toolbar class="admin-toolbar">
        <q-btn
          flat
          round
          dense
          icon="menu"
          class="drawer-toggle"
          aria-label="Toggle administration navigation"
          @click="drawerOpen = !drawerOpen"
        />
        <router-link
          :to="{ name: 'system-admin-overview' }"
          class="admin-brand"
        >
          <span class="admin-brand-mark">CV</span>
          <span class="admin-brand-name">Career<span>Vault</span></span>
          <span class="admin-brand-divider"></span>
          <span class="admin-product-label">Control Center</span>
        </router-link>

        <q-space />

        <div class="admin-access-badge q-hide-xs">
          <q-icon name="verified_user" size="15px" />
          System administrator
        </div>
        <q-btn-dropdown flat no-caps class="admin-user-menu">
          <template #label>
            <div class="admin-user-chip">
              <UserInitialsAvatar
                :name="auth.user?.full_name || 'System Admin'"
                size="34px"
                font-size="11px"
                variant="solid"
              />
              <div class="q-hide-sm-and-down">
                <div class="admin-user-name">{{ auth.user?.full_name }}</div>
                <div class="admin-user-role">Product owner</div>
              </div>
            </div>
          </template>
          <q-list padding class="admin-profile-menu">
            <q-item class="admin-profile-header">
              <q-item-section avatar>
                <UserInitialsAvatar
                  :name="auth.user?.full_name || 'System Admin'"
                  size="42px"
                  font-size="12px"
                  variant="solid"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-bold">{{
                  auth.user?.full_name
                }}</q-item-label>
                <q-item-label caption>{{ auth.user?.email }}</q-item-label>
              </q-item-section>
            </q-item>
            <q-separator spaced />
            <q-item clickable v-close-popup class="logout-item" @click="logout">
              <q-item-section avatar><q-icon name="logout" /></q-item-section>
              <q-item-section>Sign out</q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="drawerOpen"
      show-if-above
      bordered
      :width="238"
      :breakpoint="900"
      class="admin-drawer"
    >
      <div class="drawer-content">
        <div class="drawer-context">
          <div class="drawer-context-icon"
            ><q-icon name="admin_panel_settings"
          /></div>
          <div>
            <div class="drawer-context-title">Administration</div>
            <div class="drawer-context-copy">Platform operations</div>
          </div>
        </div>

        <q-list padding class="admin-nav">
          <q-item-label header>Workspace</q-item-label>
          <q-item
            v-for="item in navItems"
            :key="item.name"
            clickable
            v-ripple
            exact
            :to="item.to"
            :active="route.name === item.name"
            active-class="admin-nav-item--active"
            class="admin-nav-item"
          >
            <q-item-section avatar><q-icon :name="item.icon" /></q-item-section>
            <q-item-section>{{ item.label }}</q-item-section>
          </q-item>
        </q-list>

        <div class="drawer-security">
          <q-icon name="shield" size="18px" />
          <div>
            <strong>Account administration</strong>
            <span>Career data stays private</span>
          </div>
        </div>
      </div>
    </q-drawer>

    <q-page-container class="admin-page-container"
      ><router-view
    /></q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import UserInitialsAvatar from "@/modules/SystemAdmin/components/UserInitialsAvatar.vue";

defineOptions({ name: "SystemAdminLayout" });

const auth = useAuthStore();
const route = useRoute();
const router = useRouter();
const drawerOpen = ref(false);
const navItems = [
  {
    name: "system-admin-overview",
    label: "Overview",
    icon: "dashboard",
    to: "/system-admin/overview"
  },
  {
    name: "system-admin-users",
    label: "Users",
    icon: "group",
    to: "/system-admin/users"
  },
  {
    name: "system-admin-login-activity",
    label: "Login activity",
    icon: "policy",
    to: "/system-admin/login-activity"
  },
  {
    name: "system-admin-settings",
    label: "Platform settings",
    icon: "tune",
    to: "/system-admin/settings"
  },
  {
    name: "system-admin-exception-logs",
    label: "Exception logs",
    icon: "bug_report",
    to: "/system-admin/exception-logs"
  }
];

onMounted(async () => {
  try {
    await auth.loadUser();
  } catch {
    await auth.logout();
    await router.replace({
      name: "login",
      query: { redirect: "/system-admin/overview" }
    });
  }
});

async function logout() {
  await auth.logout();
  await router.replace({ name: "login" });
}
</script>

<style lang="scss" scoped>
.admin-header {
  color: #263449;
  background: rgba(255, 255, 255, 0.98);
  border-bottom: 1px solid #e1e6ec;
  box-shadow: 0 1px 3px rgba(30, 42, 56, 0.04);
}
.admin-toolbar {
  min-height: 64px;
  padding: 0 20px;
  gap: 10px;
}
.drawer-toggle {
  display: none;
  color: #5f6d80;
}
.admin-brand {
  display: flex;
  align-items: center;
  gap: 9px;
  color: #172033;
  text-decoration: none;
}
.admin-brand-mark {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  border-radius: 8px;
  color: #fff;
  background: #1769e0;
  box-shadow: 0 5px 14px rgba(23, 105, 224, 0.2);
  font-size: 12px;
  font-weight: 900;
}
.admin-brand-name {
  font-size: 18px;
  font-weight: 800;
  letter-spacing: -0.4px;
}
.admin-brand-name span {
  color: #1769e0;
}
.admin-brand-divider {
  width: 1px;
  height: 22px;
  margin-left: 3px;
  background: #dce2e9;
}
.admin-product-label {
  color: #7d8898;
  font-size: 12px;
  font-weight: 650;
}
.admin-access-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  border-radius: 999px;
  color: #1769e0;
  background: #edf4ff;
  font-size: 10.5px;
  font-weight: 700;
}
.admin-user-menu {
  margin-left: 2px;
  border-radius: 22px;
}
.admin-user-chip {
  display: flex;
  align-items: center;
  gap: 9px;
}
.admin-user-name {
  max-width: 150px;
  overflow: hidden;
  color: #29364a;
  font-size: 12px;
  font-weight: 700;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.admin-user-role {
  color: #8d97a6;
  font-size: 10px;
}
.admin-profile-menu {
  min-width: 285px;
}
.admin-profile-header {
  padding: 11px;
  border-radius: 9px;
  background: #f6f8fb;
}
.logout-item {
  min-height: 48px;
  border-radius: 8px;
  color: #b52f3a;
}
.logout-item:hover {
  background: #fff2f3;
}
.admin-drawer {
  background: #fff;
}
.drawer-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}
.drawer-context {
  display: flex;
  align-items: center;
  gap: 11px;
  margin: 16px 14px 8px;
  padding: 13px;
  border-radius: 11px;
  background: #f4f7fb;
}
.drawer-context-icon {
  display: grid;
  place-items: center;
  width: 37px;
  height: 37px;
  border-radius: 9px;
  color: #1769e0;
  background: #e6efff;
  font-size: 20px;
}
.drawer-context-title {
  color: #253247;
  font-size: 12.5px;
  font-weight: 750;
}
.drawer-context-copy {
  color: #8a95a5;
  font-size: 10.5px;
}
.admin-nav {
  flex: 1;
}
.admin-nav :deep(.q-item__label--header) {
  color: #9aa3b1;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.75px;
  text-transform: uppercase;
}
.admin-nav-item {
  min-height: 48px;
  margin: 3px 10px;
  border-radius: 9px;
  color: #566377;
  font-weight: 600;
}
.admin-nav-item:hover {
  background: #f5f8fc;
}
.admin-nav-item :deep(.q-item__section--avatar) {
  min-width: 38px;
  color: #7d8999;
}
.admin-nav-item--active {
  color: #1769e0;
  background: #edf4ff;
}
.admin-nav-item--active :deep(.q-item__section--avatar) {
  color: #1769e0;
}
.drawer-security {
  display: flex;
  gap: 9px;
  margin: 14px;
  padding: 12px;
  border: 1px solid #e4e9ef;
  border-radius: 10px;
  color: #6e7a8c;
  background: #fafbfc;
}
.drawer-security .q-icon {
  color: #22a06b;
}
.drawer-security strong,
.drawer-security span {
  display: block;
}
.drawer-security strong {
  color: #445166;
  font-size: 10.5px;
}
.drawer-security span {
  margin-top: 2px;
  font-size: 9.5px;
}
.admin-page-container {
  background: #f3f5f7;
}

@media (max-width: 899px) {
  .drawer-toggle {
    display: inline-flex;
  }
  .admin-brand-divider,
  .admin-product-label {
    display: none;
  }
}

@media (max-width: 520px) {
  .admin-toolbar {
    padding: 0 10px;
  }
  .admin-brand-name {
    font-size: 16px;
  }
}
</style>
