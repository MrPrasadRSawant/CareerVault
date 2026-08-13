import type { RouteRecordRaw } from "vue-router";

const routes: RouteRecordRaw[] = [
  {
    path: "/login",
    name: "login",
    component: () => import("@/modules/Login/LoginPage.vue"),
    meta: { guestOnly: true }
  },
  {
    path: "/register",
    name: "register",
    component: () => import("@/modules/Register/RegisterPage.vue"),
    meta: { guestOnly: true }
  },
  {
    path: "/",
    component: () => import("@/layouts/MainLayout.vue"),
    meta: { requiresAuth: true },
    children: [
      { path: "", redirect: "/dashboard" },
      {
        path: "dashboard",
        name: "dashboard",
        component: () => import("@/modules/Dashboard/DashboardPage.vue")
      },
      {
        path: "opportunities",
        name: "opportunities",
        component: () => import("@/modules/Opportunities/OpportunitiesPage.vue")
      },
      {
        path: "applications",
        name: "applications",
        component: () => import("@/modules/Applications/ApplicationsPage.vue")
      },
      {
        path: "email-follow-ups",
        name: "email-follow-ups",
        component: () =>
          import("@/modules/EmailFollowUps/EmailFollowUpsPage.vue")
      },
      {
        path: "cover-letters",
        name: "cover-letters",
        component: () => import("@/modules/CoverLetters/CoverLettersPage.vue")
      },
      {
        path: "resumes",
        name: "resumes",
        component: () => import("@/modules/Resumes/ResumesPage.vue")
      },
      {
        path: "settings",
        name: "settings",
        component: () => import("@/modules/Settings/SettingsPage.vue")
      },
      {
        path: "notifications",
        name: "notifications",
        component: () => import("@/modules/Notifications/NotificationsPage.vue")
      }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("@/pages/ErrorNotFound.vue")
  }
];

export default routes;
