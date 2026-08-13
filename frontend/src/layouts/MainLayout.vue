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
          aria-label="Open navigation menu"
          aria-controls="mobile-navigation-drawer"
          :aria-expanded="leftDrawerOpen"
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

        <q-space />

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
            aria-label="Open profile menu"
          >
            <template #label>
              <div class="user-chip">
                <div class="user-avatar-wrap">
                  <q-avatar
                    icon="person"
                    size="30px"
                    color="primary"
                    text-color="white"
                  />
                  <q-badge
                    v-if="notificationStore.unseenCount > 0"
                    rounded
                    color="negative"
                    class="profile-notification-badge"
                    :label="notificationStore.badgeLabel"
                  />
                </div>
                <div class="user-chip-text q-hide-sm-and-down">
                  <div class="user-name">{{ auth.user.full_name }}</div>
                  <div class="user-email">{{ auth.user.email }}</div>
                </div>
                <q-icon name="arrow_drop_down" size="18px" class="user-caret" />
              </div>
            </template>

            <q-list padding>
              <q-item class="user-menu-header">
                <q-item-section avatar>
                  <q-avatar size="42px" class="profile-avatar">{{ userInitials }}</q-avatar>
                </q-item-section>
                <q-item-section>
                  <q-item-label class="user-menu-name">
                    {{ auth.user.full_name }}
                  </q-item-label>
                  <q-item-label caption class="user-menu-email">
                    {{ auth.user.email }}
                  </q-item-label>
                  <q-item-label caption class="user-menu-account">Personal account</q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-icon name="verified_user" color="positive" size="18px" />
                </q-item-section>
              </q-item>

              <q-separator spaced />

              <q-item clickable v-ripple to="/notifications" exact class="profile-menu-item">
                <q-item-section avatar>
                  <q-icon name="notifications" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>Notifications</q-item-label>
                  <q-item-label caption>
                    {{ notificationCaption }}
                  </q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-badge
                    v-if="notificationStore.unseenCount > 0"
                    rounded
                    color="negative"
                    :label="notificationStore.badgeLabel"
                  />
                  <q-icon v-else name="chevron_right" size="18px" />
                </q-item-section>
              </q-item>

              <q-item clickable v-ripple to="/settings" exact class="profile-menu-item">
                <q-item-section avatar>
                  <q-icon name="settings" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>Settings</q-item-label>
                  <q-item-label caption>API keys and automation APIs</q-item-label>
                </q-item-section>
                <q-item-section side><q-icon name="chevron_right" size="18px" /></q-item-section>
              </q-item>

              <q-item clickable v-ripple class="profile-menu-item profile-menu-item--danger" @click="onLogout">
                <q-item-section avatar>
                  <q-icon name="logout" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>Sign out</q-item-label>
                  <q-item-label caption>End this session</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </template>
      </q-toolbar>
    </q-header>

    <q-drawer
      id="mobile-navigation-drawer"
      v-model="leftDrawerOpen"
      :width="240"
      :breakpoint="1023"
      behavior="mobile"
      dark
      aria-label="Mobile navigation"
    >
      <div class="drawer-content">
        <div class="drawer-brand">
          <div class="drawer-brand-mark">
            <q-icon name="rocket_launch" size="16px" />
          </div>
          <span>Career<span class="brand-accent">Vault</span></span>
          <q-space />
          <q-btn
            flat
            round
            dense
            icon="close"
            color="white"
            aria-label="Close navigation menu"
            class="drawer-close"
            @click="leftDrawerOpen = false"
          />
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
      </div>
    </q-drawer>

    <q-page-container class="page-container">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useNotificationStore } from "@/stores/notifications";

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
const notificationStore = useNotificationStore();
const router = useRouter();
const route = useRoute();

const currentYear = new Date().getFullYear();
const leftDrawerOpen = ref(false);
const userInitials = computed(() => auth.user?.full_name?.split(/\s+/).filter(Boolean).slice(0, 2).map(part => part[0]).join("").toUpperCase() || "CV");
const notificationCaption = computed(() =>
  notificationStore.unseenCount > 0
    ? `${notificationStore.unseenCount} unseen notification${notificationStore.unseenCount === 1 ? "" : "s"}`
    : "You’re all caught up"
);
let notificationPoll: ReturnType<typeof setInterval> | undefined;

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
        name: "email-follow-ups",
        label: "Email Follow-ups",
        icon: "mark_email_read",
        to: "/email-follow-ups"
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
  void notificationStore.refreshUnseenCount();
  notificationPoll = setInterval(() => {
    void notificationStore.refreshUnseenCount();
  }, 30_000);
});

onBeforeUnmount(() => {
  if (notificationPoll) clearInterval(notificationPoll);
});

function onLogout() {
  notificationStore.clear();
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

.user-avatar-wrap {
  position: relative;
  display: flex;
}

.profile-notification-badge {
  position: absolute;
  top: -7px;
  left: -8px;
  z-index: 2;
  min-width: 17px;
  min-height: 17px;
  padding: 2px 4px;
  border: 2px solid #174f65;
  font-size: 9px;
  font-weight: 800;
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

:global(.user-menu-card) {
  min-width: 292px;
  padding: 8px;
  border: 1px solid rgba(16, 42, 67, 0.08);
  background: #fff;
}

.user-menu-header {
  padding: 12px 10px;
  background: linear-gradient(135deg, #f1f8fb 0%, #f8fbfc 100%);
  border-radius: 10px;
}

.profile-avatar {
  color: #fff;
  background: linear-gradient(135deg, #1f6f8b 0%, #219ebc 100%);
  font-size: 14px;
  font-weight: 800;
  box-shadow: 0 4px 10px rgba(31, 111, 139, 0.22);
}

.user-menu-name {
  font-weight: 600;
  color: #023047;
}

.user-menu-email {
  color: #6b8a99;
}

.user-menu-account {
  margin-top: 3px;
  color: #8a9eaa;
  font-size: 10px;
}

.profile-menu-item {
  min-height: 56px;
  margin: 4px 0;
  border-radius: 9px;
  color: #243b53;

  &:hover {
    background: #f1f8fb;
  }

  :deep(.q-item__label--caption) {
    margin-top: 2px;
    color: #829ab1;
    font-size: 11px;
  }

  :deep(.q-icon) {
    color: #1f6f8b;
  }
}

.profile-menu-item--danger {
  color: #b42318;

  &:hover {
    background: #fff4f2;
  }

  :deep(.q-icon) {
    color: #d64545;
  }
}

.drawer-content {
  height: 100%;
  background: #023047;
  display: flex;
  flex-direction: column;
  overflow: hidden;
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
  min-height: 0;
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
