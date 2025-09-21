export const rolePermissions: Record<string, string[]> = {
  owner: ["admin", "analyst", "moderator", "user"],
  admin: ["analyst", "moderator", "user"],
  analyst: [],
  moderator: [],
  user: [],
};
