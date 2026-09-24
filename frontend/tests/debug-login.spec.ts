import { test, expect } from '@playwright/test';

test('Debug Login', async ({ page }) => {
  page.on('console', msg => console.log('BROWSER CONSOLE:', msg.text()));
  page.on('response', resp => console.log('RESPONSE:', resp.url(), resp.status()));

  await page.goto('http://localhost:3000/login');
  await page.fill('input[type="email"]', 'admin@campuslink.com');
  await page.fill('input[type="password"]', 'password');
  await page.click('button:has-text("Sign In")');
  
  await page.waitForTimeout(3000); // Give it time to do requests
  
  console.log('Current URL:', page.url());
  console.log('Page Text:', await page.locator('body').innerText());
});
