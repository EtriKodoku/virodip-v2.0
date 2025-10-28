import { type ToastType, useToast } from "vue-toast-notification";

const $toast = useToast();

export function showNotification(type: ToastType, message: string) {
  $toast.open({
    position: "top-right",
    duration: 3000,
    type,
    message,
  });
}
