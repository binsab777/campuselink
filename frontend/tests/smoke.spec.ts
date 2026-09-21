import { test, expect } from '@playwright/test';

test('Smoke test: Verify browser execution', async ({ page }) => {
  await page.goto('http://localhost:3000/login');
  
  // Verify URL
  expect(page.url()).toBe('http://localhost:3000/login');
  
  // Verify page title
  await expect(page).toHaveTitle(/CAMPUSLINK/i);
  
  // Verify login form exists
  await expect(page.locator('input[type="email"]')).toBeVisible();
  await expect(page.locator('input[type="password"]')).toBeVisible();
  await expect(page.locator('button:has-text("Sign In")')).toBeVisible();
  
  // Take screenshot
  await page.screenshot({ path: 'login-smoke-test.png' });
});
