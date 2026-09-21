import { test, expect } from '@playwright/test';

test('Student Visual Check', async ({ page }) => {
  await page.goto('http://localhost:3000/login');
  await page.fill('input[type="email"]', 'student1@college.edu');
  await page.fill('input[type="password"]', 'stu123');
  await page.click('button:has-text("Sign In")');

  await page.waitForURL('**/dashboard**');
  
  // Wait for the actual content to load instead of the "Loading..." spinner
  await expect(page.locator('.text-2xl').first()).toBeVisible({ timeout: 10000 });
  await page.waitForTimeout(2000); // Give it a moment to fully render charts etc
  
  await page.screenshot({ path: 'screenshots/student-dashboard-verified.png', fullPage: true });
});
