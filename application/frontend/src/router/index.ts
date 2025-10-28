import { ref } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/useAuthStore";

import main from "@/containers/main/routes";
import me from "@/containers/me/routes";
import users from "@/containers/users/routes";
import howToUse from "@/containers/how-to-use/routes";
import admin from "@/containers/admin/routes";

export const isLoading = ref(false);

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [...main, ...me, ...users, ...howToUse, ...admin],
});

router.beforeEach(async (to, _, next) => {
  try {
    const authStore = useAuthStore();
    const { initAuth, setTokenData } = authStore;
    const { isAuthenticated, isInitialized, idTokenClaims, isAdmin, isOwner } =
      storeToRefs(authStore);

    isLoading.value = true;

    if (!isInitialized.value) {
      await initAuth();
    }

    if (to.meta.requiresAuth && !isAuthenticated.value) {
      return next({ name: "main" });
    }

    if (to.meta.requiresAdmin && !idTokenClaims.value) {
      await setTokenData();

      if (!isAdmin.value && !isOwner.value) {
        return next({ name: "main" });
      }
    }

    next();
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false;
  }
});

export default router;
