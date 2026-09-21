# Parity Failure Analysis

## 1. Drive Creation `job_id` Constraint Failure

* **Test Name**: `DriveParityTest::test_recruiter_can_create_drive`
* **Endpoint**: `POST /api/v1/me/drives`
* **FastAPI Behavior**: The Pydantic schema `PlacementDriveBase` requires `job_id: int = Field(..., gt=0)`, `start_time: datetime`, and `end_time: datetime`. The FastAPI endpoint effectively blocks drive creation without a valid job_id and schedule.
* **Laravel Behavior**: The `placement_drives` table enforces `job_id` as `NOT NULL`. However, the scaffolded test omitted `job_id`, `start_time`, and `end_time`, causing a 500 error when the database rightly blocked the invalid insert.
* **Expected Behavior**: Both FastAPI and Laravel schemas strictly require `job_id`.
* **Root Cause**: The testing payload was mock data missing mandatory fields required by the business logic, not a flaw in Laravel's migration. In addition, the scaffolded `RecruiterDriveController` didn't explicitly map `job_id` from the payload to the created drive.
* **Proposed Fix**: 
  1. Rewrite `RecruiterDriveController` to explicitly validate and map `job_id`, `start_time`, and `end_time`.
  2. Rewrite `DriveParityTest` to instantiate a Job first, and pass the `job_id` in the drive creation payload.
* **Affected Files**: `tests/Feature/Recruiters/DriveParityTest.php`, `app/Http/Controllers/Api/RecruiterDriveController.php`

## 2. Admin User Pagination/Count Failure

* **Test Name**: `UserParityTest::test_super_admin_can_list_users`
* **Endpoint**: `GET /api/v1/admin/users`
* **FastAPI Behavior**: Returns a payload structured as `{"total": 4, "users": [...]}` enforcing pagination via `limit` and `offset`.
* **Laravel Behavior**: The scaffolded controller returned `UserResource::collection(User::all())` which evaluates to `{"data": [...]}` (bypassing pagination and wrapping in `data`).
* **Expected Behavior**: The API must return the paginated `{"total": x, "users": [...]}` contract.
* **Root Cause**: The scaffolded `AdminController::index` did not implement pagination and relied on default Laravel Resource wrapping, breaking the contract parity.
* **Proposed Fix**: Rewrite `AdminController::index` to process `limit`/`offset` and return `response()->json(['total' => $total, 'users' => UserResource::collection($users)])`. Update the test to verify `total` and `users` nodes.
* **Affected Files**: `tests/Feature/Admin/UserParityTest.php`, `app/Http/Controllers/Api/AdminController.php`
