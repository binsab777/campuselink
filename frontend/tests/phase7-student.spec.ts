import { test, expect } from '@playwright/test';

const BASE_URL = 'http://localhost:3000';

test.describe('Phase 7 - Student Workflows', () => {
  test.beforeEach(async ({ page }) => {
    // Listen for unexpected errors
    page.on('pageerror', error => {
      console.error(`Uncaught exception: "${error}"`);
    });
    
    // Login
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[type="email"]', 'teststudent99@test.com');
    await page.fill('input[type="password"]', 'password');
    await page.click('button:has-text("Sign In")');
    await page.waitForURL('**/dashboard');
  });

  test('Navigate and Verify All Student Pages', async ({ page }) => {
    // 1. Dashboard
    await expect(page.locator('h1')).toContainText('Command Center');
    
    // 2. Profile
    await page.click('text="My Profile"');
    await page.waitForURL('**/dashboard/profile');
    await expect(page.locator('h2').filter({ hasText: 'Basic Information' })).toBeVisible();
    await expect(page.locator('text=Academic History')).toBeVisible();
    await expect(page.locator('text=Skills')).toBeVisible();
    await expect(page.locator('text=Projects')).toBeVisible();
    
    // 3. Jobs & Drives
    await page.click('a:has-text("Jobs & Drives")');
    await page.waitForURL('**/dashboard/jobs');
    await expect(page.locator('h1')).toContainText('Jobs & Drives');
    
    // 4. Readiness & Gaps
    await page.click('text="Readiness & Gaps"');
    await page.waitForURL('**/dashboard/readiness');
    await expect(page.locator('h1')).toContainText('Readiness & Skill Gaps');
    await expect(page.locator('text=7-Dimension Employability')).toBeVisible();
  });

  test('Student Profile CRUD Workflow', async ({ page }) => {
    await page.goto(`${BASE_URL}/dashboard/profile`);
    
    // Create Skill
    await page.click('text="+ Add Skill"');
    await page.waitForSelector('select'); // Ensure modal opens
    await page.selectOption('select', { index: 1 });
    await page.click('button:has-text("Save")');
    await page.waitForTimeout(500); // wait for toast

    // Create Project
    await page.click('text=Add Project');
    await page.fill('input[name="title"]', 'Test E2E Project');
    await page.fill('textarea[name="description"]', 'This is a test project');
    await page.fill('input[name="project_url"]', 'https://github.com/test');
    await page.click('button:has-text("Save")');
    await expect(page.locator('text=Test E2E Project')).toBeVisible();

    // Delete Project (Cleanup)
    const projectRow = page.locator('li', { hasText: 'Test E2E Project' });
    await projectRow.locator('button.text-red-600').click();
    await page.click('button:has-text("Confirm")');
    await expect(page.locator('text=Test E2E Project')).not.toBeVisible();
    
    // Delete Skill (Cleanup)
    // Find the first skill delete button
    const deleteSkillBtn = page.locator('button[title="Delete Skill"]').first();
    await deleteSkillBtn.click();
    await page.click('button:has-text("Confirm")');
    await expect(page.locator('button[title="Delete Skill"]')).toHaveCount(0);
  });
  
  test('Student Authorization Checks', async ({ page }) => {
    // Should block access to admin users
    await page.goto(`${BASE_URL}/dashboard/admin/users`);
    await expect(page.locator('text=403').or(page.locator('text=permission'))).toBeVisible();

    // Should block access to officer students
    await page.goto(`${BASE_URL}/dashboard/students`);
    await expect(page.locator('text=403').or(page.locator('text=permission'))).toBeVisible();
  });
});
