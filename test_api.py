import requests
import json

BASE_URL = 'http://localhost:5001/api'

def test_register():
    print("Testing registration...")
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'test123',
        'role': 'student'
    }
    response = requests.post(f'{BASE_URL}/register', json=data)
    print(f"Register: {response.status_code} - {response.json()}")
    return response.status_code == 200

def test_login():
    print("\nTesting login...")
    data = {
        'username': 'admin',
        'password': 'admin123'
    }
    response = requests.post(f'{BASE_URL}/login', json=data)
    print(f"Login: {response.status_code} - {response.json()}")
    if response.status_code == 200:
        return response.json()['token']
    return None

def test_create_course(token):
    print("\nTesting course creation...")
    data = {
        'name': 'Python Programming',
        'category': 'Programming',
        'instructor': 'John Doe',
        'description': 'Learn Python basics',
        'limit': 30,
        'duration_hours': 40,
        'duration_minutes': 0,
        'prerequisites': 'None'
    }
    headers = {'Authorization': token}
    response = requests.post(f'{BASE_URL}/courses', json=data, headers=headers)
    print(f"Create Course: {response.status_code} - {response.json()}")

def test_get_courses():
    print("\nTesting get courses...")
    response = requests.get(f'{BASE_URL}/courses')
    print(f"Get Courses: {response.status_code} - {len(response.json())} courses found")

def run_tests():
    print("=== Database Backend Tests ===\n")
    print("Make sure api.py is running on port 5001!\n")
    
    try:
        test_register()
        token = test_login()
        if token:
            test_create_course(token)
            test_get_courses()
        print("\n=== Tests Complete ===")
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to server. Make sure api.py is running!")

if __name__ == '__main__':
    run_tests()
