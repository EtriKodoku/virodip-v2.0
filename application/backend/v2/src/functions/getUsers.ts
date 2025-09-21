import {
  app,
  HttpRequest,
  HttpResponseInit,
  InvocationContext,
} from "@azure/functions";
import { getAllUsers } from "../services/userService";

export const getLatestUsersHandler = async (
  request: HttpRequest,
  context: InvocationContext
): Promise<HttpResponseInit> => {
  try {
    const users = await getAllUsers();

    if (!users) {
      return {
        status: 404,
        jsonBody: { error: "Users not found" },
      };
    }

    return {
      status: 200,
      jsonBody: { users },
    };
  } catch (error: any) {
    context.log("Error fetching users", error.message);
    return {
      status: 500,
      jsonBody: { error: "Failed to fetch users" },
    };
  }
};

app.http("getLatestUsers", {
  methods: ["GET"],
  route: "users",
  handler: getLatestUsersHandler,
  authLevel: "anonymous",
});
