import { test, expect } from '@playwright/test';

test('Debug', async ({ page }) => {
  await page.goto('http://localhost:3000/login');
  await page.fill('input[type="email"]', 'admin@campuslink.com');
  await page.fill('input[type="password"]', 'admin123');
  await page.click('button:has-text("Sign In")');
  await page.waitForURL('**/dashboard');
  await page.goto('http://localhost:3000/dashboard/admin/users');
  await page.waitForTimeout(3000);
  await page.screenshot({ path: 'screenshots/debug-admin.png' });
});
