import axios from "axios";
import { AZURE_CONFIG } from "../config";

export const getAccessToken = async () => {
  const { tenantId, clientId, clientSecret } = AZURE_CONFIG;

  const tokenResponse = await axios.post(
    `https://login.microsoftonline.com/${tenantId}/oauth2/v2.0/token`,
    new URLSearchParams({
      client_id: clientId,
      client_secret: clientSecret,
      scope: "https://graph.microsoft.com/.default",
      grant_type: "client_credentials",
    }),
    {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    }
  );

  return tokenResponse.data.access_token;
};
