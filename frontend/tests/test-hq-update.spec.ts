import { test, expect } from '@playwright/test';

test('Update Headquarters', async ({ page }) => {
  await page.goto('http://localhost:3000/login');
  await page.fill('input[type="email"]', 'testrecruiter_real@test.com');
  await page.fill('input[type="password"]', 'mypassword123');
  await page.click('button:has-text("Sign In")');
  await page.waitForURL('**/dashboard**');
  await page.click('text=Open Recruiter Portal');
  await page.waitForURL('**/dashboard/recruiter**');
  await page.waitForTimeout(2000);
  
  // Open Company Edit Modal
  await page.click('button:has-text("Edit Company")');
  await page.waitForTimeout(1000);
  
  // Fill headquarters
  await page.fill('input[placeholder="e.g. Bangalore, India"]', 'New York, USA');
  await page.click('button:has-text("Save Company")');
  
  await page.waitForTimeout(2000);
  
  // Verify it updated on the page
  await expect(page.locator('text=New York, USA')).toBeVisible();
  
  // Revert back for cleanliness
  await page.click('button:has-text("Edit Company")');
  await page.waitForTimeout(1000);
  await page.fill('input[placeholder="e.g. Bangalore, India"]', 'San Francisco, CA');
  await page.click('button:has-text("Save Company")');
  
  await page.waitForTimeout(2000);
  console.log("Successfully updated and reverted headquarters.");
});
