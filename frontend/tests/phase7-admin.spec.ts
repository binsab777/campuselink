import { test, expect } from '@playwright/test';

const BASE_URL = 'http://localhost:3000';

test.describe('Phase 7 - Admin & Officer Workflows', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[type="email"]', 'admin@campuslink.com');
    await page.fill('input[type="password"]', 'password');
    await page.click('button:has-text("Sign In")');
    await page.waitForURL('**/dashboard');
  });

  test('Super Admin User Accounts Workflow', async ({ page }) => {
    // Go to User Accounts
    await page.click('text="User Accounts"');
    await expect(page.locator('h1')).toContainText('User Accounts');
    
    // Check data representations
    await expect(page.locator('text=student1@college.edu')).toBeVisible();
    await expect(page.locator('text=recruiter1@comp1.com')).toBeVisible();
    
    // View Modal Parity Check
    const viewButton = page.locator('tr', { hasText: 'student1@college.edu' }).locator('button:has-text("View")');
    await viewButton.click();
    
    // Wait for modal
    await expect(page.locator('text=Account Details')).toBeVisible();
    await expect(page.locator('text=student1@college.edu')).toBeVisible();
    await expect(page.locator('text=Student Profile Information')).toBeVisible();
    await expect(page.locator('text=Academic History')).toBeVisible();
    
    // Test Resume Link exists
    await expect(page.locator('text=View Resume Document')).toBeVisible();
    
    // Close modal
    await page.click('button:has-text("Close")');
    await expect(page.locator('text=Account Details')).not.toBeVisible();
  });

  test('Master Skills QA', async ({ page }) => {
    await page.click('text="Master Skills"');
    await expect(page.locator('h1')).toContainText('Skills Catalog');
    
    // Create Skill
    await page.click('button:has-text("Add Skill")');
    await page.fill('input[name="name"]', 'Phase7 Test Skill');
    await page.selectOption('select[name="category"]', 'Technology');
    await page.click('button:has-text("Save")');
    
    await expect(page.locator('td:has-text("Phase7 Test Skill")')).toBeVisible();
    
    // Cleanup
    const skillRow = page.locator('tr', { hasText: 'Phase7 Test Skill' });
    await skillRow.locator('button:has-text("Delete")').click();
    await page.click('button:has-text("Confirm")'); // Assuming the confirm dialog has a Confirm button
    
    await expect(page.locator('td:has-text("Phase7 Test Skill")')).not.toBeVisible();
  });
});

test.describe('Phase 7 - Officer Workflows', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[type="email"]', 'po@campuslink.com');
    await page.fill('input[type="password"]', 'password');
    await page.click('button:has-text("Sign In")');
    await page.waitForURL('**/dashboard');
  });

  test('Officer View Students and Companies', async ({ page }) => {
    // Check Students
    await page.goto(`${BASE_URL}/dashboard/students`);
    await expect(page.locator('h1')).toContainText('Student Placement Directory');
    await expect(page.locator('text=Alice Johnson')).toBeVisible();
    
    // Check Companies
    await page.goto(`${BASE_URL}/dashboard/companies`);
    await expect(page.locator('h1')).toContainText('Companies');
    await expect(page.locator('text=comp1.com')).toBeVisible();
  });

  test('Officer Blocked from Users', async ({ page }) => {
    await page.goto(`${BASE_URL}/dashboard/admin/users`);
    await expect(page.locator('text=403').or(page.locator('text=permission'))).toBeVisible();
  });
});
