# Azure Admin Page

> A web application for managing authorized users and their roles using Azure AD B2C with Microsoft Graph API or MongoDB backend.

---

> [Live Demo](https://mango-water-0843c520f.1.azurestaticapps.net) 

## Overview

**User Roles Manager** enables secure management of user roles and permissions in Azure AD B2C environments. It provides an admin panel to view authorized users, assign or remove roles, and delete users safely, using either Microsoft Graph API or a custom MongoDB database.

### Key Features:

- View authorized users with detailed profile data;
- Manage user roles with hierarchical permissions (Owner, Admin, Manager, Moderator);
- Remove users with lower privileges securely;
- Role-based route protection and UI visibility;
- Integration with Microsoft Graph API for token enrichment and user data;
- Option to use custom MongoDB backend for flexible role management.

---

## Technologies Used

### Frontend

- **Vue 3 (Composition API)**
- **TypeScript**
- **Tailwind CSS**
- **Azure AD B2C + MSAL.js**

### Backend

- **Azure Functions (Serverless) + TypeScript**
- **MongoDB (optional backend)**
- **Microsoft Graph API**

---

## Infrastructure

- **Azure Static Web Apps**  
  - CI/CD pipeline via GitHub Actions  
  - Unified hosting for frontend and serverless backend  

- **Azure Functions**  
  - Implements backend logic, token claims enrichment, and RBAC enforcement  

- **Microsoft Graph / MongoDB**  
  - Stores user role metadata and synchronization data  

---


