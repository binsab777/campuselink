import { test, expect } from '@playwright/test';

const BASE_URL = 'http://localhost:3000';

test.describe('Phase 7 - Recruiter Workflows', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[type="email"]', 'testrecruiter99@test.com');
    await page.fill('input[type="password"]', 'password');
    await page.click('button:has-text("Sign In")');
    await page.waitForURL('**/dashboard');
  });

  test('Navigate and Verify Recruiter Pages', async ({ page }) => {
    await expect(page.locator('h1')).toContainText('Command Center');
    
    // Go to Portal
    await page.click('text="Open Recruiter Portal"');
    await page.waitForURL('**/dashboard/recruiter');
    await expect(page.locator('h1')).toContainText('Placement Operations Portal');
    
    // Verify tabs
    await expect(page.locator('button:has-text("Job Postings")')).toBeVisible();
    await expect(page.locator('button:has-text("Placement Drives")')).toBeVisible();
    await expect(page.locator('button:has-text("Company Profile")')).toBeVisible();
  });

  test('Recruiter Job CRUD Workflow', async ({ page }) => {
    await page.goto(`${BASE_URL}/dashboard/recruiter`);
    
    // Create Job
    await page.click('button:has-text("+ Create Job Posting")');
    await page.fill('input[name="title"]', 'Phase7 Test Job');
    await page.fill('textarea[name="description"]', 'Looking for Phase7 Engineers');
    await page.selectOption('select[name="employment_type"]', 'Full-time');
    await page.click('button:has-text("Save Job")');
    
    // Read Job
    await expect(page.locator('text=Phase7 Test Job')).toBeVisible();
    
    // Delete Job (Cleanup)
    // Find the job card or row
    const jobCard = page.locator('div.border', { hasText: 'Phase7 Test Job' }).first();
    await jobCard.locator('button:has-text("Delete")').click();
    
    // Accept confirm dialog if it exists, wait playwright auto-accepts dialogs or we might need to handle it.
    // Assuming UI does not use native confirm or we need to handle it:
    // await page.on('dialog', dialog => dialog.accept());
    
    await expect(page.locator('text=Phase7 Test Job')).not.toBeVisible();
  });
  
  test('Recruiter Authorization Checks', async ({ page }) => {
    // Should block access to admin users
    await page.goto(`${BASE_URL}/dashboard/admin/users`);
    await expect(page.locator('text=403').or(page.locator('text=permission'))).toBeVisible();

    // Should block access to readiness
    await page.goto(`${BASE_URL}/dashboard/readiness`);
    await expect(page.locator('text=403').or(page.locator('text=permission'))).toBeVisible();
  });
});
