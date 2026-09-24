import { test, expect } from '@playwright/test';

const BASE_URL = 'http://localhost:3000';

test.describe('Phase 8 - Academic & Certifications CRUD', () => {

  test.beforeEach(async ({ page }) => {
    // Login as a test student
    await page.goto(`${BASE_URL}/login`);
    await page.fill('input[type="email"]', 'teststudent99@test.com');
    await page.fill('input[type="password"]', 'mypassword123');
    await page.click('button:has-text("Sign In")');
    await page.waitForURL('**/dashboard');
    
    // Navigate to profile by clicking the link to preserve Next.js SPA state
    await page.click('text="My Profile"');
    await page.waitForURL('**/dashboard/profile');
  });

  test('Academic History & Certifications CRUD', async ({ page }) => {
    test.setTimeout(120000); // 2 minutes timeout

    // ---- ACADEMIC HISTORY CRUD ----
    // 1. Create
    await page.click('button:has-text("Add Academic Record")');
    // Using nth() for inputs since names are not present
    await page.locator('div[role="dialog"] input').nth(0).fill('B.Tech Computer Science');
    await page.locator('div[role="dialog"] input').nth(1).fill('E2E University');
    await page.locator('div[role="dialog"] input').nth(2).fill('AI & ML');
    
    // Start Year is the 4th input (index 3)
    await page.locator('div[role="dialog"] input[type="number"]').nth(0).fill('2020');
    await page.locator('div[role="dialog"] input[type="number"]').nth(1).fill('2024');
    
    // Select Option
    await page.locator('div[role="dialog"] select').first().selectOption('CGPA');
    await page.locator('div[role="dialog"] input[type="number"]').nth(2).fill('9.5');
    
    await page.locator('div[role="dialog"] button:has-text("Save Record")').click();
    
    // Assert Create
    await expect(page.locator('text=E2E University')).toBeVisible();

    // 2. Read (Already asserted by it being visible)
    
    // 3. Update
    // Find the edit button inside the container of E2E University
    const recordContainer = page.locator('div', { hasText: 'E2E University' }).last();
    // Wait, the edit and delete buttons are in a div next to the text. We can just look for the row.
    // There are multiple divs with E2E university, the most specific one is the row.
    const row = page.locator('.py-4', { hasText: 'E2E University' });
    await row.locator('button:has-text("Edit")').click();
    
    // Change score
    await page.locator('div[role="dialog"] input[type="number"]').nth(2).fill('9.8');
    await page.locator('div[role="dialog"] button:has-text("Update Record")').click();
    
    // Wait a bit for update to reflect
    await expect(page.locator('text=9.8')).toBeVisible();

    // 4. Delete
    await row.locator('button:has-text("Delete")').click(); 
    await page.locator('div[role="dialog"] button:has-text("Delete")').click();
    await page.locator('div[role="dialog"]').waitFor({ state: 'hidden' });
    await expect(page.locator('text=E2E University').first()).not.toBeVisible();

    // ---- CERTIFICATIONS CRUD ----
    // 1. Create
    await page.click('button:has-text("Add Certification")');
    // Using nth() for inputs since names are not present
    await page.locator('div[role="dialog"] input').nth(0).fill('AWS Certified Developer');
    await page.locator('div[role="dialog"] input').nth(1).fill('Amazon Web Services');
    await page.locator('div[role="dialog"] input[type="date"]').nth(0).fill('2023-05-01');
    await page.locator('div[role="dialog"] input').nth(4).fill('AWS-DEV-999');
    await page.locator('div[role="dialog"] button:has-text("Add Certification")').click();

    // Assert Create
    await expect(page.locator('text=AWS Certified Developer')).toBeVisible();
    await expect(page.locator('text=Amazon Web Services')).toBeVisible();

    // 3. Update
    const certRow = page.locator('.py-3\\.5', { hasText: 'AWS Certified Developer' });
    await certRow.locator('button:has-text("Edit")').click();
    await page.locator('div[role="dialog"] input').nth(4).fill('AWS-DEV-1000');
    await page.locator('div[role="dialog"] button:has-text("Update Certification")').click();
    await expect(page.locator('text=AWS-DEV-1000')).toBeVisible();

    // 4. Delete
    await certRow.locator('button:has-text("Delete")').click();
    await page.locator('div[role="dialog"] button:has-text("Delete")').click();
    await page.locator('div[role="dialog"]').waitFor({ state: 'hidden' });
    await expect(page.locator('text=AWS Certified Developer').first()).not.toBeVisible();
  });
});
