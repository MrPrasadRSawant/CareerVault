<template>
  <q-layout view="hHh Lpr lFf">
    <q-header elevated class="app-header">
      <q-toolbar class="app-toolbar">
        <q-btn
          flat
          round
          dense
          icon="menu"
          color="white"
          aria-label="Menu"
          class="header-hamburger"
          @click="toggleLeftDrawer"
        />

        <div
          class="toolbar-brand"
          role="link"
          tabindex="0"
          @click="goDashboard"
        >
          <div class="toolbar-brand-mark">
            <q-icon name="rocket_launch" size="18px" />
          </div>
          <span>Career<span class="brand-accent">Vault</span></span>
        </div>

        <q-space class="gt-md" />

        <nav class="header-nav" aria-label="Primary">
          <q-btn
            flat
            no-caps
            :class="{ 'nav-trigger--active': isActive('dashboard') }"
            class="nav-trigger"
            icon="dashboard"
            label="Dashboard"
            to="/dashboard"
          />

          <q-btn-dropdown
            v-for="group in navGroups"
            :key="group.label"
            flat
            no-caps
            :icon="group.icon"
            :label="group.label"
            :class="{ 'nav-trigger--active': isGroupActive(group) }"
            class="nav-trigger nav-dropdown"
            content-class="nav-menu"
          >
            <q-list padding>
              <q-item
                v-for="item in group.items"
                :key="item.name"
                clickable
                v-ripple
                :to="item.to"
                :active="isActive(item.name)"
                active-class="nav-item--active"
                class="nav-item"
                exact
              >
                <q-item-section avatar>
                  <q-icon :name="item.icon" />
                </q-item-section>
                <q-item-section>{{ item.label }}</q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </nav>

        <template v-if="auth.user">
          <q-btn-dropdown
            flat
            no-caps
            class="user-menu"
            content-class="nav-menu user-menu-card"
          >
            <template #label>
              <div class="user-chip">
                <q-avatar
                  icon="person"
                  size="30px"
                  color="primary"
                  text-color="white"
                />
                <div class="user-chip-text q-hide-sm-and-down">
                  <div class="user-name">{{ auth.user.full_name }}</div>
                  <div class="user-email">{{ auth.user.email }}</div>
                </div>
                <q-icon name="arrow_drop_down" size="18px" class="user-caret" />
              </div>
            </template>

            <q-list padding>
              <q-item class="user-menu-header">
                <q-item-section>
                  <q-item-label class="user-menu-name">
                    {{ auth.user.full_name }}
                  </q-item-label>
                  <q-item-label caption class="user-menu-email">
                    {{ auth.user.email }}
                  </q-item-label>
                </q-item-section>
              </q-item>

              <q-separator spaced />

              <q-item clickable v-ripple @click="onLogout">
                <q-item-section avatar>
                  <q-icon name="logout" />
                </q-item-section>
                <q-item-section>Logout</q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </template>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      class="app-drawer"
      :width="240"
      :breakpoint="767"
      overlay
    >
      <div class="drawer-brand">
        <div class="drawer-brand-mark">
          <q-icon name="rocket_launch" size="16px" />
        </div>
        <span>Career<span class="brand-accent">Vault</span></span>
      </div>

      <q-scroll-area class="drawer-scroll">
        <q-list padding>
          <q-item-label header class="drawer-section-label">
            Menu
          </q-item-label>

          <q-item
            v-for="item in dashboardItems"
            :key="item.name"
            clickable
            v-ripple
            :to="item.to"
            :active="isActive(item.name)"
            active-class="menu-item--active"
            class="menu-item"
            exact
            @click="leftDrawerOpen = false"
          >
            <q-item-section avatar>
              <q-icon :name="item.icon" />
            </q-item-section>
            <q-item-section>
              {{ item.label }}
            </q-item-section>
          </q-item>

          <template v-for="group in navGroups" :key="group.label">
            <q-item-label header class="drawer-section-label">
              {{ group.label }}
            </q-item-label>

            <q-item
              v-for="item in group.items"
              :key="item.name"
              clickable
              v-ripple
              :to="item.to"
              :active="isActive(item.name)"
              active-class="menu-item--active"
              class="menu-item"
              exact
              @click="leftDrawerOpen = false"
            >
              <q-item-section avatar>
                <q-icon :name="item.icon" />
              </q-item-section>
              <q-item-section>
                {{ item.label }}
              </q-item-section>
            </q-item>
          </template>
        </q-list>
      </q-scroll-area>

      <div class="drawer-footer">
        <q-icon name="copyright" size="14px" />
        {{ currentYear }} CareerVault
      </div>
    </q-drawer>

    <q-page-container class="page-container">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

interface NavItem {
  name: string;
  label: string;
  icon: string;
  to: string;
}

interface NavGroup {
  label: string;
  icon: string;
  items: NavItem[];
}

const auth = useAuthStore();
const router = useRouter();
const route = useRoute();

const currentYear = new Date().getFullYear();
const leftDrawerOpen = ref(false);

const navGroups: NavGroup[] = [
  {
    label: "Job Search",
    icon: "work",
    items: [
      {
        name: "opportunities",
        label: "Opportunities",
        icon: "work",
        to: "/opportunities"
      },
      {
        name: "applications",
        label: "Applications",
        icon: "assignment",
        to: "/applications"
      },
      {
        name: "companies",
        label: "Companies",
        icon: "business",
        to: "/companies"
      }
    ]
  },
  {
    label: "Documents",
    icon: "folder_open",
    items: [
      {
        name: "resumes",
        label: "Resume",
        icon: "description",
        to: "/resumes"
      },
      {
        name: "cover-letters",
        label: "Cover Letters",
        icon: "article",
        to: "/cover-letters"
      }
    ]
  }
];

const dashboardItems: NavItem[] = [
  {
    name: "dashboard",
    label: "Dashboard",
    icon: "dashboard",
    to: "/dashboard"
  }
];

function isActive(name: string): boolean {
  return route.name === name;
}

function isGroupActive(group: NavGroup): boolean {
  return group.items.some(item => isActive(item.name));
}

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}

function goDashboard() {
  if (!isActive("dashboard")) {
    void router.push({ name: "dashboard" });
  }
}

onMounted(() => {
  void auth.loadUser();
});

function onLogout() {
  auth.logout();
  void router.push({ name: "login" });
}
</script>

<style lang="scss" scoped>
.app-header {
  background: #023047;
}

@media (min-width: 1024px) {
  .header-hamburger {
    display: none !important;
  }
}

@media (max-width: 1023px) {
  .header-nav {
    display: none !important;
  }
}

.app-toolbar {
  min-height: 60px;
  gap: 4px;
}

.toolbar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.2px;
  cursor: pointer;
  user-select: none;
  padding: 4px 8px;
  border-radius: 10px;

  &:hover {
    background: rgba(142, 202, 230, 0.1);
  }
}

.toolbar-brand-mark {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 10px;
  color: #fff;
  background: linear-gradient(135deg, #219ebc 0%, #8ecae6 100%);
  box-shadow: 0 4px 12px rgba(33, 158, 188, 0.4);
}

.brand-accent {
  color: #ffb703;
}

.header-nav {
  display: flex;
  align-items: center;
  gap: 2px;
  margin-left: 16px;
}

.nav-trigger {
  color: #cfe3ec;
  font-weight: 500;
  border-radius: 8px;
  padding: 0 10px;

  &:hover {
    background: rgba(142, 202, 230, 0.14);
    color: #fff;
  }
}

.nav-trigger--active {
  color: #fff;
  background: rgba(33, 158, 188, 0.28);

  :deep(.q-icon) {
    color: #8ecae6;
  }
}

.nav-dropdown :deep(.q-btn-dropdown__arrow) {
  color: inherit;
}

.nav-menu {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 30px rgba(2, 48, 71, 0.18);
}

.nav-item {
  border-radius: 8px;
  margin: 2px 8px;
  font-weight: 500;
  color: #334e5a;

  &:hover {
    background: rgba(33, 158, 188, 0.08);
  }

  .q-icon {
    color: #6b8a99;
  }
}

.nav-item--active {
  background: rgba(33, 158, 188, 0.14);
  color: #0b7285;

  .q-icon {
    color: #219ebc;
  }
}

.user-menu {
  border-radius: 12px;
  margin-left: 8px;
}

.user-chip {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 4px 6px 4px 4px;
  border-radius: 12px;
  background: rgba(142, 202, 230, 0.14);
  border: 1px solid rgba(142, 202, 230, 0.18);

  &:hover {
    background: rgba(142, 202, 230, 0.22);
  }
}

.user-chip-text {
  text-align: left;
}

.user-name {
  font-size: 13px;
  font-weight: 600;
  color: #fff;
  line-height: 1.25;
}

.user-email {
  font-size: 11px;
  color: #8ecae6;
  line-height: 1.25;
}

.user-caret {
  color: #8ecae6;
}

.user-menu-card {
  min-width: 240px;
}

.user-menu-header {
  background: #f6fafc;
  border-radius: 10px;
}

.user-menu-name {
  font-weight: 600;
  color: #023047;
}

.user-menu-email {
  color: #6b8a99;
}

.app-drawer {
  background: #023047;
  display: flex;
  flex-direction: column;
}

.drawer-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 18px 20px;
  font-size: 16px;
  font-weight: 700;
  color: #fff;
  border-bottom: 1px solid rgba(142, 202, 230, 0.12);
}

.drawer-brand-mark {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 9px;
  color: #fff;
  background: linear-gradient(135deg, #219ebc 0%, #8ecae6 100%);
}

.drawer-scroll {
  flex: 1;
}

.drawer-section-label {
  color: #6f93a3;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.menu-item {
  color: #b9d5df;
  border-radius: 10px;
  margin: 2px 10px;
  font-weight: 500;

  &:hover {
    background: rgba(142, 202, 230, 0.12);
  }
}

.menu-item--active {
  background: rgba(33, 158, 188, 0.3);
  color: #fff;

  .q-icon {
    color: #8ecae6;
  }
}

.drawer-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 14px;
  font-size: 12px;
  color: #6f93a3;
  border-top: 1px solid rgba(142, 202, 230, 0.12);
}

.page-container {
  background: #f8fafc;
}
</style>
