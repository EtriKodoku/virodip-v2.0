import { computed, ref } from "vue";
import { defineStore } from "pinia";
import { loginRequest, myMSALObj } from "@/azure/msalConfig";
import { parseRolesFromString } from "@/helpers/roleConverters";
import { showNotification } from "@/helpers/showNotification";
import { useI18n } from "vue-i18n";
import type { IdTokenClaimsExtended } from "@/types/IdTokenClaimsExtended";

export const useAuthStore = defineStore("auth", () => {
  const { t } = useI18n();

  const isAuthenticated = ref(false);
  const isInitialized = ref(false);
  const bearerToken = ref("");
  const idTokenClaims = ref<IdTokenClaimsExtended | null>(null);

  const userRolesArray = computed(() => {
    if (!idTokenClaims.value) {
      return "";
    }

    return parseRolesFromString(
      idTokenClaims.value!.extension_AzureAdminPageRole
    );
  });

  const isAdmin = computed(() => {
    return userRolesArray.value.includes("admin");
  });

  const isOwner = computed(() => {
    return userRolesArray.value.includes("owner");
  });

  const login = async () => {
    try {
      if (!myMSALObj) {
        throw new Error("MSAL is not initialized");
      }
      await myMSALObj.loginRedirect(loginRequest);
    } catch (error) {
      showNotification("error", t("notifications.auth.loginFailed"));
      console.error("Login error", error);
    }
  };

  const logout = async () => {
    try {
      if (!myMSALObj) {
        throw new Error("MSAL is not initialized");
      }
      isAuthenticated.value = false;
      isInitialized.value = false;
      await myMSALObj.logoutRedirect();
    } catch (error) {
      showNotification("error", t("notifications.auth.logoutFailed"));
      console.error("Logout error", error);
    }
  };

  const initAuth = async () => {
    if (isInitialized.value) {
      return;
    }

    isInitialized.value = true;

    try {
      await myMSALObj.handleRedirectPromise();
      const accounts = myMSALObj.getAllAccounts();
      if (accounts.length > 0) {
        myMSALObj.setActiveAccount(accounts[0]);
        isAuthenticated.value = true;
        setTokenData();
      } else {
        isAuthenticated.value = false;
      }
    } catch (error) {
      showNotification("error", t("notifications.auth.authError"));
      console.error("Auth init error", error);
      isAuthenticated.value = false;
    }
  };

  const setTokenData = async () => {
    if (bearerToken.value) {
      return;
    }

    const token = await getMsalToken();
    if (!token) {
      showNotification("error", t("notifications.auth.tokenMissing"));
      return;
    }

    const tokenClaims = token.idTokenClaims as IdTokenClaimsExtended;

    bearerToken.value = token.idToken;
    idTokenClaims.value = tokenClaims;
  };

  const getMsalToken = async () => {
    try {
      const response = await myMSALObj.acquireTokenSilent(loginRequest);
      return response;
    } catch (error) {
      showNotification("error", t("notifications.auth.tokenAcquisitionFailed"));
      console.error("Token error", error);
    }
  };

  return {
    isAuthenticated,
    isInitialized,
    userRolesArray,
    bearerToken,
    idTokenClaims,
    isAdmin,
    isOwner,
    login,
    logout,
    initAuth,
    getMsalToken,
    setTokenData,
  };
});
