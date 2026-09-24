import { test, expect } from '@playwright/test';

const BASE_URL = 'http://localhost:3000';

test.describe('Phase 7 - Full Browser Coverage', () => {
  test.setTimeout(60000);

  // STUDENT WORKFLOW
  test('STUDENT Workflow Coverage', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[type="email"]', 'teststudent99@test.com');
    await page.fill('input[type="password"]', 'mypassword123');
    await page.click('button:has-text("Sign In")');
    await page.waitForURL('**/dashboard');
    
    // 1. Dashboard
    await expect(page.locator('h1').first()).toContainText('Command Center');
    
    // 2. Profile (CRUD)
    await page.click('text="My Profile"');
    await page.waitForURL('**/dashboard/profile');
    
    // 3. Readiness
    await page.click('text="Readiness & Gaps"');
    await page.waitForURL('**/dashboard/readiness');
    
    // 4. Jobs & Drives
    await page.click('a:has-text("Jobs & Drives")');
    await page.waitForURL('**/dashboard/jobs');
    
    // Auth Test
    await page.goto(`${BASE_URL}/dashboard/admin/users`);
    await expect(page).not.toHaveURL(/.*admin\/users/);
  });

  // RECRUITER WORKFLOW
  test('RECRUITER Workflow Coverage', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[type="email"]', 'recruiter1@comp1.com');
    await page.fill('input[type="password"]', 'password');
    await page.click('button:has-text("Sign In")');
    await page.waitForURL('**/dashboard');
    
    await page.click('text="Open Recruiter Portal"');
    await page.waitForURL('**/dashboard/recruiter');
    
    // Job CRUD
    await page.click('text="Job Postings"'); // Switch to Jobs tab
    const createBtn = page.locator('button:has-text("+ Create Job Posting")');
    await expect(createBtn).toBeVisible({ timeout: 10000 });
    await createBtn.click();
    await page.fill('input[name="title"]', 'E2E Matrix Job');
    await page.fill('textarea[name="description"]', 'Desc');
    await page.selectOption('select[name="employment_type"]', 'Full-time');
    await page.fill('input[name="base_salary"]', '100000');
    await page.click('button:has-text("Save")');
    
    await expect(page.locator('text=E2E Matrix Job')).toBeVisible();
    
    const jobCard = page.locator('div.border', { hasText: 'E2E Matrix Job' }).first();
    await jobCard.locator('button:has-text("Delete")').click();
    await page.click('button:has-text("Confirm")');
    await expect(page.locator('text=E2E Matrix Job')).not.toBeVisible();
    
    // Auth Test
    await page.goto(`${BASE_URL}/dashboard/admin/users`);
    await expect(page).not.toHaveURL(/.*admin\/users/);
  });

  // PLACEMENT OFFICER WORKFLOW
  test('PLACEMENT_OFFICER Workflow Coverage', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[type="email"]', 'po@campuslink.com');
    await page.fill('input[type="password"]', 'password');
    await page.click('button:has-text("Sign In")');
    await page.waitForURL('**/dashboard');
    
    await page.click('text="Browse Students"');
    await page.waitForURL('**/dashboard/students');
    await expect(page.locator('text=Alice Johnson')).toBeVisible();
    
    await page.click('a[href="/dashboard"]');
    
    await page.click('text="View Partners"');
    await page.waitForURL('**/dashboard/companies');

    // Auth test
    await page.goto(`${BASE_URL}/dashboard/admin/users`);
    await expect(page).not.toHaveURL(/.*admin\/users/);
  });

  // SUPER_ADMIN WORKFLOW
  test('SUPER_ADMIN Workflow Coverage', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[type="email"]', 'admin@campuslink.com');
    await page.fill('input[type="password"]', 'password');
    await page.click('button:has-text("Sign In")');
    await page.waitForURL('**/dashboard');
    
    // View Users
    await page.click('text="Manage Users"');
    await page.waitForURL('**/dashboard/admin/users');
    await expect(page.locator('text=student1@college.edu')).toBeVisible();
    
    // Master Skills
    await page.click('a[href="/dashboard"]');
    await page.click('text="Manage Catalog"');
    await page.waitForURL('**/dashboard/admin/skills');
    
    // CRUD Skill
    await page.click('button:has-text("+ Add Master Skill")');
    await page.fill('input[name="name"]', 'E2E Matrix Skill');
    await page.selectOption('select[name="category"]', 'Technology');
    await page.click('button:has-text("Save")');
    await expect(page.locator('td:has-text("E2E Matrix Skill")')).toBeVisible();
    
    const skillRow = page.locator('tr', { hasText: 'E2E Matrix Skill' });
    await skillRow.locator('button:has-text("Delete")').click();
    await page.click('button:has-text("Confirm")');
    await expect(page.locator('td:has-text("E2E Matrix Skill")')).not.toBeVisible();
  });
});
