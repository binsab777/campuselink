import { test, expect } from '@playwright/test';

test('Debug Text', async ({ page }) => {
  await page.goto('http://localhost:3000/login');
  await page.fill('input[type="email"]', 'testadmin99@test.com');
  await page.fill('input[type="password"]', 'mypassword123');
  await page.click('button:has-text("Sign In")');
  await page.waitForURL('**/dashboard');
  await page.goto('http://localhost:3000/dashboard/admin/users');
  await page.waitForTimeout(3000);
  const text = await page.innerText('body');
  console.log(text);
});
