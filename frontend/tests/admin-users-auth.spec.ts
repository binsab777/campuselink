import { test, expect } from '@playwright/test';

const BASE_URL = 'http://localhost:3000';

test.describe('Platform Admin - Access Control Verification', () => {
  test('Student is blocked from admin users page', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[type="email"]', 'student1@college.edu');
    await page.fill('input[type="password"]', 'password');
    await page.click('button:has-text("Sign In")');
    await page.waitForTimeout(3000);

    // Try going to admin/users
    await page.goto(`${BASE_URL}/dashboard/admin/users`);
    
    // Check if it redirects or shows unauthorized
    await expect(page.locator('text=403 Forbidden').first()).toBeVisible({ timeout: 5000 });
  });

  test('Recruiter is blocked from admin users page', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[type="email"]', 'recruiter1@comp1.com');
    await page.fill('input[type="password"]', 'password');
    await page.click('button:has-text("Sign In")');
    await page.waitForTimeout(3000);

    // Try going to admin/users
    await page.goto(`${BASE_URL}/dashboard/admin/users`);
    
    await expect(page.locator('text=403 Forbidden').first()).toBeVisible({ timeout: 5000 });
  });
});
