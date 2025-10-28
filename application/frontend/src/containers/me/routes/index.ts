import Me from "../views/Me.vue";

export default [
  {
    path: "/me",
    name: "me",
    component: Me,
    meta: {
      requiresAuth: true,
    },
  },
];
