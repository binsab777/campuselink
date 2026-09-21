import { test, expect } from '@playwright/test';

const BASE_URL = 'http://localhost:3000';

test.describe('Platform Admin - User Accounts', () => {
  test('Admin can view user details but cannot update roles', async ({ page }) => {
    // Login as admin
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[type="email"]', 'admin@campuslink.com');
    await page.fill('input[type="password"]', 'password');
    await page.click('button:has-text("Sign In")');
    await page.waitForTimeout(3000);

    // Go to User Accounts
    await page.goto(`${BASE_URL}/dashboard/admin/users`);
    
    // Ensure "Role" button (used for Role Update) is missing
    await expect(page.locator('button:has-text("Role")').first()).not.toBeVisible();
    
    // Ensure "View" button is present
    const viewButton = page.locator('button:has-text("View")').first();
    await expect(viewButton).toBeVisible();
    
    // Click View and verify modal
    await viewButton.click();
    await expect(page.locator('h3:has-text("Account Details")').or(page.locator('h2:has-text("Account Details")'))).toBeVisible();
    
    // Check read-only role display
    await expect(page.locator('span.text-xs.font-semibold.text-gray-500:has-text("System Role")')).toBeVisible();
    
    // Student or Recruiter info should be rendered (depends on which user we clicked, just check if Modal shows up)
    const modalContent = page.locator('.space-y-6');
    await expect(modalContent).toBeVisible();

    await page.screenshot({ path: 'screenshots/admin-view-user.png' });
  });
});
