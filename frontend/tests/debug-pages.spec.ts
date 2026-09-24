import { test, expect } from '@playwright/test';

test('Debug pages', async ({ page }) => {
  await page.goto('http://localhost:3000/login');
  await page.fill('input[type="email"]', 'admin@campuslink.com');
  await page.fill('input[type="password"]', 'password');
  await page.click('button:has-text("Sign In")');
  await page.waitForURL('**/dashboard');
  
  await page.waitForTimeout(2000);
  console.log('After login URL:', page.url());
  
  // Try to click a link if it exists
  const linkCount = await page.locator('text="Manage Users"').count();
  if (linkCount > 0) {
    await page.click('text="Manage Users"');
    await page.waitForTimeout(2000);
    console.log('After click URL:', page.url());
    console.log('After click Text:', await page.locator('body').innerText());
  }
});
