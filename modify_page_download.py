import re
import sys

with open('frontend/src/app/dashboard/admin/users/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Add download function inside AdminUsersPage component
download_func = """
  const handleDownloadResume = async (url: string) => {
    try {
      const fullUrl = url.startsWith('http') ? url : (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000') + url;
      const token = localStorage.getItem('token');
      const response = await fetch(fullUrl, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (!response.ok) throw new Error('Failed to download');
      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = downloadUrl;
      a.download = 'resume.pdf';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(downloadUrl);
      a.remove();
    } catch (err) {
      console.error(err);
      alert('Could not download resume');
    }
  };
"""

content = content.replace(
    'const [error, setError] = useState<string | null>(null);',
    'const [error, setError] = useState<string | null>(null);\n' + download_func
)

# Change a tag to button
content = content.replace(
    '<a href={viewingUser.student_profile.resume_url} target="_blank" rel="noopener noreferrer" className="text-xs text-blue-600 underline">View Resume Document</a>',
    '<button onClick={() => handleDownloadResume(viewingUser.student_profile.resume_url)} className="text-xs text-blue-600 underline cursor-pointer">View Resume Document</button>'
)

with open('frontend/src/app/dashboard/admin/users/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
