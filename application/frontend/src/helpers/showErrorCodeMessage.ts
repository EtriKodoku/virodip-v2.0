import { i18n } from "@/i18n";
import { showNotification } from "./showNotification";

export const showErrorCodeMessage = (statusCode: number) => {
  const t = i18n.global.t;
  const message = t(
    `notifications.errors.${statusCode}`,
    t("notifications.unexpectedError")
  );
  showNotification("error", message);
};
