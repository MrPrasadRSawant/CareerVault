import { defineBoot } from "#q-app";
import { api, axios } from "@/api/client";

export default defineBoot(({ app }) => {
  app.config.globalProperties.$axios = axios;
  app.config.globalProperties.$api = api;
});

export { api, axios };
