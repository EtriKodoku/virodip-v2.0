import {
  app,
  HttpRequest,
  HttpResponseInit,
  InvocationContext,
} from "@azure/functions";
import { User } from "../types/User";
import { getRoles } from "../utils/getRoles";
import { checkBasicAuth } from "../auth/checkBasicAuth";
import { addUser } from "../services/userService";

type CreateUserResponseBody = {
  email: string;
  objectId: string;
  [key: string]: any;
};

export const createUserHandler = async (
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
    const body = (await request.json()) as CreateUserResponseBody;

    const userData: User = {
      id: body.objectId,
      displayName: body.displayName ?? null,
      jobTitle: body.jobTitle ?? null,
      department: body.department ?? null,
      createdDateTime: body.createdDateTime ?? null,
      accountEnabled: body.accountEnabled ?? false,
      onPremisesSyncEnabled: body.onPremisesSyncEnabled ?? false,
      preferredLanguage: body.preferredLanguage ?? null,
      role: getRoles(body.email),
    };

    await addUser(userData);

    return {
      status: 200,
      jsonBody: {
        version: "1.0.0",
        status: 200,
        action: "Continue",
      },
    };
  } catch (err: any) {
    context.error("Error in createUserHandler", err);
    return {
      status: 500,
      jsonBody: {
        version: "1.0.0",
        status: 500,
        userMessage: "Something went wrong while saving user data.",
      },
    };
  }
};

app.http("createUser", {
  methods: ["POST"],
  handler: createUserHandler,
  route: "users",
  authLevel: "anonymous",
});
