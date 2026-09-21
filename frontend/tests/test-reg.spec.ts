import { test, expect } from '@playwright/test';

test('Test Reg Error', async ({ page }) => {
  await page.goto('http://localhost:3000/register');
  await page.selectOption('select', 'STUDENT');
  await page.fill('input[type="email"]', 'newstudent999@test.com');
  await page.fill('input[type="password"]', 'password123');
  await page.click('button:has-text("Register Account")');
  await page.waitForTimeout(3000);
  await page.screenshot({ path: 'screenshots/reg-error.png', fullPage: true });
});
