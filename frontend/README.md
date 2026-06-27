# AI_FloorPlanner

An AI Architect Assistant that collects user requirements, validates them, and generates architectural floor plans (supporting SVG, DXF, and 3D generation).

## Architecture Overview

The application follows a clean, component-based enterprise-grade architecture:

### Frontend Stack
- **Next.js 15 (App Router)**: Provides the React foundation, file-system routing, and server/client component boundaries.
- **TypeScript**: Ensures type safety across models, state, and UI.
- **Tailwind CSS + shadcn/ui**: For utility-first, sleek, dynamic, and responsive styling with theming support.
- **React Hooks & Context**: Centralized state management in `src/store` combined with custom hooks (`useChat.ts`) allows scalable state handling.

### Directory Structure

- `src/app/`: Next.js App Router entry points (`layout.tsx`, `page.tsx`). Global CSS with theme configuration.
- `src/components/`: Modular React components grouped by functionality.
  - `Chat/`: Dedicated to the conversation interface (`ChatContainer`, `WelcomeScreen`, etc.).
  - `Layout/`: App shell components (`Header`, `Sidebar`).
  - `ui/`: Reusable, generic UI primitives (buttons, inputs) inspired by `shadcn/ui`.
- `src/hooks/`: Custom React hooks, including `useChat.ts` which provides the controller layer connecting components to the global store and services.
- `src/services/`: The communication layer handling API requests (`axios` config and `chatService`). This has placeholders to connect to the future FastAPI backend.
- `src/store/`: React Context based global state management (`chatStore.tsx`).
- `src/types/`: Centralized domain models and TypeScript interfaces (`chat`, `floorplan`, `requirement`).
- `src/lib/`: Shared utility functions and constants.

## Setup Instructions

1. `npm install`
2. `npm run dev`

Open [http://localhost:3000](http://localhost:3000) to view it in the browser.
