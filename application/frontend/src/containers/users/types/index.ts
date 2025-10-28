import type { User } from "@/types/User";

export type UserOverall = Pick<
  User,
  "id" | "displayName" | "createdDateTime" | "role"
>;

export type GetUsersResponseData = {
  users: UserOverall[];
};
