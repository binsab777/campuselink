import { test, expect } from '@playwright/test';
import { execSync } from 'child_process';

test.describe('Registration E2E Workflows', () => {
  const timestamp = Date.now();
  const studentEmail = `student${timestamp}@test.com`;
  const recruiterEmail = `recruiter${timestamp}@test.com`;

  test.afterAll(async () => {
    console.log("Cleaning up test data...");
    // Delete test users and any companies created by them (via recruiter relation)
    // Note: Since cascade delete is unreliable for reverse relations (recruiter -> company),
    // we delete companies created by these specific test recruiters explicitly.
    try {
      const deleteCmd = `php artisan tinker --execute="DB::table('users')->whereIn('email', ['${studentEmail}', '${recruiterEmail}'])->delete(); DB::table('companies')->where('name', 'like', 'Recruiter${timestamp}%')->delete(); echo 'Cleanup done';"`;
      execSync(deleteCmd, { cwd: '../backend-laravel', stdio: 'ignore' });
      console.log("Cleanup complete.");
    } catch (e) {
      console.error("Cleanup failed:", e);
    }
  });

  test('1. Invalid restricted role registration is hidden/rejected', async ({ page, request }) => {
    await page.goto('http://localhost:3000/register');
    const options = await page.locator('select').innerText();
    expect(options).not.toContain('Admin');
    expect(options).not.toContain('Placement Officer');
    expect(options).not.toContain('SUPER_ADMIN');

    // Also verify API actively rejects PLACEMENT_OFFICER, MENTOR, SUPER_ADMIN
    const rolesToReject = ['PLACEMENT_OFFICER', 'MENTOR', 'SUPER_ADMIN'];
    for (const role of rolesToReject) {
      const response = await request.post('http://localhost:8001/api/v1/auth/register', {
        data: {
          email: `test${role}@test.com`,
          password: 'password123',
          role: role
        }
      });
      expect(response.status()).toBe(403);
    }
  });

  test('2. Student registration -> login -> student dashboard', async ({ page }) => {
    await page.goto('http://localhost:3000/register');
    await page.selectOption('select', 'STUDENT');
    await page.fill('input[type="email"]', studentEmail);
    await page.locator('input[type="password"]').nth(0).fill('password123');
    await page.locator('input[type="password"]').nth(1).fill('password123');
    await page.click('button:has-text("Register Account")');
    await page.waitForURL('**/login');

    await page.fill('input[type="email"]', studentEmail);
    await page.locator('input[type="password"]').nth(0).fill('password123');
    await page.click('button:has-text("Sign In")');
    await page.waitForURL('**/dashboard');
    console.log("Student login successful");
  });

  test('3. Duplicate email registration -> rejected', async ({ page }) => {
    await page.goto('http://localhost:3000/register');
    await page.selectOption('select', 'STUDENT');
    await page.fill('input[type="email"]', studentEmail); 
    await page.locator('input[type="password"]').nth(0).fill('password123');
    await page.locator('input[type="password"]').nth(1).fill('password123');
    await page.click('button:has-text("Register Account")');
    await page.waitForTimeout(2000);
    expect(page.url()).toContain('register');
  });

  test('4. Recruiter registration -> login -> recruiter dashboard', async ({ page }) => {
    await page.goto('http://localhost:3000/register');
    await page.selectOption('select', 'RECRUITER');
    await page.fill('input[type="email"]', recruiterEmail);
    await page.locator('input[type="password"]').nth(0).fill('password123');
    await page.locator('input[type="password"]').nth(1).fill('password123');
    await page.click('button:has-text("Register Account")');
    await page.waitForURL('**/login');
    
    await page.fill('input[type="email"]', recruiterEmail);
    await page.locator('input[type="password"]').nth(0).fill('password123');
    await page.click('button:has-text("Sign In")');
    await page.waitForURL('**/dashboard');
    console.log("Recruiter login successful");
  });
});
