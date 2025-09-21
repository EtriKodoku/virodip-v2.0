import * as jwt from "jsonwebtoken";
import { parseRolesFromString } from "../../utils/roleConverters";

export const getRolesFromToken = (token: string): string[] => {
  try {
    const decoded: any = jwt.decode(token);
    const rawRoles = decoded?.extension_AzureAdminPageRole || "";
    return parseRolesFromString(rawRoles);
  } catch (error) {
    return [];
  }
};
