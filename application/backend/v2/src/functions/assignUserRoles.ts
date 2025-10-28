import {
  app,
  HttpRequest,
  HttpResponseInit,
  InvocationContext,
} from "@azure/functions";

import { getRolesFromToken } from "../auth/jwt/getRolesFromToken";
import { rolePermissions } from "../data/rolePermissions";
import { parseRolesFromString } from "../utils/roleConverters";
import { getUserById, updateUserRole } from "../services/userService";

interface assignUserRolesRequestBody {
  newRoles: string;
}

export const assignUserRolesHandler = async (
  request: HttpRequest,
  context: InvocationContext
): Promise<HttpResponseInit> => {
  const authHeader = request.headers.get("authorization") || "";
  const token = authHeader.replace("Bearer ", "");

  if (!token) {
    return {
      status: 401,
      jsonBody: { error: "No token provided" },
    };
  }

  const currentUserRoles = getRolesFromToken(token);

  const isOwner = currentUserRoles.includes("owner");
  const isAdmin = currentUserRoles.includes("admin");

  if (!isOwner && !isAdmin) {
    return {
      status: 403,
      jsonBody: { error: "Insufficient permissions" },
    };
  }

  try {
    const body = (await request.json()) as assignUserRolesRequestBody;
    const targetUserId = request.params.id;
    const targetUser = await getUserById(targetUserId);

    const { newRoles } = body;

    const allowedRoles = rolePermissions[isOwner ? "owner" : "admin"];

    const isAllowed = parseRolesFromString(targetUser.role).every((role) =>
      allowedRoles.includes(role)
    );

    if (!isAllowed) {
      return {
        status: 403,
        jsonBody: { error: "You cannot assign some of these roles" },
      };
    }

    await updateUserRole(targetUserId, newRoles);

    return {
      status: 200,
      jsonBody: { success: true },
    };
  } catch (error) {
    context.error("Error assigning role");
    return {
      status: 500,
      jsonBody: { error: "Internal server error" },
    };
  }
};

app.http("assignUserRoles", {
  methods: ["POST"],
  handler: assignUserRolesHandler,
  route: "users/{id}/roles",
});
