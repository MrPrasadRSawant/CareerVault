<template>
  <q-layout view="hHh Lpr lFf">
    <q-header class="app-header">
      <q-toolbar class="app-toolbar">
        <q-btn
          flat
          round
          dense
          icon="menu"
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
          @keyup.enter="goDashboard"
        >
          <div class="toolbar-brand-mark" aria-hidden="true">CV</div>
          <span>Career<span class="brand-accent">Vault</span></span>
        </div>

        <form class="vault-search" role="search" @submit.prevent="submitSearch">
          <q-input
            v-model="globalSearch"
            dense
            outlined
            clearable
            placeholder="Search opportunities, companies..."
            aria-label="Search CareerVault"
          >
            <template #prepend><q-icon name="search" size="20px" /></template>
          </q-input>
        </form>

        <q-space />

        <nav class="header-nav" aria-label="Primary navigation">
          <q-btn
            v-for="item in primaryNavItems"
            :key="item.name"
            flat
            no-caps
            :to="item.to"
            :class="{ 'nav-trigger--active': isActive(item.name) }"
            class="nav-trigger"
          >
            <q-icon :name="item.icon" size="21px" class="nav-icon" />
            <span>{{ item.shortLabel || item.label }}</span>
          </q-btn>

          <q-btn-dropdown
            flat
            no-caps
            class="nav-trigger nav-more"
            :class="{ 'nav-trigger--active': isGroupActive(moreGroup) }"
            content-class="nav-menu"
          >
            <template #label>
              <div class="nav-trigger-content">
                <q-icon name="apps" size="21px" />
                <span>More</span>
              </div>
            </template>
            <q-list padding>
              <q-item
                v-for="item in moreGroup.items"
                :key="item.name"
                clickable
                v-ripple
                :to="item.to"
                :active="isActive(item.name)"
                active-class="nav-item--active"
                class="nav-item"
                exact
              >
                <q-item-section avatar
                  ><q-icon :name="item.icon"
                /></q-item-section>
                <q-item-section>{{ item.label }}</q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </nav>

        <template v-if="auth.user">
          <q-btn
            flat
            round
            class="notification-button"
            icon="notifications_none"
            aria-label="Notifications"
            to="/notifications"
          >
            <q-badge
              v-if="notificationStore.unseenCount > 0"
              floating
              rounded
              color="negative"
              :label="notificationStore.badgeLabel"
            />
          </q-btn>

          <q-btn-dropdown
            flat
            no-caps
            class="user-menu"
            content-class="nav-menu user-menu-card"
            aria-label="Open profile menu"
          >
            <template #label>
              <div class="user-chip">
                <q-avatar size="34px" class="profile-avatar">{{
                  userInitials
                }}</q-avatar>
                <div class="user-chip-text q-hide-sm-and-down">
                  <div class="user-name">{{ firstName }}</div>
                  <div class="user-account">My account</div>
                </div>
              </div>
            </template>

            <q-list padding>
              <q-item class="user-menu-header">
                <q-item-section avatar>
                  <q-avatar size="46px" class="profile-avatar">{{
                    userInitials
                  }}</q-avatar>
                </q-item-section>
                <q-item-section>
                  <q-item-label class="user-menu-name">{{
                    auth.user.full_name
                  }}</q-item-label>
                  <q-item-label caption class="user-menu-email">{{
                    auth.user.email
                  }}</q-item-label>
                </q-item-section>
              </q-item>
              <q-separator spaced />
              <q-item
                clickable
                v-ripple
                to="/notifications"
                exact
                class="profile-menu-item"
              >
                <q-item-section avatar
                  ><q-icon name="notifications_none"
                /></q-item-section>
                <q-item-section>
                  <q-item-label>Notifications</q-item-label>
                  <q-item-label caption>{{ notificationCaption }}</q-item-label>
                </q-item-section>
              </q-item>
              <q-item
                clickable
                v-ripple
                to="/settings"
                exact
                class="profile-menu-item"
              >
                <q-item-section avatar
                  ><q-icon name="settings"
                /></q-item-section>
                <q-item-section>
                  <q-item-label>Settings</q-item-label>
                  <q-item-label caption>Account and integrations</q-item-label>
                </q-item-section>
              </q-item>
              <q-item
                clickable
                v-ripple
                class="profile-menu-item profile-menu-item--danger"
                @click="onLogout"
              >
                <q-item-section avatar><q-icon name="logout" /></q-item-section>
                <q-item-section>Sign out</q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </template>
      </q-toolbar>
    </q-header>

    <q-drawer
      id="mobile-navigation-drawer"
      v-model="leftDrawerOpen"
      :width="280"
      :breakpoint="1023"
      behavior="mobile"
      aria-label="Mobile navigation"
    >
      <div class="drawer-content">
        <div class="drawer-brand">
          <div class="toolbar-brand-mark">CV</div>
          <span>Career<span class="brand-accent">Vault</span></span>
          <q-space />
          <q-btn
            flat
            round
            dense
            icon="close"
            aria-label="Close navigation menu"
            @click="leftDrawerOpen = false"
          />
        </div>

        <div v-if="auth.user" class="drawer-profile">
          <q-avatar size="44px" class="profile-avatar">{{
            userInitials
          }}</q-avatar>
          <div>
            <div class="drawer-profile-name">{{ auth.user.full_name }}</div>
            <div class="drawer-profile-email">{{ auth.user.email }}</div>
          </div>
        </div>

        <q-scroll-area class="drawer-scroll">
          <q-list padding>
            <template v-for="group in mobileNavGroups" :key="group.label">
              <q-item-label header class="drawer-section-label">{{
                group.label
              }}</q-item-label>
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
                <q-item-section avatar
                  ><q-icon :name="item.icon"
                /></q-item-section>
                <q-item-section>{{ item.label }}</q-item-section>
                <q-item-section
                  v-if="
                    item.name === 'notifications' &&
                    notificationStore.unseenCount
                  "
                  side
                >
                  <q-badge
                    rounded
                    color="negative"
                    :label="notificationStore.badgeLabel"
                  />
                </q-item-section>
              </q-item>
            </template>
          </q-list>
        </q-scroll-area>

        <div class="drawer-footer">CareerVault · {{ currentYear }}</div>
      </div>
    </q-drawer>

    <q-page-container class="page-container"><router-view /></q-page-container>
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
  shortLabel?: string;
  icon: string;
  to: string;
}

interface NavGroup {
  label: string;
  items: NavItem[];
}

const auth = useAuthStore();
const notificationStore = useNotificationStore();
const router = useRouter();
const route = useRoute();
const currentYear = new Date().getFullYear();
const leftDrawerOpen = ref(false);
const globalSearch = ref("");
const userInitials = computed(
  () =>
    auth.user?.full_name
      ?.split(/\s+/)
      .filter(Boolean)
      .slice(0, 2)
      .map(part => part[0])
      .join("")
      .toUpperCase() || "CV"
);
const firstName = computed(
  () => auth.user?.full_name?.trim().split(/\s+/)[0] || "Profile"
);
const notificationCaption = computed(() =>
  notificationStore.unseenCount > 0
    ? `${notificationStore.unseenCount} unseen notification${notificationStore.unseenCount === 1 ? "" : "s"}`
    : "You're all caught up"
);
let notificationPoll: ReturnType<typeof setInterval> | undefined;

const primaryNavItems: NavItem[] = [
  {
    name: "dashboard",
    label: "Dashboard",
    shortLabel: "Home",
    icon: "home",
    to: "/dashboard"
  },
  {
    name: "opportunities",
    label: "Opportunities",
    shortLabel: "Jobs",
    icon: "work",
    to: "/opportunities"
  },
  {
    name: "applications",
    label: "Applications",
    icon: "assignment",
    to: "/applications"
  },
  { name: "resumes", label: "Resumes", icon: "description", to: "/resumes" }
];

const moreGroup: NavGroup = {
  label: "More",
  items: [
    {
      name: "email-follow-ups",
      label: "Email follow-ups",
      icon: "mark_email_read",
      to: "/email-follow-ups"
    },
    {
      name: "cover-letters",
      label: "Cover letters",
      icon: "article",
      to: "/cover-letters"
    },
    { name: "settings", label: "Settings", icon: "settings", to: "/settings" }
  ]
};

const mobileNavGroups: NavGroup[] = [
  { label: "Career", items: primaryNavItems },
  { label: "Tools", items: moreGroup.items },
  {
    label: "Account",
    items: [
      {
        name: "notifications",
        label: "Notifications",
        icon: "notifications_none",
        to: "/notifications"
      }
    ]
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
  if (!isActive("dashboard")) void router.push({ name: "dashboard" });
}

function submitSearch() {
  const search = globalSearch.value.trim();
  if (search) void router.push({ name: "opportunities", query: { search } });
  else void router.push({ name: "opportunities" });
}

onMounted(() => {
  void auth.loadUser();
  void notificationStore.refreshUnseenCount();
  notificationPoll = setInterval(
    () => void notificationStore.refreshUnseenCount(),
    30_000
  );
});

onBeforeUnmount(() => {
  if (notificationPoll) clearInterval(notificationPoll);
});

async function onLogout() {
  notificationStore.clear();
  await auth.logout();
  await router.push({ name: "login" });
}
</script>

<style lang="scss" scoped>
.app-header {
  color: #263547;
  background: rgba(255, 255, 255, 0.98);
  border-bottom: 1px solid #e2e7ec;
  box-shadow: 0 1px 3px rgba(17, 31, 48, 0.05);
}

.app-toolbar {
  width: min(100%, 1220px);
  min-height: 66px;
  margin: 0 auto;
  padding: 0 18px;
  gap: 12px;
}

.header-hamburger {
  display: none;
  color: #334155;
}

.toolbar-brand {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 4px;
  color: #14213d;
  font-size: 19px;
  font-weight: 800;
  letter-spacing: -0.45px;
  cursor: pointer;
  user-select: none;
}

.toolbar-brand-mark {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  border-radius: 9px;
  color: #fff;
  background: #1769e0;
  font-size: 13px;
  font-weight: 900;
  letter-spacing: -0.4px;
  box-shadow: 0 5px 14px rgba(23, 105, 224, 0.2);
}

.brand-accent {
  color: #1769e0;
}

.vault-search {
  width: clamp(210px, 23vw, 320px);
  margin-left: 8px;
}

.vault-search :deep(.q-field__control) {
  height: 38px;
  border-radius: 20px;
  background: #f6f8fb;
}

.vault-search :deep(.q-field__native) {
  font-size: 13px;
}
.vault-search :deep(.q-field__control::before) {
  border-color: #d9e0e8;
}

.header-nav {
  display: flex;
  align-self: stretch;
  align-items: stretch;
  gap: 2px;
}

.nav-trigger {
  min-width: 68px;
  padding: 4px 9px 2px;
  border-radius: 0;
  color: #687386;
  font-size: 11px;
  font-weight: 500;
}

.nav-trigger :deep(.q-btn__content),
.nav-trigger-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3px;
  flex-wrap: nowrap;
  line-height: 1.1;
}
.nav-icon {
  display: inline-flex;
  width: 22px;
  height: 22px;
  align-items: center;
  justify-content: center;
  line-height: 22px;
}

.nav-trigger::after {
  content: "";
  position: absolute;
  right: 8px;
  bottom: -1px;
  left: 8px;
  height: 2px;
  border-radius: 2px 2px 0 0;
  background: transparent;
}

.nav-trigger:hover {
  color: #172033;
  background: #f8fafc;
}
.nav-trigger--active {
  color: #1769e0;
}
.nav-trigger--active::after {
  background: #1769e0;
}
.nav-more :deep(.q-btn-dropdown__arrow) {
  display: none;
}

:global(.nav-menu) {
  min-width: 230px;
  padding: 5px;
  border: 1px solid #e1e7ee;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 16px 38px rgba(30, 45, 65, 0.14);
}

.nav-item {
  min-height: 48px;
  margin: 2px 0;
  border-radius: 8px;
  color: #334155;
  font-weight: 550;
}

.nav-item:hover,
.nav-item--active {
  color: #1769e0;
  background: #eef5ff;
}
.nav-item :deep(.q-icon) {
  color: #728095;
}
.nav-item--active :deep(.q-icon) {
  color: #1769e0;
}

.notification-button {
  color: #5f6b7b;
}
.notification-button:hover {
  color: #1769e0;
  background: #f0f5fb;
}

.user-menu {
  margin-left: -5px;
  border-radius: 24px;
}
.user-chip {
  display: flex;
  align-items: center;
  gap: 8px;
}
.profile-avatar {
  color: #fff;
  background: linear-gradient(135deg, #1769e0, #635bdf);
  font-size: 13px;
  font-weight: 800;
}
.user-name {
  color: #253247;
  font-size: 12px;
  font-weight: 700;
  line-height: 1.2;
}
.user-account {
  color: #8a95a5;
  font-size: 10px;
  line-height: 1.2;
}

:global(.user-menu-card) {
  min-width: 292px;
}
.user-menu-header {
  padding: 12px 10px;
  border-radius: 9px;
  background: #f7f9fc;
}
.user-menu-name {
  color: #172033;
  font-weight: 700;
}
.user-menu-email {
  color: #748094;
}
.profile-menu-item {
  min-height: 52px;
  margin: 2px 0;
  border-radius: 8px;
  color: #334155;
}
.profile-menu-item:hover {
  background: #f5f8fc;
}
.profile-menu-item :deep(.q-icon) {
  color: #64748b;
}
.profile-menu-item :deep(.q-item__label--caption) {
  margin-top: 2px;
  color: #8a95a5;
  font-size: 11px;
}
.profile-menu-item--danger {
  color: #ba2f39;
}
.profile-menu-item--danger :deep(.q-icon) {
  color: #ba2f39;
}
.profile-menu-item--danger:hover {
  background: #fff3f4;
}

.drawer-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #fff;
}
.drawer-brand {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 14px 16px;
  border-bottom: 1px solid #e6eaf0;
  color: #14213d;
  font-size: 18px;
  font-weight: 800;
}
.drawer-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 14px;
  padding: 14px;
  border-radius: 12px;
  background: #f4f7fb;
}
.drawer-profile-name {
  color: #1f2b3d;
  font-size: 13px;
  font-weight: 700;
}
.drawer-profile-email {
  max-width: 165px;
  overflow: hidden;
  color: #7b8797;
  font-size: 11px;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.drawer-scroll {
  flex: 1;
  min-height: 0;
}
.drawer-section-label {
  padding-top: 16px;
  color: #9aa4b2;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.9px;
  text-transform: uppercase;
}
.menu-item {
  min-height: 50px;
  margin: 2px 10px;
  border-radius: 9px;
  color: #536174;
  font-weight: 550;
}
.menu-item:hover {
  background: #f5f8fc;
}
.menu-item--active {
  color: #1769e0;
  background: #edf4ff;
}
.menu-item--active :deep(.q-icon) {
  color: #1769e0;
}
.drawer-footer {
  padding: 14px;
  border-top: 1px solid #e6eaf0;
  color: #9aa4b2;
  font-size: 11px;
  text-align: center;
}

.page-container {
  background: #f3f5f7;
}

@media (max-width: 1120px) {
  .vault-search {
    display: none;
  }
}

@media (max-width: 1023px) {
  .app-toolbar {
    min-height: 58px;
    padding: 0 12px;
  }
  .header-hamburger {
    display: inline-flex;
  }
  .header-nav,
  .notification-button {
    display: none;
  }
  .toolbar-brand {
    font-size: 17px;
  }
  .toolbar-brand-mark {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .user-chip-text {
    display: none;
  }
  .app-toolbar {
    gap: 5px;
  }
}
</style>
