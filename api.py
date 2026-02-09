from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import bcrypt
import jwt
import datetime
import secrets
from functools import wraps
DB_PATH = "course_system.db"

app = Flask(__name__)
import os  
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev-secret-key")
CORS(app)

def init_db():
    conn = sqlite3.connect('course_system.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT UNIQUE NOT NULL, 
                  email TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL, 
                  role TEXT DEFAULT 'student',
                  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                  last_login TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS courses
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
    
    c.execute('''CREATE TABLE IF NOT EXISTS enrollments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  student_id INTEGER NOT NULL, 
                  course_id INTEGER NOT NULL, 
                  department TEXT, 
                  batch TEXT, 
                  enrolled_date TEXT DEFAULT CURRENT_TIMESTAMP, 
                  status TEXT DEFAULT 'ongoing',
                  FOREIGN KEY(student_id) REFERENCES users(id) ON DELETE CASCADE,
                  FOREIGN KEY(course_id) REFERENCES courses(id) ON DELETE CASCADE)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS audit_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  action TEXT NOT NULL,
                  details TEXT,
                  ip_address TEXT,
                  timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    conn.commit()
    conn.close()

init_db()

def log_action(user_id, action, details=''):
    conn = sqlite3.connect('course_system.db')
    c = conn.cursor()
    ip = request.remote_addr
    c.execute('INSERT INTO audit_logs (user_id, action, details, ip_address) VALUES (?, ?, ?, ?)',
              (user_id, action, details, ip))
    conn.commit()
    conn.close()

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
        except:
            return jsonify({'message': 'Token invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# User Authentication
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400
    
    conn = sqlite3.connect('course_system.db')
    c = conn.cursor()
    c.execute('SELECT id, username, email, password, role FROM users WHERE username=?', (username,))
    user = c.fetchone()
    
    if user and bcrypt.checkpw(password.encode(), user[3].encode()):
        c.execute('UPDATE users SET last_login=? WHERE id=?', 
                  (datetime.datetime.now().isoformat(), user[0]))
        conn.commit()
        log_action(user[0], 'LOGIN', f'User {username} logged in')
        conn.close()
        
        token = jwt.encode({
            'user_id': user[0],
            'username': username,
            'role': user[4],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token, 'role': user[4], 'username': username, 'email': user[2]})
    
    conn.close()
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'student')
    
    if not username or not email or not password:
        return jsonify({'message': 'Username, email and password required'}), 400
    
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    try:
        conn = sqlite3.connect('course_system.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)',
                  (username, email, hashed, role))
        user_id = c.lastrowid
        log_action(user_id, 'REGISTER', f'New user {username} registered')
        conn.commit()
        conn.close()
        return jsonify({'message': 'User created successfully'})
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Username or email already exists'}), 400

# Course Management
@app.route('/api/courses', methods=['GET'])
def get_courses():
    conn = sqlite3.connect('course_system.db')
    c = conn.cursor()
    c.execute('SELECT * FROM courses')
    courses = c.fetchall()
    conn.close()
    
    return jsonify([{
        'id': c[0], 'name': c[1], 'category': c[2], 'instructor': c[3],
        'description': c[4], 'limit': c[5], 'duration_hours': c[6],
        'duration_minutes': c[7], 'prerequisites': c[8]
    } for c in courses])

@app.route('/api/courses', methods=['POST'])
@token_required
def create_course(current_user):
    data = request.json
    conn = sqlite3.connect('course_system.db')
    c = conn.cursor()
    c.execute('''INSERT INTO courses (name, category, instructor, description, 
                 limit_students, duration_hours, duration_minutes, prerequisites)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (data['name'], data['category'], data['instructor'], data['description'],
               data.get('limit', 0), data.get('duration_hours', 0),
               data.get('duration_minutes', 0), data.get('prerequisites', '')))
    course_id = c.lastrowid
    c.execute('SELECT id FROM users WHERE username=?', (current_user,))
    user = c.fetchone()
    if user:
        log_action(user[0], 'CREATE_COURSE', f'Created course: {data["name"]}')
    conn.commit()
    conn.close()
    return jsonify({'message': 'Course created successfully'})

@app.route('/api/courses/<int:course_id>', methods=['PUT'])
@token_required
def update_course(current_user, course_id):
    data = request.json
    conn = sqlite3.connect('course_system.db')
    c = conn.cursor()
    c.execute('''UPDATE courses SET name=?, category=?, instructor=?, description=?,
                 limit_students=?, duration_hours=?, duration_minutes=?, prerequisites=?
                 WHERE id=?''',
              (data['name'], data['category'], data['instructor'], data['description'],
               data.get('limit', 0), data.get('duration_hours', 0),
               data.get('duration_minutes', 0), data.get('prerequisites', ''), course_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Course updated successfully'})

@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
@token_required
def delete_course(current_user, course_id):
    conn = sqlite3.connect('course_system.db')
    c = conn.cursor()
    c.execute('DELETE FROM courses WHERE id=?', (course_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Course deleted successfully'})

# Enrollment Management
@app.route('/api/enroll', methods=['POST'])
@token_required
def enroll_student(current_user):
    data = request.json
    conn = sqlite3.connect('course_system.db')
    c = conn.cursor()
    
    c.execute('SELECT id FROM users WHERE username=?', (current_user,))
    user = c.fetchone()
    
    if user:
        c.execute('SELECT name FROM courses WHERE id=?', (data['course_id'],))
        course = c.fetchone()
        c.execute('''INSERT INTO enrollments (student_id, course_id, department, batch, status) 
                     VALUES (?, ?, ?, ?, ?)''',
                  (user[0], data['course_id'], data['department'], data['batch'], 'ongoing'))
        log_action(user[0], 'ENROLL', f'Enrolled in course: {course[0] if course else data["course_id"]}')
        conn.commit()
    
    conn.close()
    return jsonify({'message': 'Enrolled successfully'})

@app.route('/api/enrollments/<username>', methods=['GET'])
def get_enrollments(username):
    conn = sqlite3.connect('course_system.db')
    c = conn.cursor()
    c.execute('''SELECT c.name, e.department, e.batch, e.enrolled_date, e.status
                 FROM enrollments e
                 JOIN users u ON e.student_id = u.id
                 JOIN courses c ON e.course_id = c.id
                 WHERE u.username = ?''', (username,))
    enrollments = c.fetchall()
    conn.close()
    
    return jsonify([{
        'course': e[0], 'department': e[1], 'batch': e[2],
        'enrolled_date': e[3], 'status': e[4]
    } for e in enrollments])

# Statistics
@app.route('/api/stats', methods=['GET'])
@token_required
def get_stats(current_user):
    conn = sqlite3.connect('course_system.db')
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM courses')
    total_courses = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM users WHERE role="student"')
    total_students = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM enrollments')
    total_enrollments = c.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total_courses': total_courses,
        'total_students': total_students,
        'total_enrollments': total_enrollments
    })

@app.route('/api/user/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    conn = sqlite3.connect('course_system.db')
    c = conn.cursor()
    c.execute('SELECT id, username, email, role, created_at, last_login FROM users WHERE username=?', 
              (current_user,))
    user = c.fetchone()
    conn.close()
    
    if user:
        return jsonify({
            'id': user[0], 'username': user[1], 'email': user[2],
            'role': user[3], 'created_at': user[4], 'last_login': user[5]
        })
    return jsonify({'message': 'User not found'}), 404

@app.route('/api/courses/bulk', methods=['POST'])
@token_required
def bulk_create_courses(current_user):
    data = request.json
    courses = data.get('courses', [])
    conn = sqlite3.connect('course_system.db')
    c = conn.cursor()
    created = 0
    for course in courses:
        try:
            c.execute('''INSERT INTO courses (name, category, instructor, description, 
                         limit_students, duration_hours, duration_minutes, prerequisites)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                      (course['name'], course['category'], course['instructor'], course['description'],
                       course.get('limit', 0), course.get('duration_hours', 0),
                       course.get('duration_minutes', 0), course.get('prerequisites', '')))
            created += 1
        except:
            pass
    conn.commit()
    conn.close()
    return jsonify({'message': f'{created} courses created'})

@app.route('/api/students/bulk', methods=['POST'])
@token_required
def bulk_create_students(current_user):
    data = request.json
    students = data.get('students', [])
    conn = sqlite3.connect('course_system.db')
    c = conn.cursor()
    created = 0
    for student in students:
        try:
            hashed = bcrypt.hashpw(student['username'].encode(), bcrypt.gensalt()).decode()
            c.execute('INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)',
                      (student['username'], student.get('email', f"{student['username']}@example.com"), hashed, 'student'))
            student_id = c.lastrowid
            
            for course_name in student.get('ongoing_courses', []):
                c.execute('SELECT id FROM courses WHERE name=?', (course_name,))
                course = c.fetchone()
                if course:
                    c.execute('''INSERT INTO enrollments (student_id, course_id, department, batch, status)
                                 VALUES (?, ?, ?, ?, ?)''',
                              (student_id, course[0], student.get('department', ''), student.get('batch', ''), 'ongoing'))
            
            for course_name in student.get('completed_courses', []):
                c.execute('SELECT id FROM courses WHERE name=?', (course_name,))
                course = c.fetchone()
                if course:
                    c.execute('''INSERT INTO enrollments (student_id, course_id, department, batch, status)
                                 VALUES (?, ?, ?, ?, ?)''',
                              (student_id, course[0], student.get('department', ''), student.get('batch', ''), 'completed'))
            created += 1
        except:
            pass
    conn.commit()
    conn.close()
    return jsonify({'message': f'{created} students created'})

@app.route('/api/enrollments/by-dept-batch', methods=['GET'])
@token_required
def get_enrollments_by_dept_batch(current_user):
    dept = request.args.get('department', '')
    batch = request.args.get('batch', '')
    conn = DB_PATH = "course_system.db"

sqlite3.connect(DB_PATH)

    c = conn.cursor()
    
    query = '''SELECT u.username, e.department, e.batch, c.name, e.status
               FROM enrollments e
               JOIN users u ON e.student_id = u.id
               JOIN courses c ON e.course_id = c.id
               WHERE 1=1'''
    params = []
    
    if dept and dept != 'All Departments':
        query += ' AND e.department = ?'
        params.append(dept)
    if batch and batch != 'All Batches':
        query += ' AND e.batch = ?'
        params.append(batch)
    
    c.execute(query, params)
    results = c.fetchall()
    conn.close()
    
    students = {}
    for row in results:
        username = row[0]
        if username not in students:
            students[username] = {
                'username': username,
                'department': row[1],
                'batch': row[2],
                'ongoing': [],
                'completed': []
            }
        if row[4] == 'ongoing':
            students[username]['ongoing'].append(row[3])
        else:
            students[username]['completed'].append(row[3])
    
    return jsonify(list(students.values()))

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

