import { OWNER } from "../config";

const { email: OWNER_EMAIL } = OWNER;

export const getRoles = (email: string) => {
  if (email === OWNER_EMAIL) {
    return "user, analyst, moderator, admin, owner";
  }

  return "user";
};
