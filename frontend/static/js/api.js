// API utility functions for BQ AI Assistant

const API_BASE_URL = '/api';

/**
 * Performs a health check on the API
 */
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        console.log('Health check:', data);
        return data.status === 'healthy';
    } catch (error) {
        console.error('Health check failed:', error);
        return false;
    }
}

/**
 * Logs in a user with email and password
 */
async function login(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await response.json();
        if (data.success) {
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);
            console.log('Login successful');
            return data;
        } else {
            console.error('Login failed:', data.error);
            return null;
        }
    } catch (error) {
        console.error('Login error:', error);
        return null;
    }
}

/**
 * Registers a new user
 */
async function registerUser(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await response.json();
        if (data.success) {
            console.log('Registration successful');
            return data;
        } else {
            console.error('Registration failed:', data.error);
            return null;
        }
    } catch (error) {
        console.error('Registration error:', error);
        return null;
    }
}

/**
 * Gets the current user information
 */
async function getCurrentUser() {
    try {
        const token = localStorage.getItem('access_token');
        if (!token) {
            console.warn('No access token found');
            return null;
        }
        
        const response = await fetch(`${API_BASE_URL}/users/me`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        const data = await response.json();
        if (data.success) {
            return data.user;
        } else {
            console.error('Failed to get user:', data.error);
            return null;
        }
    } catch (error) {
        console.error('Get user error:', error);
        return null;
    }
}

/**
 * Creates a new meeting
 */
async function createMeeting(title, userId) {
    try {
        const token = localStorage.getItem('access_token');
        if (!token) {
            console.warn('No access token found');
            return null;
        }
        
        const response = await fetch(`${API_BASE_URL}/meetings`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ title, user_id: userId })
        });
        const data = await response.json();
        if (data.success) {
            console.log('Meeting created:', data.meeting_id);
            return data;
        } else {
            console.error('Failed to create meeting:', data.error);
            return null;
        }
    } catch (error) {
        console.error('Create meeting error:', error);
        return null;
    }
}

/**
 * Gets a specific meeting
 */
async function getMeeting(meetingId) {
    try {
        const token = localStorage.getItem('access_token');
        if (!token) {
            console.warn('No access token found');
            return null;
        }
        
        const response = await fetch(`${API_BASE_URL}/meetings/${meetingId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        const data = await response.json();
        if (data.success) {
            return data;
        } else {
            console.error('Failed to get meeting:', data.error);
            return null;
        }
    } catch (error) {
        console.error('Get meeting error:', error);
        return null;
    }
}

/**
 * Gets AI assistance for a question
 */
async function getAIAssist(question, context) {
    try {
        const response = await fetch(`${API_BASE_URL}/ai/assist`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question, context })
        });
        const data = await response.json();
        if (data.success) {
            return data.answer;
        } else {
            console.error('AI assist failed:', data.error);
            return null;
        }
    } catch (error) {
        console.error('AI assist error:', error);
        return null;
    }
}

/**
 * Transcribes audio
 */
async function transcribeAudio(audioData) {
    try {
        const response = await fetch(`${API_BASE_URL}/transcribe`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ audio: audioData })
        });
        const data = await response.json();
        if (data.success) {
            return data.transcript;
        } else {
            console.error('Transcription failed:', data.error);
            return null;
        }
    } catch (error) {
        console.error('Transcription error:', error);
        return null;
    }
}

/**
 * Subscribes a user to a billing plan
 */
async function subscribeToPlan(plan, userId) {
    try {
        const token = localStorage.getItem('access_token');
        if (!token) {
            console.warn('No access token found');
            return null;
        }
        
        const response = await fetch(`${API_BASE_URL}/billing/subscribe`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ plan, user_id: userId })
        });
        const data = await response.json();
        if (data.success) {
            console.log('Subscription successful');
            return data;
        } else {
            console.error('Subscription failed:', data.error);
            return null;
        }
    } catch (error) {
        console.error('Subscription error:', error);
        return null;
    }
}

/**
 * Logs out the current user
 */
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    console.log('Logged out');
}

/**
 * Gets the access token from local storage
 */
function getAccessToken() {
    return localStorage.getItem('access_token');
}

/**
 * Checks if user is authenticated
 */
function isAuthenticated() {
    return !!getAccessToken();
}

// Initialize API on page load
document.addEventListener('DOMContentLoaded', function() {
    checkHealth();
});
