# Database-Connected Frontend Setup

## Overview

The system now has TWO versions:

### Version 1: LocalStorage (Original)
- **Files**: `index.html`, `dashboard.html`, `script.js`
- **Storage**: Browser localStorage
- **No backend needed**

### Version 2: Database-Connected (NEW)
- **Files**: `index-db.html`, `dashboard-db.html`, `script-db.js`, `api-config.js`
- **Storage**: SQLite database via backend API
- **Backend required**

## Setup Database Version

### 1. Install Dependencies
```bash
cd backend
pip install -r ../config/requirements.txt
```

### 2. Initialize Database
```bash
cd database
python setup_db.py
```

This creates:
- Admin account: `admin` / `admin123`
- SQLite database: `course_system.db`

### 3. Start Backend Server
```bash
cd backend
python api.py
```

Server runs on: http://localhost:5001

### 4. Open Frontend
Open `frontend/index-db.html` in browser

## Features

### Admin Can:
- ✅ Add/Delete courses
- ✅ Upload courses from Excel
- ✅ Upload students from Excel
- ✅ View student enrollments by department/batch
- ✅ All data stored in database

### Students Can:
- ✅ Login with credentials
- ✅ View available courses
- ✅ Enroll in courses
- ✅ View their enrollments
- ✅ All data stored in database

## Excel Upload

### Courses Excel Format:
- Name, Category, Instructor, Description
- Limit, Duration (hours), Duration (minutes), Prerequisites

### Students Excel Format:
- Username, Student Name, Department, Batch
- Course Ongoing, Course Completed

Sample files in: `sample_documents/`

## Database Editing

### Option 1: Via Web Interface
- Login as admin
- Use dashboard to add/edit/delete

### Option 2: Direct Database Access
```bash
cd backend
sqlite3 course_system.db
```

SQL Commands:
```sql
-- View all courses
SELECT * FROM courses;

-- View all students
SELECT * FROM users WHERE role='student';

-- View enrollments
SELECT u.username, c.name, e.status 
FROM enrollments e 
JOIN users u ON e.student_id = u.id 
JOIN courses c ON e.course_id = c.id;

-- Add course
INSERT INTO courses (name, category, instructor, description) 
VALUES ('New Course', 'Technical', 'Dr. Smith', 'Description');

-- Delete course
DELETE FROM courses WHERE id = 1;
```

### Option 3: Python Script
```python
import sqlite3

conn = sqlite3.connect('backend/course_system.db')
c = conn.cursor()

# Add course
c.execute("INSERT INTO courses (name, category, instructor, description) VALUES (?, ?, ?, ?)",
          ('Python Advanced', 'Technical', 'Dr. Jones', 'Advanced Python'))

conn.commit()
conn.close()
```

## API Endpoints

All endpoints: http://localhost:5001/api/

- POST `/login` - Login
- POST `/register` - Register user
- GET `/courses` - Get all courses
- POST `/courses` - Create course (auth required)
- DELETE `/courses/<id>` - Delete course (auth required)
- POST `/courses/bulk` - Bulk upload courses (auth required)
- POST `/students/bulk` - Bulk upload students (auth required)
- POST `/enroll` - Enroll in course (auth required)
- GET `/enrollments/<username>` - Get user enrollments
- GET `/enrollments/by-dept-batch?department=X&batch=Y` - Filter students

## Troubleshooting

**"Server error"**: Make sure `python api.py` is running

**"Token invalid"**: Logout and login again

**"Database locked"**: Close all database connections and restart api.py

**CORS errors**: Backend has CORS enabled, should work from any origin

## Comparison

| Feature | LocalStorage | Database |
|---------|-------------|----------|
| Data persistence | Browser only | Permanent |
| Multi-user | No | Yes |
| Backend required | No | Yes |
| Excel upload | Yes | Yes |
| Direct DB edit | No | Yes |
| Security | Low | High (bcrypt, JWT) |

## Migration

To migrate from localStorage to database:
1. Export data from localStorage (browser console)
2. Format as Excel
3. Upload via database version

Or keep both versions for different use cases!
