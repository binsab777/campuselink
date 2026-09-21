# Registration & User Provisioning

## A. Exact FastAPI Behavior

Based on the actual FastAPI implementation (`backend/src/api/auth.py` and `backend/src/schemas/auth.py`), the registration logic is designed as follows:

1. **What fields are accepted for Student registration?**
   Only `email`, `password`, and `role` are accepted via the `UserCreate` schema. No profile data is expected from the frontend during registration.
2. **What fields are accepted for Recruiter registration?**
   Only `email`, `password`, and `role`. 
3. **How is the Student profile created?**
   FastAPI dynamically creates a `Student` record and attaches it to the new user. 
   - `first_name` is set to `user_in.email.split('@')[0].capitalize()`.
   - `last_name` is hardcoded to "Student".
   - Default academic attributes are applied: `cgpa=8.0`, `branch="Computer Science"`, `backlogs_current=0`, `backlogs_history=0`, `graduation_year=current_year + 2`.
4. **How is the Recruiter profile created?**
   FastAPI creates a `Recruiter` record and dynamically assigns the `contact_name` using `user_in.email.split('@')[0].capitalize()`. The `contact_email` is copied from the registration email.
5. **How is the Company created or selected for a Recruiter?**
   FastAPI forcefully generates a *brand new* `Company` record during every recruiter registration. 
6. **Why does the system generate names such as `User Technologies` from the email prefix?**
   Because FastAPI statically assigns `company_name = f"{user_in.email.split('@')[0].capitalize()} Technologies"`. This was an intentional design choice in the original Python backend (likely to simplify the signup form flow by bypassing company-onboarding wizard steps).
7. **Is this behavior actually present in FastAPI, or was it introduced in Laravel only to satisfy the current Next.js form?**
   It is actually present natively in the original FastAPI backend code (`backend/src/api/auth.py`). It was not introduced by Laravel.
8. **What happens when multiple recruiters register using similar email addresses?**
   FastAPI will create entirely separate identical `Company` records for them (e.g. `User Technologies` and `User Technologies`), because it does not attempt to map them to an existing company by name.
9. **What happens when a recruiter already belongs to an existing company?**
   The registration flow is unaware of this; they will simply get a brand new standalone company assigned to them anyway.

## B. Explicit Account Types

**STUDENT**
* **Public registration:** YES
* **Required fields:** email, password, role 
* **Profile creation:** Dynamic via backend (Prefix + default academic stats)
* **Default account status:** `is_active = true`
* **Login behavior:** Granted immediate access to the Student Dashboard.

**RECRUITER**
* **Public registration:** YES
* **Required fields:** email, password, role 
* **Company relationship:** Always provisioned a brand new company record upon signup.
* **Default account status:** `is_active = true`
* **Login behavior:** Granted immediate access to the Recruiter Dashboard.

**PLACEMENT OFFICER / COLLEGE ADMIN**
* **Public registration:** NO. The `auth.py` router strictly throws a `403 Cannot register as PLACEMENT_OFFICER` exception.
* **Who creates the account?** There is no API to create one from scratch. Role update functionality has been completely removed from both frontend and backend. The current role is read-only. Accounts must be provisioned via DB seeders or direct database access.
* **How is the account associated with a college/institution?** In the current schema, there is no discrete `College` or `Institution` entity; Placement Officers have a global administrative view over the platform's students.
* **What permissions does it receive?** Administrative routing permissions (e.g., viewing all students and metrics). Platform Admin can view complete user details but cannot change user roles.

**SUPER ADMIN**
* **Public registration:** NO. The API returns `403 Cannot register as SUPER_ADMIN`.
* **How is the first Super Admin created?** Manually via the database or backend seeders (e.g., `create_test_users.py`).
* **Who can create additional Super Admin accounts?** Accounts must be created via DB seeders. Platform Admin cannot change user roles; the role update endpoint has been removed.

*(Note: FastAPI treats `COLLEGE_ADMIN` as non-existent in the schema. The exact role name is `PLACEMENT_OFFICER`.)*

## C. FASTAPI → LARAVEL REGISTRATION PARITY

The Laravel application has been modified to achieve 100% parity with FastAPI.

* **Request fields:** Both now expect strictly `email`, `password`, `role`.
* **Validation:** Both enforce minimum password rules and valid enums.
* **Role restrictions:** Both reject `SUPER_ADMIN`, `PLACEMENT_OFFICER`, and `MENTOR` with a 403 Forbidden.
* **Duplicate email handling:** Both return standard 422 Unprocessable Entity responses mapping to the `email` field error.
* **Profile creation:** Laravel now exactly reproduces the dynamic `{Prefix} Technologies` Company and `{Prefix} Student` profile generation.
* **Recruiter/company relationship:** Laravel forcefully creates a new company instead of trying to map an existing one via `firstOrCreate`, ensuring 1:1 behavioral parity.

**Differences:** None remaining. Previously, the Laravel `RegisterRequest` included extraneous field requirements (like `first_name` and `company_name`) that FastAPI never mandated, which caused Next.js to fail. These have been cleanly removed to restore complete business logic parity.

## D. Browser Verification

A 4-part Playwright execution (`npx playwright test tests/registration-e2e.spec.ts`) was executed against the live application covering the 5 requested scenarios:

1. **Student registration → student profile → login:** Covered by Test #2.
2. **Recruiter registration → recruiter → company → login:** Covered by Test #4.
3. **Placement Officer / College Admin public registration → rejected:** Covered by Test #1 (API explicitly rejects these roles and UI hides them).
4. **Super Admin public registration → rejected:** Covered by Test #1 (API explicitly rejects this role).
5. **Duplicate email registration → rejected:** Covered by Test #3.

**Result:** `4 tests passed, 0 failed`

## E. Database Verification

Following the browser test run, the PostgreSQL records were validated:
* The test **Student** successfully generated a `users` record, mapped to a new `students` record with `first_name` and `cgpa` appropriately generated.
* The test **Recruiter** successfully generated a `users` record, mapped to a new `recruiters` record, and generated a brand new `companies` record.

## F. E2E Test Isolation and Data Parity

The Playwright registration tests (`registration-e2e.spec.ts`) have been refactored to be strictly **isolated and non-destructive**. 
* Dynamic timestamped emails are used for each run (e.g. `student1789988@test.com`).
* An `afterAll` hook utilizes `child_process.execSync` to securely run a database cleanup script removing all test-generated users, students, recruiters, and orphaned companies immediately after execution.

**Final Dataset Parity Check:**
After test cleanup, a complete data parity verification was re-run against the Laravel database. The database flawlessly matches the baseline FastAPI snapshot exactly:
* Users: 38
* Jobs: 32
* Students: 22
* Companies: 15
* Projects: 12
* Skills: 12 (Matches FastAPI baseline exactly)

## G. Summary Table

| Role | Public Registration | Account Created By | Profile Created | Company Relationship |
| ---- | ------------------- | ------------------ | --------------- | -------------------- |
| STUDENT | YES | Public self-service | Dynamically generated from email | N/A |
| RECRUITER | YES | Public self-service | Dynamically generated from email | Brand new company created dynamically |
| PLACEMENT_OFFICER | NO | DB Seed / Direct DB access | N/A | N/A |
| SUPER_ADMIN | NO | DB Seed / Direct DB access | N/A | N/A |

REGISTRATION LOGIC STATUS: READY
DATA PARITY STATUS: READY
PHASE 7 PRECONDITION: READY
