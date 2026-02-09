# Quick Reference: Edit Database

## Start Backend
```bash
cd C:\Users\mtpoo\Desktop\Project Login Page\Web page\backend
python api.py
```

## Method 1: Web Interface (Easiest)
1. Open `frontend/index-db.html`
2. Login: `admin` / `admin123`
3. Add/Edit/Delete via dashboard

## Method 2: Direct SQL
```bash
cd C:\Users\mtpoo\Desktop\Project Login Page\Web page\backend
sqlite3 course_system.db
```

### Common Commands:
```sql
-- View all courses
SELECT * FROM courses;

-- Add course
INSERT INTO courses (name, category, instructor, description, limit_students, duration_hours, duration_minutes) 
VALUES ('New Course', 'Technical', 'Dr. Smith', 'Description', 50, 3, 30);

-- Update course
UPDATE courses SET name='Updated Name' WHERE id=1;

-- Delete course
DELETE FROM courses WHERE id=1;

-- View students
SELECT * FROM users WHERE role='student';

-- View enrollments
SELECT u.username, c.name, e.status 
FROM enrollments e 
JOIN users u ON e.student_id=u.id 
JOIN courses c ON e.course_id=c.id;

-- Exit
.quit
```

## Method 3: Excel Upload
1. Edit `sample_documents/sample_courses.xlsx`
2. Login to dashboard
3. Courses → Upload Excel
4. Select file → Upload

## Method 4: Python Script
```python
import sqlite3

conn = sqlite3.connect('backend/course_system.db')
c = conn.cursor()

# Add course
c.execute("""INSERT INTO courses 
             (name, category, instructor, description) 
             VALUES (?, ?, ?, ?)""",
          ('Python Advanced', 'Technical', 'Dr. Jones', 'Advanced Python'))

# Get all courses
c.execute("SELECT * FROM courses")
print(c.fetchall())

conn.commit()
conn.close()
```

## Database Location
```
C:\Users\mtpoo\Desktop\Project Login Page\Web page\backend\course_system.db
```

## Backup Database
```bash
copy course_system.db course_system_backup.db
```

## Reset Database
```bash
cd database
python setup_db.py
```

## Check if Backend Running
Open browser: http://localhost:5001/api/courses
Should show JSON response

## Troubleshooting
- **Database locked**: Close all connections, restart api.py
- **Changes not showing**: Refresh browser page
- **Server not running**: Run `python api.py` in backend folder
