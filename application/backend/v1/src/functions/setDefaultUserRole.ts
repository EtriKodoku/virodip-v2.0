import {
  app,
  HttpRequest,
  InvocationContext,
  HttpResponseInit,
} from "@azure/functions";
import { getFormatedExtension } from "../utils/getFormatedExtension";
import { OWNER } from "../config";
import { checkBasicAuth } from "../auth/checkBasicAuth";
import { stringifyRoles } from "../utils/roleConverters";
import { updateUserRoles } from "../graphApi/updateUserRoles";

interface AssignRoleRequestBody {
  email?: string;
  objectId?: string;
  [key: string]: any;
}

export const setDefaultUserRole = async (
  request: HttpRequest,
  context: InvocationContext
): Promise<HttpResponseInit> => {
  if (!checkBasicAuth(request)) {
    context.error("Unauthorized");
    return {
      status: 401,
      headers: { "WWW-Authenticate": "Basic" },
      jsonBody: { error: "Unauthorized" },
    };
  }

  const { email: ownerEmail } = OWNER;

  try {
    const body = (await request.json()) as AssignRoleRequestBody;
    const userEmail = body.email?.toLowerCase();

    if (!body[getFormatedExtension("AzureAdminPageRole")]) {
      let roles = [];

      if (userEmail === ownerEmail.toLowerCase()) {
        await updateUserRoles(
          body.objectId,
          "user, analyst, moderator, admin, owner"
        );
        roles.push("user, analyst, moderator, admin, owner");
      }

      if (roles.length === 0) {
        await updateUserRoles(body.objectId, "user");
        roles.push("user");
      }

      return {
        status: 200,
        jsonBody: {
          version: "1.0.0",
          action: "Continue",
          [getFormatedExtension("AzureAdminPageRole")]: stringifyRoles(roles),
        },
      };
    }

    return {
      status: 200,
      jsonBody: {
        version: "1.0.0",
        action: "Continue",
        [getFormatedExtension("AzureAdminPageRole")]:
          body[getFormatedExtension("AzureAdminPageRole")],
      },
    };
  } catch (err) {
    context.error("Error assigning role:", err);
    return {
      status: 500,
      jsonBody: {
        version: "1.0.0",
        action: "ValidationError",
        userMessage: "Could not assign role",
      },
    };
  }
};

app.http("setDefaultUserRole", {
  methods: ["POST"],
  handler: setDefaultUserRole,
});
