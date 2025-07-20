# Frontend Architecture Overview

## Overview
This frontend provides a modern web chat interface for the Knowledge Management System (KMS), allowing users to upload documents, ask questions, and view answers with source citations. It is built with Next.js and React, following best practices for separation of concerns and maintainability.

---

## Key Components

### 1. API Client (`frontend/lib/api.ts`)
- Centralizes all HTTP requests to the backend API.
- Exposes methods for document management, chat, and health checks.
- All API logic is contained here.

### 2. Custom Hooks
- **`use-chat` (`frontend/hooks/use-chat.ts`)**
  - Manages chat state, message history, and API calls for sending/receiving messages.
  - Handles loading and error states for chat.
- **`use-documents` (`frontend/hooks/use-documents.ts`)**
  - Manages document list, upload, and deletion.
  - Handles loading, upload progress, and error states for documents.

### 3. UI Components
- **Presentational and stateless.**
- **`ChatArea`**: Renders chat messages, input, and formatting.
- **`Sidebar`**: Displays document list, upload, and delete actions.
- **Other UI components**: Buttons, inputs, progress bars, etc., are reused from the `components/ui/` directory.

### 4. Page Composition
- **`page.tsx`**: Orchestrates the UI using hooks and passes state/handlers to components.

---

## Best Practices
- **Separation of concerns:** API logic in the API client, state management in hooks, UI in presentational components.
- **Consistent error/loading handling:** All hooks and components use standardized patterns for error, loading, and progress states.
- **Stateless UI components:** Components receive all data and handlers via props.

---

## Contributor Onboarding
- See the main project README for setup instructions.
- To add new features, extend hooks or components as needed, keeping logic and presentation separate.
- Keep API logic centralized in the API client. 