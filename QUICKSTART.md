# Quick Start Guide

## Setup Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python setup_db.py
```
This creates the database with a default admin account:
- Username: `admin`
- Password: `admin123`

### 3. Start Backend Server
```bash
python api.py
```
API runs on: http://localhost:5001

### 4. (Optional) Start Email Server
```bash
python server.py
```
Email service runs on: http://localhost:5000

### 5. Open Frontend
Open `index.html` in your browser or use a local server:
```bash
python -m http.server 8000
```
Then visit: http://localhost:8000

## Testing the System

Run automated tests:
```bash
python test_api.py
```

## What's Included

### Database Tables
- **users**: Secure user authentication with bcrypt
- **courses**: Course catalog management
- **enrollments**: Student enrollment tracking
- **audit_logs**: Security audit trail

### Security Features
✓ Bcrypt password hashing
✓ JWT token authentication
✓ Audit logging with IP tracking
✓ SQL injection protection
✓ Input validation

### API Endpoints
- User registration & login
- Course CRUD operations
- Enrollment management
- User profile management
- System statistics

## File Structure
```
├── api.py              # Main backend API
├── server.py           # Email service
├── database.py         # Database utilities
├── setup_db.py         # Database initialization
├── test_api.py         # API tests
├── index.html          # Login page
├── dashboard.html      # Dashboard
├── requirements.txt    # Python dependencies
└── DATABASE_SCHEMA.md  # Database documentation
```

## Next Steps

1. Change the default admin password
2. Configure email settings (see EMAIL_SETUP.txt)
3. Customize frontend to use the new API endpoints
4. Add more features as needed

## Troubleshooting

**Database locked error**: Close all connections and restart api.py

**Import errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`

**Connection refused**: Ensure api.py is running on port 5001
