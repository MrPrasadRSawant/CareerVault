import { defineRouter } from "#q-app";
import {
  createMemoryHistory,
  createRouter,
  createWebHashHistory,
  createWebHistory
} from "vue-router";

import routes from "./routes";

const TOKEN_KEY = "cv_token";
const ROLE_KEY = "cv_role";

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default defineRouter((/* { store, ssrContext } */) => {
  const createHistory = import.meta.env.QUASAR_SERVER
    ? createMemoryHistory
    : import.meta.env.QUASAR_VUE_ROUTER_MODE === "history"
      ? createWebHistory
      : createWebHashHistory;

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(import.meta.env.QUASAR_VUE_ROUTER_BASE)
  });

  Router.beforeEach(to => {
    const isAuthenticated = localStorage.getItem(TOKEN_KEY) !== null;
    const role = localStorage.getItem(ROLE_KEY);

    if (to.meta.requiresAdmin === true) {
      if (!isAuthenticated) {
        return {
          name: "login",
          query: { redirect: to.fullPath }
        };
      }
      if (role !== "system_admin") return { name: "dashboard" };
    }

    if (to.meta.requiresApplicant === true && !isAuthenticated) {
      return { name: "login", query: { redirect: to.fullPath } };
    }

    if (to.meta.requiresApplicant === true && role === "system_admin") {
      return { name: "system-admin-overview" };
    }

    if (to.meta.guestOnly === true && isAuthenticated) {
      return role === "system_admin"
        ? { name: "system-admin-overview" }
        : { name: "dashboard" };
    }
  });

  return Router;
});
