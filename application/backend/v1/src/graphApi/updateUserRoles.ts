import axios from "axios";
import { getAccessToken } from "./getAccessToken";
import { getFormatedExtension } from "../utils/getFormatedExtension";

export const updateUserRoles = async (userId: string, rolesString: string) => {
  const accessToken = await getAccessToken();

  const response = await axios.patch(
    `https://graph.microsoft.com/v1.0/users/${userId}`,
    {
      [getFormatedExtension("AzureAdminPageRole")]: rolesString,
    },
    {
      headers: {
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      },
    }
  );

  return response.status === 204;
};
