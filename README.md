# Sample Documents

This folder contains sample Excel files matching the format used in the web application.

## Files

### sample_courses.xlsx
Contains 15 sample courses with columns:
- Name, Category, Instructor, Description
- Limit, Duration (hours), Duration (minutes)
- Prerequisites

Includes courses like:
- Data Structures, Web Development, Machine Learning
- Graphic Design, UI/UX Design, Cybersecurity
- Digital Marketing, Public Speaking, HR Management

### sample_students.xlsx
Contains 14 sample students with columns:
- Username, Student Name, Department, Batch
- Course Ongoing (comma-separated)
- Course Completed (comma-separated)

Includes students from various departments:
- Computer Science, Data Science, Psychology
- Commerce, English, Information Technology

## Usage

1. **Upload to Dashboard**: Use the "Upload Excel" buttons in the web application
2. **Course Upload**: Navigate to Courses → Upload Excel
3. **Student Upload**: Navigate to Get Details → Upload Student Data

## Auto-Generated Accounts

When uploading student data, login accounts are automatically created:
- Username: As specified in Excel
- Password: Same as username (e.g., Priya1/Priya1)

## Regenerate Files

Run `python generate_samples.py` to recreate the Excel files with the same data.
