import { test, expect } from '@playwright/test';

test('Recruiter End-to-End Workflow', async ({ page }) => {
  console.log('Starting Recruiter E2E Test...');
  
  // 1. Login
  await page.goto('http://localhost:3000/login');
  await page.fill('input[type="email"]', 'testrecruiter_real@test.com');
  await page.fill('input[type="password"]', 'mypassword123');
  await page.click('button:has-text("Sign In")');
  await page.waitForURL('**/dashboard**');
  console.log('Successfully logged in');
  
  // 2. Open Recruiter Portal
  await page.click('text=Open Recruiter Portal');
  await page.waitForURL('**/dashboard/recruiter**');
  await page.waitForTimeout(2000);
  await expect(page.locator('text=ACTIVE JOBS')).toBeVisible();
  
  // 3. Company Profile
  await expect(page.locator('text=Testrecruiter_real Technologies')).toBeVisible();
  console.log('Successfully loaded Company Profile');

  // 4. Jobs 
  await page.click('text=Job Postings');
  await page.waitForTimeout(2000);
  await expect(page.locator('text=Create Job Posting').first()).toBeVisible();
  console.log('Successfully loaded Jobs page');

  // 5. Drives
  await page.click('text=Placement Drives');
  await page.waitForTimeout(2000);
  console.log('Successfully loaded Placement Drives page');
  
  // Capture Final Screenshot
  await page.screenshot({ path: 'screenshots/recruiter-e2e-final.png', fullPage: true });
  console.log('Recruiter Workflow complete.');
});
