export const get_user = (id: string) => {
  return `https://azure-admin-page.azurewebsites.net/api/users/${id}`;
};

export const edit_user_roles = (id: string) => {
  return `https://azure-admin-page.azurewebsites.net/api/users/${id}/roles`;
};

export const delete_user = (id: string) => {
  return `https://azure-admin-page.azurewebsites.net/api/users/${id}`;
};
