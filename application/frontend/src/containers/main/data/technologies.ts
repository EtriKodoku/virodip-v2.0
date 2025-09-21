import vueIcon from "@/assets/images/tech/vue.svg";
import tsIcon from "@/assets/images/tech/typescript.png";
import tailwindIcon from "@/assets/images/tech/tailwindcss.png";
import graphApiIcon from "@/assets/images/tech/microsoft-graph.png";
import azureFuncIcon from "@/assets/images/tech/azure-functions.svg";
import nodeJS from "@/assets/images/tech/node-js.png";
import mongoDB from "@/assets/images/tech/mongo-db.svg";
import azureADB2C from "@/assets/images/tech/azure-ad-b2c.svg";
import type { Tech } from "../types/Tech";

export const technologies: Tech[] = [
  {
    name: "Vue 3",
    imageUrl: vueIcon,
    docsUrl: "https://vuejs.org/",
  },
  {
    name: "TypeScript",
    imageUrl: tsIcon,
    docsUrl: "https://www.typescriptlang.org/",
  },
  {
    name: "Tailwind CSS",
    imageUrl: tailwindIcon,
    docsUrl: "https://tailwindcss.com/docs",
  },
  {
    name: "Azure AD B2C",
    imageUrl: azureADB2C,
    docsUrl: "https://learn.microsoft.com/en-us/azure/active-directory-b2c/",
  },
  {
    name: "Azure Functions",
    imageUrl: azureFuncIcon,
    docsUrl: "https://learn.microsoft.com/en-us/azure/azure-functions/",
  },
  {
    name: "Microsoft Graph API",
    imageUrl: graphApiIcon,
    docsUrl: "https://learn.microsoft.com/en-us/graph/overview",
  },
  {
    name: "Node JS",
    imageUrl: nodeJS,
    docsUrl: "https://nodejs.org/en/docs",
  },
  {
    name: "Mongo DB",
    imageUrl: mongoDB,
    docsUrl: "https://www.mongodb.com/docs/",
  },
];
