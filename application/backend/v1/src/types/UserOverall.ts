import type { User } from "./User";

export type UserOverall = Pick<
  User,
  "id" | "displayName" | "createdDateTime" | "role"
>;
