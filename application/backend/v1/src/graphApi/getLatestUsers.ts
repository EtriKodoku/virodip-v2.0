import axios from "axios";
import { getAccessToken } from "./getAccessToken";
import { getFormatedExtension } from "../utils/getFormatedExtension";
import { formatDateToUnix } from "../utils/formatDateToUnix";
import { UserOverall } from "../types/UserOverall";

export const getLatestUsers = async (): Promise<UserOverall[]> => {
  const accessToken = await getAccessToken();

  const roleExtension = getFormatedExtension("AzureAdminPageRole");

  const url = `https://graph.microsoft.com/v1.0/users/?$select=id,displayName,createdDateTime,${roleExtension}`;

  try {
    const response = await axios.get(url, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    const data = response.data.value as UserOverall[];

    const filteredUsers = data
      .filter((user) => user[roleExtension])
      .sort(
        (a, b) =>
          formatDateToUnix(b.createdDateTime) -
          formatDateToUnix(a.createdDateTime)
      )
      .slice(0, 5)
      .map((user: any) => ({
        id: user.id,
        displayName: user.displayName,
        createdDateTime: user.createdDateTime,
        role: user[roleExtension],
      }));

    return filteredUsers;
  } catch (error: any) {
    if (axios.isAxiosError(error) && error.response?.status === 404) {
      return null;
    }

    throw error;
  }
};
