# System Architecture Diagram

## Complete System Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                 │
├─────────────────────────────────────────────────────────────────┤
│  index.html (Login)  →  dashboard.html (Main App)               │
│  script.js           →  dashboard.js                             │
│  style.css           →  dashboard.css                            │
└────────────┬────────────────────────────────────────────────────┘
             │ HTTP Requests (JSON)
             ↓
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND SERVERS                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐              ┌──────────────────┐         │
│  │   api.py         │              │   server.py      │         │
│  │   Port: 5001     │              │   Port: 5000     │         │
│  │                  │              │                  │         │
│  │ • Authentication │              │ • Email Service  │         │
│  │ • User Mgmt      │              │ • SMTP           │         │
│  │ • Course CRUD    │              │                  │         │
│  │ • Enrollments    │              │                  │         │
│  │ • Statistics     │              │                  │         │
│  └────────┬─────────┘              └──────────────────┘         │
│           │                                                       │
└───────────┼───────────────────────────────────────────────────────┘
            │ SQL Queries
            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE LAYER                                │
├─────────────────────────────────────────────────────────────────┤
│  database.py (Utilities)                                         │
│  course_system.db (SQLite)                                       │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │    users     │  │   courses    │  │ enrollments  │          │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤          │
│  │ id           │  │ id           │  │ id           │          │
│  │ username     │  │ name         │  │ student_id   │          │
│  │ email        │  │ category     │  │ course_id    │          │
│  │ password     │  │ instructor   │  │ department   │          │
│  │ role         │  │ description  │  │ batch        │          │
│  │ created_at   │  │ limit        │  │ enrolled_date│          │
│  │ last_login   │  │ duration     │  │ status       │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│  ┌──────────────────────────────────────────────────┐           │
│  │              audit_logs                          │           │
│  ├──────────────────────────────────────────────────┤           │
│  │ id, user_id, action, details, ip_address,        │           │
│  │ timestamp                                        │           │
│  └──────────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Examples

### 1. User Registration
```
User fills form → POST /api/register
                ↓
        Validate input
                ↓
        Hash password (bcrypt)
                ↓
        INSERT into users table
                ↓
        Log action in audit_logs
                ↓
        Return success response
```

### 2. User Login
```
User enters credentials → POST /api/login
                        ↓
                Fetch user from DB
                        ↓
                Verify password (bcrypt)
                        ↓
                Generate JWT token
                        ↓
                Update last_login
                        ↓
                Log action in audit_logs
                        ↓
                Return token + user info
```

### 3. Course Enrollment
```
User selects course → POST /api/enroll (with JWT)
                    ↓
            Verify JWT token
                    ↓
            Get user_id from token
                    ↓
            INSERT into enrollments
                    ↓
            Log action in audit_logs
                    ↓
            Return success
```

## Security Layers

```
┌─────────────────────────────────────────┐
│  Layer 1: Input Validation              │
│  • Required field checks                │
│  • Data type validation                 │
└─────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────┐
│  Layer 2: Authentication                │
│  • JWT token verification               │
│  • Token expiry check                   │
└─────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────┐
│  Layer 3: Authorization                 │
│  • Role-based access control            │
│  • User permission checks               │
└─────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────┐
│  Layer 4: Data Protection               │
│  • Bcrypt password hashing              │
│  • Parameterized SQL queries            │
│  • Foreign key constraints              │
└─────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────┐
│  Layer 5: Audit Logging                 │
│  • Action logging                       │
│  • IP address tracking                  │
│  • Timestamp recording                  │
└─────────────────────────────────────────┘
```

## File Organization

```
Project Root/
│
├── Frontend Files
│   ├── index.html          (Login page)
│   ├── dashboard.html      (Main dashboard)
│   ├── script.js           (Login logic)
│   ├── dashboard.js        (Dashboard logic)
│   ├── style.css           (Login styles)
│   └── dashboard.css       (Dashboard styles)
│
├── Backend Files
│   ├── api.py              (Main API server)
│   ├── server.py           (Email service)
│   └── database.py         (DB utilities)
│
├── Database Files
│   ├── setup_db.py         (DB initialization)
│   └── course_system.db    (SQLite database - created on setup)
│
├── Testing
│   └── test_api.py         (API tests)
│
├── Documentation
│   ├── DATABASE_SCHEMA.md
│   ├── DATABASE_SETUP.md
│   ├── QUICKSTART.md
│   ├── IMPLEMENTATION_SUMMARY.md
│   └── SYSTEM_ARCHITECTURE.md (this file)
│
├── Configuration
│   ├── requirements.txt    (Python dependencies)
│   ├── .env.example        (Config template)
│   └── .gitignore          (Git exclusions)
│
└── Assets
    ├── college_bg.jpg
    └── LOGO.png
```
