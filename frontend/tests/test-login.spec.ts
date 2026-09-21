import { test, expect } from '@playwright/test';

test('Test Login', async ({ page }) => {
  await page.goto('http://localhost:3000/login');
  await page.fill('input[type="email"]', 'testrecruiter_real@test.com');
  await page.fill('input[type="password"]', 'mypassword123');
  await page.click('button:has-text("Sign In")');
  await page.waitForTimeout(3000);
  await page.screenshot({ path: 'screenshots/login-error.png', fullPage: true });
});
