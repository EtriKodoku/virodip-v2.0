import {
  PublicClientApplication,
  type Configuration,
  type RedirectRequest,
} from "@azure/msal-browser";

import { azureConfig } from "@/config";

const { clientId, tenantName, userFlow, redirectUri } = azureConfig;

export const msalConfig: Configuration = {
  auth: {
    clientId,
    authority: `https://${tenantName}.b2clogin.com/${tenantName}.onmicrosoft.com/${userFlow}`,
    knownAuthorities: [`${tenantName}.b2clogin.com`],
    redirectUri,
    postLogoutRedirectUri: "/",
  },
  cache: {
    cacheLocation: "localStorage",
    storeAuthStateInCookie: true,
  },
};

export const loginRequest: RedirectRequest = {
  scopes: ["openid", "profile"],
};

export const myMSALObj = new PublicClientApplication(msalConfig);
