# Database Backend Setup Guide

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize the database:
```bash
python setup_db.py
```

## Database Structure

The system uses SQLite with 4 main tables:
- **users**: Authentication and user profiles
- **courses**: Course catalog
- **enrollments**: Student-course relationships
- **audit_logs**: Security audit trail

See DATABASE_SCHEMA.md for detailed schema information.

## API Endpoints

### Authentication
- POST `/api/register` - Register new user (username, email, password, role)
- POST `/api/login` - Login (username, password) → returns JWT token

### User Management
- GET `/api/user/profile` - Get current user profile (requires auth)

### Course Management
- GET `/api/courses` - List all courses
- POST `/api/courses` - Create course (requires auth)
- PUT `/api/courses/<id>` - Update course (requires auth)
- DELETE `/api/courses/<id>` - Delete course (requires auth)

### Enrollment
- POST `/api/enroll` - Enroll in course (requires auth)
- GET `/api/enrollments/<username>` - Get user enrollments

### Statistics
- GET `/api/stats` - Get system statistics (requires auth)

## Running the Server

Start the API server:
```bash
python api.py
```

Server runs on http://localhost:5001

## Security Features

1. **Password Security**: Bcrypt hashing with salt
2. **Authentication**: JWT tokens (24-hour expiry)
3. **Audit Logging**: All actions logged with IP address
4. **Input Validation**: Required field checks
5. **SQL Injection Protection**: Parameterized queries

## Default Credentials

After running setup_db.py:
- Username: admin
- Password: admin123
- Role: admin

**IMPORTANT**: Change the admin password immediately in production!

## Frontend Integration

Include JWT token in Authorization header:
```javascript
headers: {
    'Authorization': token,
    'Content-Type': 'application/json'
}
```
