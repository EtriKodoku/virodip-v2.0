# Azure Admin Page — Backend

> Backend service for managing user roles and claims in Azure AD B2C environment. Supports two versions: Microsoft Graph API-based and custom database-based.

---

## Overview

This backend handles secure management of user roles and access control metadata for the User Roles Manager application. It integrates with Azure AD B2C and supplements it with either direct Microsoft Graph API calls or a custom backend database.

Two distinct approaches are implemented:

1. **Microsoft Graph API version** — roles and claims are managed directly within Azure AD B2C via Microsoft Graph API.
2. **Custom Database version** — roles and claims are stored in an external database (MongoDB) and synchronized with Azure AD B2C.

---

## Versions & Technologies

### 1. Microsoft Graph API Version

- **Technologies**: Node.js, TypeScript, Azure Functions, Microsoft Graph API
- **Description**: Roles and other claims are managed directly in Azure Active Directory Business to Consumer and can be retrieved either from the ID token or dynamically via Microsoft Graph API.
- **Pros**:
  - No need to maintain a separate database for role storage.
  - Supports SSO out of the box: Users can seamlessly access multiple applications under one tenant with the same login.
  - Security through token-based access: queries require valid access tokens, improving control and traceability.
  - Centralized identity and access management within Azure ecosystem.
  - High stability and scalability: Microsoft Graph API is hosted on Azure's robust infrastructure, designed to handle large-scale traffic reliably.
- **Cons**:
  - Custom claims require globally unique names — this can become confusing across multiple apps.
  - SSO maintenance complexity: Removing a user deletes them from all tenant applications, complicating user lifecycle management.
  - Limited flexibility: Custom mappings or logic require advanced Entra configuration or external tools.
  - Microsoft Graph API performance is slow, even for basic queries. This impacts UX, especially during login flows.
  - Microsoft Graph for Azure AD B2C offers very limited support for filtering, sorting, or pagination of user data.
- **When to Use:**
  - Your application only needs a small amount of identity metadata (e.g., 1–2 fields like role).
  - You want to avoid managing your own user database and rely solely on Azure.
  - Security and centralized control are more important than performance or query flexibility.

### 2. Custom Database Version

- **Technologies**: Node.js, TypeScript, Azure Functions, MongoDB
- **Description**: Users and roles are stored in your own backend database — in our case, MongoDB — synchronized with Azure Active Directory Business to Consumer during user creation. This approach is highly recommended for production-grade applications where performance and flexibility are critical.
- **Pros**:
  - Extremely fast: ~40-70ms response time vs 400–1500ms from Graph API.
  - Maximum flexibility: Full control over queries, filtering, pagination, or even GraphQL if desired.
  - Easy integration of custom claims: Any additional data or rules can be injected from the backend.
  - Supports advanced use cases: Role-based access, permissions, multi-tenancy, etc.
  - Simplifies testing and maintenance: Everything is under your control.
- **Cons**:
  - Requires extra backend logic: Syncing users on creation.
  - Lower security by default: You’re responsible for securing endpoints and preventing data leaks.
  - Potential for overload: Unlike Graph API, performance under high load depends on your infrastructure.
- **When to Use:**
  - You need a fast, flexible, and scalable user management system.
  - You want to decouple user logic from the identity provider.
  - Your users have many custom fields or app-specific metadata.
  - You want full control over role resolution and permissions logic.
---

## Local Setup

1. Clone the repository and navigate to the backend folder:

   ```bash
   git clone https://github.com/ygyubyv/azure-admin-page.git
   cd backend
   cd <version>
   
2. Install dependencies:

   ```bash
   npm install
   ```

3. Run functions locally:

   ```bash
   npm start
   ```
  
