import { test, expect } from '@playwright/test';

const BASE_URL = 'http://localhost:3000';

test.describe('Phase 8 - Validation Testing', () => {
  test.beforeEach(async ({ page }) => {
    // Login as a test student
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[type="email"]', 'teststudent99@test.com');
    await page.fill('input[type="password"]', 'mypassword123');
    await page.click('button:has-text("Sign In")');
    await page.waitForURL('**/dashboard');
    
    // Navigate to profile
    await page.click('text="My Profile"');
    await page.waitForURL('**/dashboard/profile');
  });

  test('Academic History Validation', async ({ page }) => {
    await page.click('button:has-text("Add Academic Record")');
    
    // 1. Missing required fields
    // Click submit without filling anything
    // In our UI, "Qualification" has default value 'Bachelor of Technology', start year 2022, end year 2026, score 8.5
    // So we clear Institution to trigger validation
    await page.locator('div[role="dialog"] input').nth(1).fill('');
    await page.locator('div[role="dialog"] button:has-text("Save Record")').click();
    await expect(page.locator('text=Institution is required.')).toBeVisible();

    // 2. Invalid year values (Start Year > End Year)
    await page.locator('div[role="dialog"] input').nth(1).fill('E2E Validation Univ');
    await page.locator('div[role="dialog"] input[type="number"]').nth(0).fill('2025');
    await page.locator('div[role="dialog"] input[type="number"]').nth(1).fill('2024');
    await page.locator('div[role="dialog"] button:has-text("Save Record")').click();
    await expect(page.locator('text=End year must be greater than or equal to start year.')).toBeVisible();

    // 3. Invalid Score (CGPA > 10)
    await page.locator('div[role="dialog"] input[type="number"]').nth(1).fill('2026'); // fix year
    await page.locator('div[role="dialog"] input[type="number"]').nth(2).fill('11'); // Invalid CGPA
    await page.locator('div[role="dialog"] button:has-text("Save Record")').click();
    await expect(page.locator('text=CGPA score must be between 0.0 and 10.0.')).toBeVisible();

    // Change to PERCENTAGE and test invalid score
    await page.locator('div[role="dialog"] select').first().selectOption('PERCENTAGE');
    await page.locator('div[role="dialog"] input[type="number"]').nth(2).fill('105'); // Invalid percentage
    await page.locator('div[role="dialog"] button:has-text("Save Record")').click();
    await expect(page.locator('text=Percentage score must be between 0% and 100%.')).toBeVisible();

    // Dismiss modal
    await page.locator('div[role="dialog"] button:has-text("Cancel")').click();
  });

  test('Certifications Validation', async ({ page }) => {
    await page.click('button:has-text("Add Certification")');
    
    // 1. Missing required fields
    await page.locator('div[role="dialog"] button:has-text("Add Certification")').click();
    await expect(page.locator('text=Certification name must be at least 2 characters.')).toBeVisible();
    await expect(page.locator('text=Issuing organization must be at least 2 characters.')).toBeVisible();

    // 2. Invalid dates (Expiry before Issue)
    await page.locator('div[role="dialog"] input').nth(0).fill('Test Cert');
    await page.locator('div[role="dialog"] input').nth(1).fill('Test Org');
    await page.locator('div[role="dialog"] input[type="date"]').nth(0).fill('2023-05-01'); // Issue
    await page.locator('div[role="dialog"] input[type="date"]').nth(1).fill('2022-05-01'); // Expiry
    await page.locator('div[role="dialog"] button:has-text("Add Certification")').click();
    await expect(page.locator('text=Expiry date cannot precede issue date.')).toBeVisible();
    
    // Dismiss modal
    await page.locator('div[role="dialog"] button:has-text("Cancel")').click();
  });
});
