// Database-connected login script

function showTab(tabName) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.login-form').forEach(form => form.classList.remove('active'));
    
    if (tabName === 'admin') {
        document.querySelector('.tab-btn:first-child').classList.add('active');
        document.getElementById('adminForm').classList.add('active');
    } else {
        document.querySelector('.tab-btn:last-child').classList.add('active');
        document.getElementById('studentForm').classList.add('active');
    }
    hideMessage();
}

function showMessage(text, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = text;
    messageDiv.className = `message ${type}`;
    messageDiv.style.display = 'block';
}

function hideMessage() {
    document.getElementById('message').style.display = 'none';
}

// Admin/Student login
document.getElementById('adminForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('adminUsername').value;
    const password = document.getElementById('adminPassword').value;
    
    try {
        const response = await fetch('http://localhost:5001/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            localStorage.setItem('authToken', data.token);
            localStorage.setItem('loginType', data.role);
            localStorage.setItem('username', data.username);
            showMessage('Login successful!', 'success');
            setTimeout(() => window.location.href = 'dashboard-db.html', 1000);
        } else {
            showMessage(data.message || 'Invalid credentials', 'error');
        }
    } catch (e) {
        showMessage('Server error. Make sure backend is running on port 5001', 'error');
    }
});

document.getElementById('studentForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('studentUsername').value;
    const password = document.getElementById('studentPassword').value;
    
    try {
        const response = await fetch('http://localhost:5001/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            localStorage.setItem('authToken', data.token);
            localStorage.setItem('loginType', data.role);
            localStorage.setItem('username', data.username);
            showMessage('Login successful!', 'success');
            setTimeout(() => window.location.href = 'dashboard-db.html', 1000);
        } else {
            showMessage(data.message || 'Invalid credentials', 'error');
        }
    } catch (e) {
        showMessage('Server error. Make sure backend is running on port 5001', 'error');
    }
});
