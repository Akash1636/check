# Database Schema Documentation

## Tables

### users
Stores user authentication and profile information
- id: Primary key (auto-increment)
- username: Unique username
- email: Unique email address
- password: Bcrypt hashed password
- role: User role (student/instructor/admin)
- created_at: Account creation timestamp
- last_login: Last login timestamp

### courses
Stores course information
- id: Primary key (auto-increment)
- name: Course name
- category: Course category
- instructor: Instructor name
- description: Course description
- limit_students: Maximum enrollment limit
- duration_hours: Course duration (hours)
- duration_minutes: Course duration (minutes)
- prerequisites: Required prerequisites
- created_at: Course creation timestamp

### enrollments
Tracks student course enrollments
- id: Primary key (auto-increment)
- student_id: Foreign key to users.id
- course_id: Foreign key to courses.id
- department: Student department
- batch: Student batch/year
- enrolled_date: Enrollment timestamp
- status: Enrollment status (ongoing/completed/dropped)

### audit_logs
Security audit trail for all user actions
- id: Primary key (auto-increment)
- user_id: Foreign key to users.id
- action: Action type (LOGIN/REGISTER/CREATE_COURSE/ENROLL/etc)
- details: Additional action details
- ip_address: User IP address
- timestamp: Action timestamp

## Security Features
- Bcrypt password hashing (cost factor 12)
- JWT token authentication (24-hour expiry)
- Audit logging for all critical actions
- Foreign key constraints with CASCADE delete
- Input validation on all endpoints
