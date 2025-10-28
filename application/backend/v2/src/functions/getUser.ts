import {
  app,
  HttpRequest,
  HttpResponseInit,
  InvocationContext,
} from "@azure/functions";
import { getRolesFromToken } from "../auth/jwt/getRolesFromToken";
import { getUserById } from "../services/userService";

export const getUserHandler = async (
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
    const user = await getUserById(userId);

    if (!user) {
      return {
        status: 404,
        jsonBody: { error: "User not found" },
      };
    }

    return {
      status: 200,
      jsonBody: { user },
    };
  } catch (error: any) {
    context.log("Error fetching user by ID:", error.message);
    return {
      status: 500,
      jsonBody: { error: "Failed to fetch user by ID" },
    };
  }
};

app.http("getUserById", {
  methods: ["GET"],
  route: "users/{id}",
  handler: getUserHandler,
  authLevel: "anonymous",
});
