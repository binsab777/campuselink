import { test, expect } from '@playwright/test';

test('Student End-to-End Workflow', async ({ page }) => {
  console.log('Starting Student E2E Test...');
  
  // 1. Login
  await page.goto('http://localhost:3000/login');
  await page.fill('input[type="email"]', 'student1@college.edu');
  await page.fill('input[type="password"]', 'stu123');
  await page.click('button:has-text("Sign In")');
  await page.waitForURL('**/dashboard**');
  console.log('Successfully logged in');
  
  // 2. Profile Page
  await page.click('text=My Profile');
  await page.waitForTimeout(2000);
  
  await expect(page.locator('text=Personal & Academic Information')).toBeVisible();
  await expect(page.locator('text=STU7800')).toBeVisible();
  
  // 3. Add Skill
  await page.click('text=+ Add Skill');
  await page.fill('input[placeholder="e.g. Python, React, PostgreSQL"]', 'Playwright Automation');
  await page.selectOption('select', { value: 'INTERMEDIATE' });
  await page.click('button[type="submit"]');
  await page.waitForTimeout(2000);
  await expect(page.locator('text=Playwright Automation')).toBeVisible();
  console.log('Successfully added skill');

  // 4. Jobs & Drives
  await page.click('text=Jobs & Drives', { force: true });
  await page.waitForURL('**/jobs');
  await page.waitForTimeout(1000);
  console.log('Successfully loaded Jobs page');

  // 5. Readiness & Gaps
  await page.click('text=Readiness & Gaps', { force: true });
  await page.waitForTimeout(2000);
  await expect(page.locator('text=Placement Readiness Score')).toBeVisible();
  await expect(page.locator('text=Data Completeness & Reliability')).toBeVisible();
  console.log('Successfully loaded Readiness page');
  
  // Capture Final Screenshot
  await page.screenshot({ path: 'screenshots/student-e2e-final.png', fullPage: true });
  console.log('Workflow complete.');
});
