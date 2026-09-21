import { test, expect } from '@playwright/test';

test('Student Profile Page Deep Check', async ({ page }) => {
  const errors: string[] = [];
  page.on('console', msg => {
    if (msg.type() === 'error') errors.push(msg.text());
  });
  page.on('pageerror', err => errors.push(err.message));
  page.on('response', response => {
    if (response.status() >= 400 && response.url().includes('/api/')) {
      errors.push(`API Error: ${response.status()} ${response.url()}`);
    }
  });

  await page.goto('http://localhost:3000/login');
  await page.fill('input[type="email"]', 'student1@college.edu');
  await page.fill('input[type="password"]', 'stu123');
  await page.click('button:has-text("Sign In")');

  await page.waitForURL('**/dashboard**');
  
  // Go to profile page via client-side routing
  await page.click('text=My Profile');
  
  // Wait for the page to settle
  await page.waitForTimeout(3000);
  
  // Take screenshot
  await page.screenshot({ path: 'screenshots/student-profile-deep.png', fullPage: true });

  // Dump errors to a file so we can read them
  const fs = require('fs');
  fs.writeFileSync('screenshots/profile-errors.json', JSON.stringify(errors, null, 2));
});
