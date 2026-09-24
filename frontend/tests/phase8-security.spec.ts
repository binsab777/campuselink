import { test, expect, request } from '@playwright/test';

const API_BASE = 'http://localhost:8000/api/v1';

test.describe('Phase 8 - Security & Ownership', () => {
  let student1Token: string;
  let student2Token: string;
  
  let student1AcademicId: number;
  let student1CertId: number;

  test.beforeAll(async () => {
    const apiContext = await request.newContext();
    
    // Login Student 1
    let res = await apiContext.post(`${API_BASE}/auth/login`, {
      data: { email: 'teststudent99@test.com', password: 'mypassword123' }
    });
    let body = await res.json();
    student1Token = body.token;
    
    // Login Student 2
    res = await apiContext.post(`${API_BASE}/auth/login`, {
      data: { email: 'student1@college.edu', password: 'password' }
    });
    body = await res.json();
    student2Token = body.token;
    
    // Create an Academic Record for Student 1
    res = await apiContext.post(`${API_BASE}/students/me/academic`, {
      headers: { Authorization: `Bearer ${student1Token}`, Accept: 'application/json' },
      data: {
        qualification: 'Security Test Degree',
        institution: 'Security Univ',
        start_year: 2020,
        end_year: 2024,
        score_type: 'CGPA',
        score_value: 9.0
      }
    });
    body = await res.json();
    student1AcademicId = body.id;

    // Create a Certification for Student 1
    res = await apiContext.post(`${API_BASE}/students/me/certifications`, {
      headers: { Authorization: `Bearer ${student1Token}`, Accept: 'application/json' },
      data: {
        name: 'Security Test Cert',
        issuing_org: 'Security Org',
      }
    });
    body = await res.json();
    student1CertId = body.id;
  });

  test('Student cannot access/modify another students Academic History', async ({ request }) => {
    // Try to update Student 1's record using Student 2's token
    let res = await request.put(`${API_BASE}/students/me/academic/${student1AcademicId}`, {
      headers: { 
        Authorization: `Bearer ${student2Token}`,
        Accept: 'application/json'
      },
      data: { qualification: 'Hacked' }
    });
    expect([401, 403, 404]).toContain(res.status()); // Forbidden or Not Found since it's scoped to me
    
    // Try to delete Student 1's record using Student 2's token
    res = await request.delete(`${API_BASE}/students/me/academic/${student1AcademicId}`, {
      headers: { Authorization: `Bearer ${student2Token}`, Accept: 'application/json' }
    });
    expect([401, 403, 404]).toContain(res.status());
  });

  test('Student cannot access/modify another students Certification', async ({ request }) => {
    // Try to update Student 1's cert using Student 2's token
    let res = await request.put(`${API_BASE}/students/me/certifications/${student1CertId}`, {
      headers: { Authorization: `Bearer ${student2Token}`, Accept: 'application/json' },
      data: { name: 'Hacked Cert' }
    });
    expect([401, 403, 404]).toContain(res.status()); 
    
    // Try to delete Student 1's cert using Student 2's token
    res = await request.delete(`${API_BASE}/students/me/certifications/${student1CertId}`, {
      headers: { Authorization: `Bearer ${student2Token}`, Accept: 'application/json' }
    });
    expect([401, 403, 404]).toContain(res.status());
  });

  test('Unauthorized requests return 401', async ({ request }) => {
    let res = await request.get(`${API_BASE}/students/me/academic`, { headers: { Accept: 'application/json' } });
    expect(res.status()).toBe(401);
    
    res = await request.post(`${API_BASE}/students/me/certifications`, {
      headers: { Accept: 'application/json' },
      data: { name: 'Hack', issuing_org: 'Hack' }
    });
    expect(res.status()).toBe(401);
  });
});
