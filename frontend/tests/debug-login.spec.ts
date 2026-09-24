import { test, expect } from '@playwright/test';

test('Debug Login', async ({ page }) => {
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', err => console.log('PAGE ERROR:', err));
  page.on('requestfailed', request => console.log('REQ FAILED:', request.url(), request.failure()?.errorText));

  await page.goto('http://localhost:3000/login');
  await page.fill('input[type="email"]', 'teststudent99@test.com');
  await page.fill('input[type="password"]', 'mypassword123');
  await page.click('button:has-text("Sign In")');
  
  await page.waitForTimeout(5000);
  await page.screenshot({ path: 'debug-login.png' });
  
  // check if there's an error message on screen
  const errorText = await page.locator('.text-red-600').allTextContents();
  console.log('Error elements:', errorText);
});
