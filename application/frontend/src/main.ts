import "./assets/main.css";

import { createApp } from "vue";
import { createPinia } from "pinia";

import { myMSALObj } from "@/azure/msalConfig.ts";

import { FontAwesomeIcon } from "./plugins/fontAwesome.ts";

import ToastPlugin from "vue-toast-notification";
import "vue-toast-notification/dist/theme-bootstrap.css";

import App from "./App.vue";
import router from "./router";
import { i18n } from "./i18n.ts";

(async () => {
  await myMSALObj.initialize();

  const app = createApp(App);
  const pinia = createPinia();

  app.component("font-awesome-icon", FontAwesomeIcon);

  app.use(pinia);
  app.use(router);
  app.use(ToastPlugin);
  app.use(i18n);

  app.mount("#app");
})();
