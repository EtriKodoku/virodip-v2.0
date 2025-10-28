import { get_users } from "@/containers/users/api";
import type { GetUsersResponseData } from "@/containers/users/types/index";

export const getUsers = async () => {
  const response = await fetch(get_users);

  if (!response.ok) {
    throw new Error("Failed to fetch users");
  }

  const data = (await response.json()) as GetUsersResponseData;

  return data;
};
