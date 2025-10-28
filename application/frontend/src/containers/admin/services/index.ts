import { useAuthStore } from "@/stores/useAuthStore";
import { storeToRefs } from "pinia";

import {
  get_user,
  edit_user_roles,
  delete_user,
} from "@/containers/admin/api/index";

import type { GetUserResponseData } from "@/containers/admin/types";
import { stringifyRoles } from "@/helpers/roleConverters";

export const getUser = async (id: string) => {
  const { bearerToken } = storeToRefs(useAuthStore());

  const response = await fetch(get_user(id), {
    headers: {
      Authorization: `Bearer ${bearerToken.value}`,
    },
  });

  if (!response.ok) {
    return {
      errorStatus: response.status,
    };
  }

  const data = (await response.json()) as GetUserResponseData;

  return data;
};

export const editUserRoles = async (id: string, roles: string[]) => {
  const { bearerToken } = storeToRefs(useAuthStore());

  const response = await fetch(edit_user_roles(id), {
    method: "POST",
    headers: {
      Authorization: `Bearer ${bearerToken.value}`,
    },
    body: JSON.stringify({
      newRoles: stringifyRoles(roles),
    }),
  });

  if (!response.ok) {
    return response.status;
  }
};

export const deleteUser = async (id: string) => {
  const { bearerToken } = storeToRefs(useAuthStore());

  const response = await fetch(delete_user(id), {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${bearerToken.value}`,
    },
  });

  return response.status;
};
