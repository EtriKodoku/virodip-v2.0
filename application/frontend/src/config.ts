export const azureConfig = {
  clientId: import.meta.env.VITE_AZURE_CLIENT_ID,
  tenantName: import.meta.env.VITE_AZURE_TENANT_NAME,
  userFlow: import.meta.env.VITE_AZURE_USER_FLOW,
  redirectUri: import.meta.env.VITE_AZURE_REDIRECT_URI,
};

export const demoUserCredentials = {
  email: import.meta.env.VITE_DEMO_USER_CREDENTIALS_EMAIL,
  password: import.meta.env.VITE_DEMO_USER_CREDENTIALS_PASSWORD,
};

export const localeConfig = {
  defaultLocale: import.meta.env.VITE_DEFAULT_LOCALE!,
  fallbackLocale: import.meta.env.VITE_FALLBACK_LOCALE!,
};
