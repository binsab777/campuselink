import re
import sys

with open('frontend/src/app/dashboard/admin/users/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

student_additions = """
                {viewingUser.student_profile.academic_history && viewingUser.student_profile.academic_history.length > 0 && (
                  <div>
                    <span className="block text-xs font-semibold text-gray-500 mb-1">Academic History ({viewingUser.student_profile.academic_history.length})</span>
                    <ul className="text-xs text-gray-700 list-disc list-inside">
                      {viewingUser.student_profile.academic_history.map((a: any) => (
                        <li key={a.id}>{a.degree} from {a.institution} ({a.percentage}%)</li>
                      ))}
                    </ul>
                  </div>
                )}
                
                {viewingUser.student_profile.certifications && viewingUser.student_profile.certifications.length > 0 && (
                  <div>
                    <span className="block text-xs font-semibold text-gray-500 mb-1">Certifications ({viewingUser.student_profile.certifications.length})</span>
                    <ul className="text-xs text-gray-700 list-disc list-inside">
                      {viewingUser.student_profile.certifications.map((c: any) => (
                        <li key={c.id}>{c.name} by {c.issuing_organization}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {viewingUser.student_profile.resume_url && (
                  <div>
                    <span className="block text-xs font-semibold text-gray-500 mb-1">Resume Metadata</span>
                    <a href={viewingUser.student_profile.resume_url} target="_blank" rel="noopener noreferrer" className="text-xs text-blue-600 underline">View Resume Document</a>
                  </div>
                )}

                {viewingUser.student_profile.applications && viewingUser.student_profile.applications.length > 0 && (
                  <div>
                    <span className="block text-xs font-semibold text-gray-500 mb-1">Job Applications ({viewingUser.student_profile.applications.length})</span>
                    <ul className="text-xs text-gray-700 list-disc list-inside">
                      {viewingUser.student_profile.applications.map((app: any) => (
                        <li key={app.id}>Application #{app.id} - Status: {app.status}</li>
                      ))}
                    </ul>
                  </div>
                )}
                
                {viewingUser.student_profile.scores && viewingUser.student_profile.scores.length > 0 && (
                  <div>
                    <span className="block text-xs font-semibold text-gray-500 mb-1">Readiness Scores ({viewingUser.student_profile.scores.length})</span>
                    <ul className="text-xs text-gray-700 list-disc list-inside">
                      {viewingUser.student_profile.scores.map((s: any) => (
                        <li key={s.id}>{s.dimension}: {s.score}/100</li>
                      ))}
                    </ul>
                  </div>
                )}

                {viewingUser.student_profile.assessments && viewingUser.student_profile.assessments.length > 0 && (
                  <div>
                    <span className="block text-xs font-semibold text-gray-500 mb-1">Assessments ({viewingUser.student_profile.assessments.length})</span>
                    <ul className="text-xs text-gray-700 list-disc list-inside">
                      {viewingUser.student_profile.assessments.map((a: any) => (
                        <li key={a.id}>{a.test_name} - Score: {a.score}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {viewingUser.student_profile.offers && viewingUser.student_profile.offers.length > 0 && (
                  <div>
                    <span className="block text-xs font-semibold text-gray-500 mb-1">Job Offers ({viewingUser.student_profile.offers.length})</span>
                    <ul className="text-xs text-gray-700 list-disc list-inside">
                      {viewingUser.student_profile.offers.map((o: any) => (
                        <li key={o.id}>Offer #{o.id} - Salary: {o.salary_offered}</li>
                      ))}
                    </ul>
                  </div>
                )}
"""

recruiter_additions = """
                {viewingUser.recruiter_profile.jobs && viewingUser.recruiter_profile.jobs.length > 0 && (
                  <div>
                    <span className="block text-xs font-semibold text-gray-500 mb-1">Job Postings ({viewingUser.recruiter_profile.jobs.length})</span>
                    <div className="space-y-2">
                      {viewingUser.recruiter_profile.jobs.map((j: any) => (
                        <div key={j.id} className="p-2 border border-gray-100 rounded bg-gray-50">
                          <div className="font-medium text-xs">{j.title} ({j.status})</div>
                          {j.requirements && j.requirements.length > 0 && (
                            <div className="mt-1 flex flex-wrap gap-1">
                              {j.requirements.map((req: any) => (
                                <span key={req.id} className="px-1.5 py-0.5 text-[10px] bg-white border rounded text-gray-600">{req.skill_name || 'Skill #'+req.skill_id}</span>
                              ))}
                            </div>
                          )}
                          {j.applications && j.applications.length > 0 && (
                            <div className="mt-1 text-2xs text-gray-500">
                              {j.applications.length} Applications Received
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
"""

# Replace in student profile
content = content.replace(
    '                {viewingUser.student_profile.projects && viewingUser.student_profile.projects.length > 0 && (',
    student_additions + '\n                {viewingUser.student_profile.projects && viewingUser.student_profile.projects.length > 0 && ('
)

# Replace in recruiter profile
content = content.replace(
    '              {viewingUser.recruiter_profile && (',
    '              {viewingUser.recruiter_profile && (\n                <div className="space-y-4">\n                  <h3 className="text-sm font-bold text-gray-900 border-b pb-2">Recruiter & Company Information</h3>'
)

# Add jobs under recruiter profile. Wait, let's find a safe hook.
content = content.replace(
    '                    </div>\n                  </div>\n                </div>\n              )}',
    '                    </div>\n                  </div>\n' + recruiter_additions + '                </div>\n              )}'
)


with open('frontend/src/app/dashboard/admin/users/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
