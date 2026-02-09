import openpyxl
from openpyxl import Workbook

# Create Sample Courses Excel
wb_courses = Workbook()
ws_courses = wb_courses.active
ws_courses.title = "Courses"

courses_data = [
    ['Name', 'Category', 'Instructor', 'Description', 'Limit', 'Duration (hours)', 'Duration (minutes)', 'Prerequisites'],
    ['Data Structures', 'Technical', 'Ms. Diya Stella Mathew', 'Learn fundamental data structures and algorithms', '100', '3', '30', 'Basic Programming'],
    ['Graphic Design', 'Technical', 'Ms. Jessica Walsh', 'Learn visual design principles using Canva to create logos, posters, and social media creatives', '140', '3', '20', 'Basic computer knowledge'],
    ['UI / UX Design', 'Technical', 'Dr. Don Norman', 'Understand user experience and usability testing for websites and mobile applications', '140', '5', '40', 'Basic design sense and computer skills'],
    ['Data Analysis (Basics)', 'Technical', 'Mr. Alex The Analyst', 'Introduction to data analysis using Excel and basic Power BI', '140', '1', '20', 'Basic mathematics and Excel knowledge'],
    ['Human Resource Management (HR)', 'Non Technical', 'Prof. Peter Cappelli', 'Learn recruitment, employee management, payroll basics, and organizational behavior for corporate environments', '100', '3', '30', 'Interest in people management'],
    ['Journalism & Mass Communication', 'Non Technical', 'Ms. Christiane Amanpour', 'Covers reporting, news writing, digital media, broadcasting, and communication ethics.', '75', '6', '0', 'Strong interest in writing and communication'],
    ['Business Analytics (Non-Tech)', 'Non Technical', 'Prof. Ramesh Sharda', 'Focuses on business decision-making using data interpretation, reports, KPIs, and visualization without programming.', '50', '5', '15', 'Basic understanding of business concepts'],
    ['Web Development', 'Technical', 'Prof. Akash C Anand', 'Complete web development with HTML CSS JS', '150', '4', '0', 'HTML Basics'],
    ['Machine Learning', 'Technical', 'Dr. Anderson', 'Introduction to ML algorithms and applications', '50', '5', '15', 'Python Programming'],
    ['Digital Marketing', 'Non-Technical', 'Ms. Wilson', 'Learn digital marketing strategies and tools', '200', '2', '45', 'None'],
    ['Project Management', 'Non-Technical', 'Mr. Brown', 'Professional project management methodologies', '100', '3', '0', 'None'],
    ['Database Systems', 'Technical', 'Dr. Aiswarya', 'Relational databases and SQL programming', '120', '4', '30', 'Basic Programming'],
    ['Public Speaking', 'Non-Technical', 'Ms. Davis', 'Improve presentation and communication skills', '80', '1', '30', 'None'],
    ['Cybersecurity', 'Technical', 'Prof. Garcia', 'Network security and ethical hacking basics', '75', '6', '0', 'Networking Fundamentals']
]

for row in courses_data:
    ws_courses.append(row)

wb_courses.save('sample_courses.xlsx')

# Create Sample Students Excel
wb_students = Workbook()
ws_students = wb_students.active
ws_students.title = "Students"

students_data = [
    ['Username', 'Student Name', 'Department', 'Batch', 'Course Ongoing', 'Course Completed'],
    ['Priya1', 'Priya Sharma', 'Computer Science', '2021-2024', 'Python Programming,Web Development', 'Communication Skills,Journalism & Mass Communication'],
    ['Meera2', 'Meera Johnson', 'Data Science', '2024-2027', 'Data Structures', 'Python Programming,Digital Marketing'],
    ['Kavya3', 'Kavya Brown', 'Psychology', '2019-2022', 'Project Management', 'Public Speaking'],
    ['Sneha4', 'Sneha Wilson', 'Commerce', '2022-2025', 'Machine Learning,Database Systems', 'None'],
    ['Steve5', 'Steve Harrington', 'English', '2020-2023', 'Cybersecurity', 'Web Development,Data Structures'],
    ['Janis6', 'Megha R', 'Psychology', '2022-2025', 'UI / UX Design,Graphic Design', 'Design Thinking Basics'],
    ['Akash7', 'Akash C Anand', 'Electronics and Communication system', '2021-2024', 'Cybersecurity,Web Development,Data Structures', 'Python Programming,Communication Skills,Database Systems'],
    ['Arun8', 'Arun Prakash', 'Computer Science', '2021-2024', 'Web Development,Database Systems', 'C Programming,HTML Basics'],
    ['Nisha9', 'Nisha K', 'B.A English', '2022-2025', 'Digital Marketing,Content Strategy', 'Creative Writing'],
    ['Diya10', 'Diya Stella Mathew', 'Computer Science', '2021-2024', 'Python Programming,Web Development', 'Communication Skills,Cybersecurity,Journalism & Mass Communication'],
    ['Jacob11', 'Priya N', 'Sociology', '2022-2025', 'Public Speaking,Journalism & Mass Communication', 'Interpersonal Communication'],
    ['Vignesh12', 'Vignesh R', 'Computer Applications', '2021-2024', 'Database Systems,Data Structures', 'Operating Systems Basics'],
    ['Karthik13', 'Karthik S', 'Information Technology', '2021-2024', 'Machine Learning,Cybersecurity', 'Python Programming,Statistics Basics'],
    ['Henry14', 'Henry Davids', 'Computer Science', '2021-2024', 'Cybersecurity,Web Development,Data Structures,Python Programming,Journalism & Mass Communication', 'None']
]

for row in students_data:
    ws_students.append(row)

wb_students.save('sample_students.xlsx')

print("Sample Excel files created successfully!")
print("- sample_courses.xlsx (15 courses)")
print("- sample_students.xlsx (14 students)")
