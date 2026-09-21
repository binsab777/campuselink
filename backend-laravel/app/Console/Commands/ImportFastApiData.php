<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

class ImportFastApiData extends Command
{
    protected $signature = 'campuslink:import-fastapi-data {--file=../fastapi_data_snapshot.json} {--dry-run} {--truncate}';
    protected $description = 'Import data from FastAPI SQLite dump to achieve data parity';

    public function handle()
    {
        $file = $this->option('file');
        if (!file_exists($file)) {
            $this->error("File not found: $file");
            return 1;
        }

        $json = file_get_contents($file);
        $data = json_decode($json, true);

        if (json_last_error() !== JSON_ERROR_NONE) {
            $this->error("Invalid JSON format.");
            return 1;
        }

        $isDryRun = $this->option('dry-run');
        $truncate = $this->option('truncate');

        if ($isDryRun) {
            $this->info("Starting DRY RUN import...");
        } else {
            $this->info("Starting actual import...");
        }

        DB::beginTransaction();
        try {
            if (!$isDryRun) {
                Schema::disableForeignKeyConstraints();
                if ($truncate) {
                    $this->info("Truncating tables...");
                    $tables = ['drive_candidates', 'applications', 'placement_drives', 'job_requirements', 'student_skills', 'student_projects', 'student_certifications', 'student_academic_history', 'jobs', 'students', 'recruiters', 'skills', 'companies', 'users'];
                    foreach ($tables as $table) {
                        DB::table($table)->truncate();
                    }
                }
            }

            // 1. Users
            $this->importTable('users', $data['users'] ?? [], function($row) {
                return [
                    'id' => $row['id'],
                    'email' => $row['email'],
                    'password_hash' => $row['password_hash'],
                    'role' => $row['role'],
                    'is_active' => $row['is_active'] ?? true,
                    'created_at' => $row['created_at'],
                    'updated_at' => $row['updated_at'],
                ];
            }, $isDryRun);

            // 2. Companies
            $this->importTable('companies', $data['companies'] ?? [], function($row) {
                return [
                    'id' => $row['id'],
                    'name' => $row['name'],
                    'description' => $row['description'],
                    'industry' => $row['industry'],
                    'website' => $row['website'],
                    'size' => $row['size'],
                    'headquarters' => $row['headquarters'],
                    'logo_url' => $row['logo_url'],
                    'metadata_json' => $row['metadata_json'],
                    'created_at' => $row['created_at'],
                    'updated_at' => $row['updated_at'],
                ];
            }, $isDryRun);

            // 3. Skills
            $this->importTable('skills', $data['skills'] ?? [], function($row) {
                return [
                    'id' => $row['id'],
                    'name' => $row['name'],
                    'category' => $row['category'],
                    'created_at' => $row['created_at'],
                    'updated_at' => $row['updated_at'],
                ];
            }, $isDryRun);

            // 4. Recruiters
            $this->importTable('recruiters', $data['recruiters'] ?? [], function($row) {
                return [
                    'id' => $row['id'],
                    'user_id' => $row['user_id'],
                    'company_id' => $row['company_id'],
                    'contact_name' => $row['contact_name'],
                    'contact_email' => $row['contact_email'],
                    'contact_phone' => $row['contact_phone'],
                    'created_at' => $row['created_at'],
                    'updated_at' => $row['updated_at'],
                ];
            }, $isDryRun);

            // 5. Students
            $this->importTable('students', $data['students'] ?? [], function($row) {
                return [
                    'id' => $row['id'],
                    'user_id' => $row['user_id'],
                    'student_identifier' => $row['student_identifier'],
                    'first_name' => $row['first_name'] ?? 'Student',
                    'last_name' => $row['last_name'] ?? '',
                    'dob' => $row['dob'] ? date('Y-m-d', strtotime($row['dob'])) : null,
                    'gender' => $row['gender'],
                    'phone' => $row['phone'],
                    'branch' => $row['branch'],
                    'graduation_year' => $row['graduation_year'],
                    'cgpa' => $row['cgpa'],
                    'backlogs_current' => $row['backlogs_current'] ?? 0,
                    'backlogs_history' => $row['backlogs_history'] ?? 0,
                    'profile_metadata' => $row['profile_metadata'],
                    'resume_url' => $row['resume_url'],
                    'created_at' => $row['created_at'],
                    'updated_at' => $row['updated_at'],
                ];
            }, $isDryRun);

            // 6. Jobs
            $this->importTable('jobs', $data['jobs'] ?? [], function($row) {
                return [
                    'id' => $row['id'],
                    'company_id' => $row['company_id'],
                    'recruiter_id' => $row['recruiter_id'],
                    'title' => $row['title'],
                    'description' => $row['description'],
                    'employment_type' => $row['employment_type'],
                    'location' => $row['location'],
                    'remote_type' => $row['remote_type'],
                    'salary_range' => $row['salary_range'],
                    'experience_requirement' => $row['experience_requirement'],
                    'application_deadline' => $row['application_deadline'],
                    'openings' => $row['openings'],
                    'job_code' => $row['job_code'],
                    'job_description_json' => $row['job_description_json'],
                    'eligibility_config' => $row['eligibility_config'],
                    'status' => $row['status'],
                    'created_at' => $row['created_at'],
                    'updated_at' => $row['updated_at'],
                ];
            }, $isDryRun);

            // 7. Student Academic History
            $this->importTable('student_academic_history', $data['student_academic_history'] ?? [], function($row) {
                return [
                    'id' => $row['id'],
                    'student_id' => $row['student_id'],
                    'qualification' => $row['qualification'],
                    'institution' => $row['institution'],
                    'specialization' => $row['specialization'],
                    'start_year' => $row['start_year'],
                    'end_year' => $row['end_year'],
                    'score_value' => $row['score_value'],
                    'score_type' => $row['score_type'],
                    'created_at' => $row['created_at'],
                    'updated_at' => $row['updated_at'],
                ];
            }, $isDryRun);

            // 8. Student Certifications
            $this->importTable('student_certifications', $data['student_certifications'] ?? [], function($row) {
                return [
                    'id' => $row['id'],
                    'student_id' => $row['student_id'],
                    'name' => $row['name'],
                    'issuing_org' => $row['issuing_org'],
                    'issue_date' => $row['issue_date'] ? date('Y-m-d H:i:s', strtotime($row['issue_date'])) : null,
                    'expiry_date' => $row['expiry_date'] ? date('Y-m-d H:i:s', strtotime($row['expiry_date'])) : null,
                    'credential_id' => $row['credential_id'],
                    'created_at' => $row['created_at'],
                    'updated_at' => $row['updated_at'],
                ];
            }, $isDryRun);

            // 9. Student Projects
            $this->importTable('student_projects', $data['student_projects'] ?? [], function($row) {
                return [
                    'id' => $row['id'],
                    'student_id' => $row['student_id'],
                    'title' => $row['title'],
                    'description' => $row['description'],
                    'project_url' => $row['project_url'],
                    'technologies' => $row['technologies'],
                    'created_at' => $row['created_at'],
                    'updated_at' => $row['updated_at'],
                ];
            }, $isDryRun);

            // 10. Student Skills
            $this->importTable('student_skills', $data['student_skills'] ?? [], function($row) {
                return [
                    'id' => $row['id'],
                    'student_id' => $row['student_id'],
                    'skill_id' => $row['skill_id'],
                    'proficiency_level' => $row['proficiency_level'],
                    'months_experience' => $row['months_experience'],
                    'source' => $row['source'],
                    'created_at' => $row['created_at'],
                    'updated_at' => $row['updated_at'],
                ];
            }, $isDryRun);

            // 11. Job Requirements
            $this->importTable('job_requirements', $data['job_requirements'] ?? [], function($row) {
                return [
                    'id' => $row['id'],
                    'job_id' => $row['job_id'],
                    'skill_id' => $row['skill_id'],
                    'required_proficiency' => $row['required_proficiency'],
                    'is_mandatory' => $row['is_mandatory'] ?? true,
                    'created_at' => $row['created_at'],
                    'updated_at' => $row['updated_at'],
                ];
            }, $isDryRun);

            // 12. Placement Drives
            $this->importTable('placement_drives', $data['placement_drives'] ?? [], function($row) {
                return [
                    'id' => $row['id'],
                    'company_id' => $row['company_id'],
                    'job_id' => $row['job_id'],
                    'name' => $row['name'],
                    'drive_type' => $row['mode'] ?? 'ON_CAMPUS',
                    'registration_deadline' => $row['registration_deadline'] ? date('Y-m-d H:i:s', strtotime($row['registration_deadline'])) : null,
                    'start_date' => $row['date'] ? date('Y-m-d H:i:s', strtotime($row['date'])) : null,
                    'end_date' => $row['date'] ? date('Y-m-d H:i:s', strtotime($row['date'])) : null,
                    'capacity' => $row['capacity'],
                    'status' => 'PUBLISHED', // Map to valid status
                    'metadata_json' => json_encode(['coordinator_info' => $row['coordinator_info'] ?? '', 'notes' => $row['notes'] ?? '', 'venue' => $row['venue'] ?? '']),
                    'created_at' => $row['created_at'],
                    'updated_at' => $row['updated_at'],
                ];
            }, $isDryRun);

            // 13. Applications
            $this->importTable('applications', $data['applications'] ?? [], function($row) {
                return [
                    'id' => $row['id'],
                    'student_id' => $row['student_id'],
                    'job_id' => $row['job_id'],
                    'drive_id' => $row['drive_id'],
                    'status' => $row['status'],
                    'applied_at' => $row['applied_at'] ?? $row['created_at'],
                    'created_at' => $row['created_at'],
                    'updated_at' => $row['updated_at'],
                ];
            }, $isDryRun);

            // 14. Drive Candidates
            $this->importTable('drive_candidates', $data['drive_candidates'] ?? [], function($row) {
                return [
                    'id' => $row['id'],
                    'drive_id' => $row['drive_id'],
                    'student_id' => $row['student_id'],
                    'status' => $row['registration_status'] ?? 'REGISTERED',
                    'registered_at' => $row['registration_timestamp'] ?? $row['created_at'],
                    'created_at' => $row['created_at'],
                    'updated_at' => $row['updated_at'],
                ];
            }, $isDryRun);

            // Check if we need to reset sequence values for PostgreSQL
            if (!$isDryRun) {
                $tables = ['users', 'companies', 'skills', 'recruiters', 'students', 'jobs', 'student_academic_history', 'student_certifications', 'student_projects', 'student_skills', 'job_requirements', 'placement_drives', 'applications', 'drive_candidates'];
                foreach ($tables as $table) {
                    $maxId = DB::table($table)->max('id');
                    if ($maxId) {
                        DB::statement("SELECT setval('{$table}_id_seq', {$maxId})");
                    }
                }
                Schema::enableForeignKeyConstraints();
            }

            if ($isDryRun) {
                DB::rollBack();
                $this->info("Dry run completed. Transaction rolled back.");
            } else {
                DB::commit();
                $this->info("Import completed successfully.");
            }
        } catch (\Exception $e) {
            DB::rollBack();
            if (!$isDryRun) Schema::enableForeignKeyConstraints();
            $this->error("Import failed: " . $e->getMessage());
            $this->error($e->getTraceAsString());
            return 1;
        }

        return 0;
    }

    private function importTable($tableName, $rows, $mapper, $isDryRun)
    {
        $this->info("Processing $tableName... " . count($rows) . " rows");
        $count = 0;
        foreach ($rows as $row) {
            $mapped = $mapper($row);
            if (!$isDryRun) {
                DB::table($tableName)->updateOrInsert(
                    ['id' => $mapped['id']],
                    $mapped
                );
            }
            $count++;
        }
        $this->info("Completed $tableName: $count rows.");
    }
}
