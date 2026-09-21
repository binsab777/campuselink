import json
import subprocess
import os

tables = ['users', 'companies', 'skills', 'recruiters', 'students', 'jobs', 'student_academic_history', 'student_certifications', 'student_projects', 'student_skills', 'job_requirements', 'placement_drives', 'applications', 'drive_candidates']

data = {}
env = os.environ.copy()
env['PGPASSWORD'] = 'campuslink_password'

for table in tables:
    query = "COPY (SELECT row_to_json(t) FROM (SELECT * FROM " + table + ") t) TO STDOUT;"
    result = subprocess.run(
        ['psql', '-U', 'campuslink', '-d', 'campuslink_db', '-h', '127.0.0.1', '-c', query],
        env=env,
        capture_output=True,
        text=True
    )
    rows = []
    if result.returncode == 0:
        for line in result.stdout.strip().split('\n'):
            if line:
                rows.append(json.loads(line))
    else:
        print(f"Error on {table}: {result.stderr}")
    data[table] = rows

with open('laravel_data_snapshot.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, default=str)

print('Exported Laravel data.')
