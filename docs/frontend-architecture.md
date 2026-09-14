# CAMPUSLINK Frontend Component Architecture

## 1. Executive Summary

This document establishes the scalable, reusable frontend component architecture for the **CAMPUSLINK** platform. Built with **Next.js 16 (App Router)**, **React 19**, and **Tailwind CSS 4**, the frontend follows a strict separation of concerns that maximizes reuse, ensures predictable state flow, and provides uniform validation error mapping across student and recruiter workflows.

---

## 2. High-Level Architecture Diagram

```
       ┌────────────────────────────────────────────────────────┐
       │                 Page Routes (Next.js)                  │
       │       app/dashboard/profile/page.tsx                   │
       │       app/dashboard/recruiter/page.tsx                 │
       │       app/dashboard/readiness/page.tsx                 │
       └───────────────────────────┬────────────────────────────┘
                                   │ (Composes domain features)
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │               Domain Feature Components                │
       │   features/students/* (Modals, Completeness, Resume)   │
       │   features/recruiters/* (Modals, Sandbox, Requisitions)│
       │   features/readiness/* (Gauge, Dimensions, Skill-Gap)  │
       └───────────────────────────┬────────────────────────────┘
                                   │ (Utilizes reusable primitives)
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │             Shared UI & Form Primitives                │
       │   components/ui/* (Button, Input, Modal, Badge, Card)  │
       │   components/forms/* (FormField, FormError)            │
       │   components/feedback/* (LoadingState, EmptyState)     │
       │   components/layout/* (AppLayout, PageHeader)          │
       └───────────────────────────┬────────────────────────────┘
                                   │ (Invokes type-safe endpoints)
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │              Centralized API Service Layer             │
       │   services/apiClient.ts (Unified Fetch & 422 Parser)   │
       │   services/studentsApi.ts, recruitersApi.ts, etc.      │
       └───────────────────────────┬────────────────────────────┘
                                   │ (HTTP / JSON / JWT)
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                 FastAPI Backend Engine                 │
       │            Pydantic V2 Schemas & Database              │
       └────────────────────────────────────────────────────────┘
```

---

## 3. Directory Structure

```
frontend/src/
├── app/
│   ├── dashboard/
│   │   ├── profile/
│   │   │   └── page.tsx              # Thin orchestrator (< 450 LOC)
│   │   ├── recruiter/
│   │   │   └── page.tsx              # Thin orchestrator (< 430 LOC)
│   │   ├── readiness/
│   │   │   └── page.tsx              # Thin orchestrator (< 150 LOC)
│   │   └── page.tsx                  # Dashboard command center
│   ├── login/
│   │   └── page.tsx                  # Authenticated login form
│   ├── unauthorized/
│   │   └── page.tsx                  # 403 Forbidden screen
│   ├── globals.css                   # Global Tailwind CSS styles
│   └── layout.tsx                    # Root Next.js layout
│
├── components/
│   ├── ui/                           # Atoms and molecules
│   │   ├── Button.tsx                # Variants: primary, secondary, danger, outline, ghost
│   │   ├── Input.tsx                 # Standard input with hasError state
│   │   ├── Textarea.tsx              # Multi-line input with hasError state
│   │   ├── Select.tsx                # Native select wrapper with styling
│   │   ├── Checkbox.tsx              # Accessible checkbox with description
│   │   ├── Card.tsx                  # Container card with title, action slot, footer
│   │   ├── Tabs.tsx                  # Accessible tab bar with count indicators
│   │   ├── StatusBadge.tsx           # Semantic status indicator
│   │   ├── Modal.tsx                 # Accessible dialog with ESC, click-outside, backdrop
│   │   └── ConfirmDialog.tsx         # Destructive action confirmation dialog
│   ├── forms/
│   │   ├── FormField.tsx             # Label, required indicator, helper, error message
│   │   └── FormError.tsx             # General server-side error alert
│   ├── feedback/
│   │   ├── LoadingState.tsx          # Spinner with contextual message
│   │   ├── EmptyState.tsx            # Placeholder for missing or empty lists
│   │   ├── ErrorState.tsx            # Failed request card with retry action
│   │   └── Toast.tsx                 # Notification banner with auto-dismiss
│   ├── layout/
│   │   ├── AppLayout.tsx             # Authenticated shell, navbar, role badge, logout
│   │   └── PageHeader.tsx            # Title, subtitle, back link, action buttons
│   └── ProtectedRoute.tsx            # Client-side RBAC guard
│
├── features/                         # Domain-specific feature modules
│   ├── students/
│   │   ├── types.ts                  # TypeScript interfaces for students
│   │   ├── BasicInfoModal.tsx        # Personal, contact, and CGPA editor
│   │   ├── LinksModal.tsx            # LinkedIn, GitHub, and target roles
│   │   ├── AcademicModal.tsx         # Academic degrees and scores
│   │   ├── SkillModal.tsx            # Technical skills and proficiency
│   │   ├── ProjectModal.tsx          # Capstone and applied projects
│   │   ├── CertModal.tsx             # Industry certifications
│   │   ├── ResumeCard.tsx            # Resume PDF viewer and uploader
│   │   ├── CompletenessCard.tsx      # Profile completeness progress indicator
│   │   └── AssessmentsCard.tsx       # Standardized evaluation scores
│   ├── recruiters/
│   │   ├── types.ts                  # TypeScript interfaces for recruiters
│   │   ├── CompanyModal.tsx          # Company details and profile editor
│   │   ├── JobModal.tsx              # Job posting & eligibility configuration
│   │   ├── JobRequirementsModal.tsx  # Skill weighting and mandatory flags
│   │   ├── DriveModal.tsx            # Placement drive event scheduler
│   │   └── EligibilitySandboxCard.tsx# Live candidate eligibility preview
│   └── readiness/
│       ├── types.ts                  # TypeScript interfaces for readiness engine
│       ├── ReadinessScoreCard.tsx    # Overall score gauge and recalculate action
│       ├── DimensionsBreakdownCard.tsx# 7-dimension weighted progress breakdown
│       ├── StrengthsWeaknessesCard.tsx# Identified competitive advantages & gaps
│       └── SkillGapTable.tsx         # Target job side-by-side gap table
│
├── services/                         # Centralized API layer
│   ├── apiClient.ts                  # Unified HTTP client, JWT header, 422 parser
│   ├── studentsApi.ts                # Student profile endpoints
│   ├── recruitersApi.ts              # Recruiter, job, drive, and eligibility endpoints
│   └── readinessApi.ts               # Readiness evaluation and skill-gap endpoints
│
└── context/
    └── AuthContext.tsx               # Authentication state, login, logout, token
```

---

## 4. Shared UI Components Catalog

| Component | Responsibility | Props & Capabilities |
| :--- | :--- | :--- |
| `Button` | Standard button primitive | `variant` (`primary`, `secondary`, `danger`, `outline`, `ghost`), `size` (`sm`, `md`, `lg`), `loading`, `disabled`. |
| `Input` | Text/number/date input | Accepts standard input attributes, `hasError` for visual `border-rose-500` highlighting. |
| `Textarea` | Multi-line text field | `rows`, `hasError`, forwardRef support. |
| `Select` | Dropdown selector | Accepts either `options` array or custom JSX `children`, `hasError`. |
| `Checkbox` | Checkbox input | `label`, `description`, `hasError`. |
| `Card` | Uniform content card | `title`, `subtitle`, `action`, `footer`, `padding` (`none`, `sm`, `md`, `lg`). |
| `Tabs` | Horizontal tab navigation | `tabs: TabItem[]`, `activeKey`, `onChange`, pill badge count support. |
| `StatusBadge` | Semantic status tag | `status`, `variant` (`auto`, `success`, `info`, `warning`, `danger`, `purple`, `neutral`), `size`. |
| `Modal` | Accessible dialog window | `isOpen`, `onClose`, `title`, `subtitle`, `size` (`sm` to `3xl`), `footer`. Handles ESC and click-outside. |
| `ConfirmDialog`| Destructive action confirmation | Built on `Modal` with `title`, `message`, `onConfirm`, `confirmText`, `loading`. |
| `FormField` | Form field layout container | Wraps any input with `label`, required indicator `*`, `error` text, `helperText`. |
| `FormError` | Form-level alert banner | Displays server error message with dismiss button. |
| `LoadingState` | Centered loading spinner | Custom message placeholder with spinner animation. |
| `EmptyState` | Empty list placeholder | `icon`, `title`, `description`, optional `actionText` & `onAction`. |
| `ErrorState` | Request failure placeholder | Failed network/server display with `onRetry` button. |
| `Toast` | Dismissable alert notification | `message`, `type` (`success`, `error`, `info`), auto-dismiss timer. |
| `PageHeader` | Standardized page heading | `title`, `subtitle`, `backHref`, `backLabel`, `actions` slot. |
| `AppLayout` | Authenticated shell | Wraps `ProtectedRoute`, persistent top navigation, user profile, role badge, logout. |

---

## 5. Form Architecture & Validation Strategy

1. **Pre-Submission Instant UX Validation:**
   - Every feature modal validates fields locally before dispatching HTTP requests.
   - Any validation failure updates `fieldErrors: Record<string, string>`.
   - Inputs receiving errors display `border-rose-500` and an explainable message underneath via `FormField`.

2. **Centralized Backend 422 Normalization:**
   - FastAPI returns Pydantic V2 validation errors in `{"detail": [{"loc": ["body", "field_name"], "msg": "..."}]}` format.
   - `services/apiClient.ts` intercepts this via `parseApiError`:
     ```typescript
     export function parseApiError(error: any): NormalizedApiError {
       // Extracts detail[0].msg as main banner error
       // Maps err.loc[last] -> fieldErrors[field]
     }
     ```
   - Forms simply catch `err` and execute:
     ```typescript
     const parsed = parseApiError(err);
     setFormError(parsed.message);
     setFieldErrors(parsed.fieldErrors);
     ```

3. **Cancel & Reset Behavior:**
   - Closing or cancelling a modal flushes `fieldErrors` and reverts inputs back to existing saved state without residual validation errors.

---

## 6. API Service & Data-Fetching Architecture

1. **Zero Raw Fetch in Components:**
   - Components never assemble manual `fetch("http://localhost:8000/...")` calls or attach manual `Authorization: Bearer` headers.
   - All network interaction is mediated through domain service objects:
     - `studentsApi`: Profile, academic history, skills, projects, certifications, resume upload.
     - `recruitersApi`: Company profile, job postings, requirements, placement drives, candidate eligibility sandbox.
     - `readinessApi`: Multidimensional readiness evaluation, recalculation, job skill-gap analysis.

2. **Unified Base URL & Environment Handling:**
   - Configurable via `NEXT_PUBLIC_API_URL` environment variable, defaulting safely to `http://localhost:8000`.

---

## 7. State Management Approach

- **Local State (`useState`):** Form input buffers, modal visibility toggles, loading and field error records remain encapsulated within their respective feature modal components.
- **Global Context (`AuthContext`):** Current authenticated user details, JWT access/refresh tokens, and login/logout lifecycle.
- **Data Flow:**
  - Parent page loads initial data via domain service (`studentsApi.getProfile()`).
  - Child modals receive initial item data and invoke `onSuccess()` callback when mutations complete.
  - Parent page re-fetches or updates state reactively and triggers a `Toast` notification.

---

## 8. Component Reuse Principles

1. **High Reuse, Clear Responsibilities:**
   - Generic UI patterns (inputs, buttons, cards, dialogs, badges) belong in `components/ui/` or `components/forms/`.
   - Domain logic (e.g., job eligibility rules, academic scoring types) belongs in dedicated feature modules (`features/students/`, `features/recruiters/`).
2. **Avoid Mega-Form Over-Abstraction:**
   - We do not create a 1,000-line "UniversalDynamicForm" that tries to generate all forms from JSON configurations. Each domain modal retains explicit, readable JSX and tailored validation rules, while sharing UI atoms.
3. **No Business Logic in Generic Primitives:**
   - `Button`, `Modal`, `FormField`, etc., have zero knowledge of students, recruiters, or backend endpoints.

---

## 9. Verification & Compliance Checklist

- [x] All repeated UI patterns refactored into `components/ui/`, `components/forms/`, `components/feedback/`, `components/layout/`.
- [x] Monolithic page sizes reduced:
  - `profile/page.tsx`: Reduced from **2,604 LOC** to **~430 LOC** (-83%).
  - `recruiter/page.tsx`: Reduced from **1,965 LOC** to **~420 LOC** (-78%).
  - `readiness/page.tsx`: Reduced from **530 LOC** to **~150 LOC** (-72%).
- [x] Unified API client with automatic token injection and FastAPI 422 error normalization.
- [x] Next.js 16 build succeeds with **0 TypeScript errors** (`npm run build`).
- [x] Backend test suite passes **51/51 tests** (`pytest backend/tests/ -v`).
