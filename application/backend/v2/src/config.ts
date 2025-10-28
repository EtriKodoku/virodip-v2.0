export const AZURE_CONFIG = {
  tenantId: process.env.AZURE_TENANT_ID!,
  clientId: process.env.AZURE_CLIENT_ID!,
  clientSecret: process.env.AZURE_CLIENT_SECRET!,
  extensionAppId: process.env.AZURE_EXTENSION_APP_ID!,
};

export const BASIC_AUTH = {
  username: process.env.BASIC_AUTH_USERNAME!,
  password: process.env.BASIC_AUTH_PASSWORD!,
};

export const OWNER = {
  email: process.env.OWNER_EMAIL!,
};
