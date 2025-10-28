import Admin from "../views/Admin.vue";

export default [
  {
    path: "/admin",
    name: "admin",
    component: Admin,
    meta: {
      requiresAdmin: true,
    },
  },
];
