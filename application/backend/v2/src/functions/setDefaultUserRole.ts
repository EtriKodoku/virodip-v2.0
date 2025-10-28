import {
  app,
  HttpRequest,
  HttpResponseInit,
  InvocationContext,
} from "@azure/functions";
import { getFormatedExtension } from "../utils/getFormatedExtension";
import { checkBasicAuth } from "../auth/checkBasicAuth";
import { addUser, getUserById } from "../services/userService";
import { getRoles } from "../utils/getRoles";

interface AssignRoleRequestBody {
  email: string;
  objectId: string;
  [key: string]: any;
}

export const setDefaultUserRoleHandler = async (
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

  try {
    const body = (await request.json()) as AssignRoleRequestBody;
    const objectId = body.objectId;

    const user = await getUserById(objectId);

    if (!user) {
      const roles = getRoles(body.email);

      const user = {
        id: body.objectId,
        displayName: body.displayName ?? null,
        jobTitle: body.jobTitle ?? null,
        department: body.department ?? null,
        createdDateTime: body.createdDateTime ?? null,
        accountEnabled: body.accountEnabled ?? false,
        onPremisesSyncEnabled: body.onPremisesSyncEnabled ?? false,
        preferredLanguage: body.preferredLanguage ?? null,
        role: roles,
      };

      await addUser(user);

      return {
        status: 200,
        jsonBody: {
          version: "1.0.0",
          action: "Continue",
          [getFormatedExtension("AzureAdminPageRole")]: roles,
        },
      };
    }

    return {
      status: 200,
      jsonBody: {
        version: "1.0.0",
        action: "Continue",
        [getFormatedExtension("AzureAdminPageRole")]: user.role,
      },
    };
  } catch (err: any) {
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
  handler: setDefaultUserRoleHandler,
});
