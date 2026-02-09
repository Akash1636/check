import sqlite3
import bcrypt

def setup_database():
    conn = sqlite3.connect('course_system.db')
    c = conn.cursor()
    
    # Drop existing tables
    c.execute('DROP TABLE IF EXISTS audit_logs')
    c.execute('DROP TABLE IF EXISTS enrollments')
    c.execute('DROP TABLE IF EXISTS courses')
    c.execute('DROP TABLE IF EXISTS users')
    
    # Create tables
    c.execute('''CREATE TABLE users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT UNIQUE NOT NULL, 
                  email TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL, 
                  role TEXT DEFAULT 'student',
                  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                  last_login TEXT)''')
    
    c.execute('''CREATE TABLE courses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT NOT NULL, 
                  category TEXT, 
                  instructor TEXT, 
                  description TEXT, 
                  limit_students INTEGER DEFAULT 0, 
                  duration_hours INTEGER DEFAULT 0, 
                  duration_minutes INTEGER DEFAULT 0, 
                  prerequisites TEXT,
                  created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE enrollments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  student_id INTEGER NOT NULL, 
                  course_id INTEGER NOT NULL, 
                  department TEXT, 
                  batch TEXT, 
                  enrolled_date TEXT DEFAULT CURRENT_TIMESTAMP, 
                  status TEXT DEFAULT 'ongoing',
                  FOREIGN KEY(student_id) REFERENCES users(id) ON DELETE CASCADE,
                  FOREIGN KEY(course_id) REFERENCES courses(id) ON DELETE CASCADE)''')
    
    c.execute('''CREATE TABLE audit_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  action TEXT NOT NULL,
                  details TEXT,
                  ip_address TEXT,
                  timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    # Create sample admin user
    admin_password = bcrypt.hashpw('admin123'.encode(), bcrypt.gensalt()).decode()
    c.execute('INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)',
              ('admin', 'admin@example.com', admin_password, 'admin'))
    
    conn.commit()
    conn.close()
    print("Database setup complete!")
    print("Sample admin user created - username: admin, password: admin123")

if __name__ == '__main__':
    setup_database()
