import {
  app,
  HttpRequest,
  HttpResponseInit,
  InvocationContext,
} from "@azure/functions";
import { deleteUserById } from "../graphApi/deleteUserById";
import { getRolesFromToken } from "../auth/jwt/getRolesFromToken";
import { getUserById } from "../graphApi/getUserById";
import { rolePermissions } from "../data/rolePermissions";
import { parseRolesFromString } from "../utils/roleConverters";

export const deleteUserHandler = async (
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

  const userId = request.params.id;

  if (!userId) {
    return {
      status: 400,
      jsonBody: { error: "Missing user ID in route" },
    };
  }

  try {
    const targetUser = await getUserById(userId);

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

    await deleteUserById(userId);

    return {
      status: 204,
    };
  } catch (error) {
    context.error("Error deleting user:", error.message || error);
    return {
      status: 500,
      jsonBody: { error: "Failed to delete user" },
    };
  }
};

app.http("deleteUserById", {
  methods: ["DELETE"],
  handler: deleteUserHandler,
  authLevel: "anonymous",
  route: "users/{id}",
});
