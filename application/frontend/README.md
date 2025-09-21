# Azure Admin Page — Frontend

> A Vue 3 + TypeScript web application for managing user roles in Azure AD B2C via Microsoft Graph API and a custom backend.

---

## Overview

This frontend provides:

- Authentication via Azure AD B2C using MSAL.js.
- Viewing user token claims on the "Me" page.
- Browsing and searching the list of users.
- Managing roles and users on the "Admin" page (accessible with proper permissions).
- Route protection based on roles encoded in the token.
- Support for two role management strategies: via Microsoft Graph API or a custom backend with MongoDB.
- Modular architecture.
- Pinia for state management
- Localization support via Vue i18n.
- Toast notification system for user feedback.

---

## Technologies

- **Vue 3** (Composition API)
- **TypeScript**
- **Vue Router**
- **Pinia**
- **Tailwind CSS**
- **MSAL.js**
- **Vue i18n**
- **Custom Toast Notifications**

---

## Local Setup

1. Clone the repository and navigate to the frontend folder:

   ```bash
   git clone https://github.com/ygyubyv/azure-admin-page.git
   cd frontend

2. Install dependencies:

   ```bash
   npm install
   ```

3. Run the development server:

   ```bash
   npm run dev
   ```
