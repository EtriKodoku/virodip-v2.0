import { HttpRequest } from "@azure/functions";
import { BASIC_AUTH } from "../config";

export const checkBasicAuth = (request: HttpRequest): boolean => {
  const authHeader = request.headers.get("authorization");
  if (!authHeader || !authHeader.startsWith("Basic ")) return false;

  const base64Credentials = authHeader.split(" ")[1];
  const [username, password] = Buffer.from(base64Credentials, "base64")
    .toString("utf-8")
    .split(":");

  const { username: BasicUsername, password: BasicPassword } = BASIC_AUTH;
  return username === BasicUsername && password === BasicPassword;
};
