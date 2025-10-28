import axios from "axios";
import { getAccessToken } from "./getAccessToken";

export const deleteUserById = async (userId: string): Promise<void> => {
  const accessToken = await getAccessToken();

  const url = `https://graph.microsoft.com/v1.0/users/${userId}`;

  await axios.delete(url, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
};
