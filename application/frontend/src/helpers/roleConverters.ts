export const parseRolesFromString = (rolesString: string): string[] => {
  return rolesString
    .split(",")
    .map((r) => r.trim())
    .filter((r) => r.length > 0);
};

export const stringifyRoles = (roles: string[]): string => {
  return roles.map((r) => r.trim()).join(", ");
};
