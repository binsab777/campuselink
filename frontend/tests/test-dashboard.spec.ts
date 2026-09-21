import { test, expect } from '@playwright/test';

test('Test Dashboard', async ({ page }) => {
  await page.goto('http://localhost:3000/login');
  await page.fill('input[type="email"]', 'testrecruiter_real@test.com');
  await page.fill('input[type="password"]', 'mypassword123');
  await page.click('button:has-text("Sign In")');
  await page.waitForURL('**/dashboard**');
  await page.click('text=Open Recruiter Portal');
  await page.waitForURL('**/dashboard/recruiter**');
  await page.waitForTimeout(3000);
  await page.screenshot({ path: 'screenshots/dashboard-recruiter.png', fullPage: true });
});
