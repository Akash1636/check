// API Configuration
const API_BASE_URL = 'http://localhost:5001/api';

// Store JWT token
let authToken = localStorage.getItem('authToken') || '';

// API Helper Functions
const api = {
    setToken(token) {
        authToken = token;
        localStorage.setItem('authToken', token);
    },
    
    clearToken() {
        authToken = '';
        localStorage.removeItem('authToken');
    },
    
    async request(endpoint, options = {}) {
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...(authToken && { 'Authorization': authToken })
            },
            ...options
        };
        
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'API request failed');
        }
        
        return data;
    },
    
    // Auth
    async login(username, password) {
        const data = await this.request('/login', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
        if (data.token) this.setToken(data.token);
        return data;
    },
    
    async register(username, email, password, role = 'student') {
        return await this.request('/register', {
            method: 'POST',
            body: JSON.stringify({ username, email, password, role })
        });
    },
    
    // Courses
    async getCourses() {
        return await this.request('/courses');
    },
    
    async createCourse(courseData) {
        return await this.request('/courses', {
            method: 'POST',
            body: JSON.stringify(courseData)
        });
    },
    
    async updateCourse(courseId, courseData) {
        return await this.request(`/courses/${courseId}`, {
            method: 'PUT',
            body: JSON.stringify(courseData)
        });
    },
    
    async deleteCourse(courseId) {
        return await this.request(`/courses/${courseId}`, {
            method: 'DELETE'
        });
    },
    
    // Enrollments
    async enroll(courseId, department, batch) {
        return await this.request('/enroll', {
            method: 'POST',
            body: JSON.stringify({ course_id: courseId, department, batch })
        });
    },
    
    async getEnrollments(username) {
        return await this.request(`/enrollments/${username}`);
    },
    
    // Profile
    async getProfile() {
        return await this.request('/user/profile');
    },
    
    // Stats
    async getStats() {
        return await this.request('/stats');
    }
};
