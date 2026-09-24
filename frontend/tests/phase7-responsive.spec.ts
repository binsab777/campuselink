import { test, expect } from '@playwright/test';

const BASE_URL = 'http://localhost:3000';

const VIEWPORTS = [
  { name: 'Desktop', width: 1440, height: 900 },
  { name: 'Tablet', width: 768, height: 1024 },
  { name: 'Mobile', width: 375, height: 667 },
];

for (const vp of VIEWPORTS) {
  test(`Responsive Layout Test - ${vp.name}`, async ({ page }) => {
    await page.setViewportSize({ width: vp.width, height: vp.height });

    // Test Login Page Responsive
    await page.goto(`${BASE_URL}/login`);
    await expect(page.locator('text="Sign in to your account"')).toBeVisible();

    // Login as Admin
    await page.fill('input[type="email"]', 'admin@campuslink.com');
    await page.fill('input[type="password"]', 'password');
    await page.click('button:has-text("Sign In")');
    await page.waitForURL('**/dashboard');

    // Dashboard Responsive
    await expect(page.locator('text="Command Center"').first()).toBeVisible();

    // Users Directory Responsive
    await page.click('text="Manage Users"');
    await page.waitForURL('**/dashboard/admin/users');
  });
}
