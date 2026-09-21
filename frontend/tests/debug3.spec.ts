import { test, expect } from '@playwright/test';

test('Debug Login', async ({ page }) => {
  await page.goto('http://localhost:3000/login');
  await page.fill('input[type="email"]', 'admin@campuslink.com');
  await page.fill('input[type="password"]', 'password');
  await page.click('button:has-text("Sign In")');
  
  await page.waitForTimeout(3000);
  const text = await page.innerText('body');
  console.log("BODY AFTER 3 SECONDS:");
  console.log(text);
});
