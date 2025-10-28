import axios from "axios";
import { getAccessToken } from "./getAccessToken";
import { getFormatedExtension } from "../utils/getFormatedExtension";
import { User } from "../types/User";

export const getUserById = async (userId: string): Promise<User | null> => {
  const accessToken = await getAccessToken();

  const roleExtension = getFormatedExtension("AzureAdminPageRole");

  const url = `https://graph.microsoft.com/v1.0/users/${userId}?$select=id,displayName,jobTitle,department,createdDateTime,accountEnabled,onPremisesSyncEnabled,preferredLanguage,${roleExtension}`;

  try {
    const response = await axios.get(url, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    const data = response.data;

    const user: User = {
      id: data.id,
      displayName: data.displayName,
      jobTitle: data.jobTitle,
      department: data.department,
      createdDateTime: data.createdDateTime,
      accountEnabled: data.accountEnabled,
      onPremisesSyncEnabled: data.onPremisesSyncEnabled,
      preferredLanguage: data.preferredLanguage,
      role: data[roleExtension] || "",
    };

    return user;
  } catch (error: any) {
    if (axios.isAxiosError(error) && error.response?.status === 404) {
      return null;
    }

    throw error;
  }
};
