// Security utilities for BQ AI Assistant

/**
 * Sanitizes user input to prevent XSS attacks
 */
function sanitizeInput(input) {
    const div = document.createElement('div');
    div.textContent = input;
    return div.innerHTML;
}

/**
 * Validates email format
 */
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Validates password strength
 */
function validatePassword(password) {
    // At least 8 characters, one uppercase, one lowercase, one number, one special character
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return passwordRegex.test(password);
}

/**
 * Gets password strength feedback
 */
function getPasswordStrengthFeedback(password) {
    let strength = 0;
    let feedback = [];

    if (password.length >= 8) strength++;
    else feedback.push("At least 8 characters");

    if (/[a-z]/.test(password)) strength++;
    else feedback.push("At least one lowercase letter");

    if (/[A-Z]/.test(password)) strength++;
    else feedback.push("At least one uppercase letter");

    if (/\d/.test(password)) strength++;
    else feedback.push("At least one number");

    if (/[@$!%*?&]/.test(password)) strength++;
    else feedback.push("At least one special character");

    return {
        strength: strength,
        feedback: feedback,
        isStrong: strength >= 4
    };
}

/**
 * Encrypts data using a simple XOR cipher (for client-side use only)
 * For production, use proper encryption libraries
 */
function encryptData(data, key) {
    let encrypted = '';
    for (let i = 0; i < data.length; i++) {
        encrypted += String.fromCharCode(data.charCodeAt(i) ^ key.charCodeAt(i % key.length));
    }
    return btoa(encrypted); // Base64 encode
}

/**
 * Decrypts data using a simple XOR cipher (for client-side use only)
 */
function decryptData(encryptedData, key) {
    const encrypted = atob(encryptedData); // Base64 decode
    let decrypted = '';
    for (let i = 0; i < encrypted.length; i++) {
        decrypted += String.fromCharCode(encrypted.charCodeAt(i) ^ key.charCodeAt(i % key.length));
    }
    return decrypted;
}

/**
 * Generates a CSRF token
 */
function generateCSRFToken() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

/**
 * Gets CSRF token from cookie or generates a new one
 */
function getCSRFToken() {
    let token = getCookie('csrf_token');
    if (!token) {
        token = generateCSRFToken();
        setCookie('csrf_token', token, 7); // 7 days
    }
    return token;
}

/**
 * Sets a cookie
 */
function setCookie(name, value, days) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = "expires=" + date.toUTCString();
    document.cookie = name + "=" + value + ";" + expires + ";path=/;SameSite=Lax";
}

/**
 * Gets a cookie value
 */
function getCookie(name) {
    const nameEQ = name + "=";
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.indexOf(nameEQ) === 0) {
            return cookie.substring(nameEQ.length);
        }
    }
    return null;
}

/**
 * Deletes a cookie
 */
function deleteCookie(name) {
    setCookie(name, "", -1);
}

/**
 * Logs security events
 */
function logSecurityEvent(eventType, details) {
    const event = {
        timestamp: new Date().toISOString(),
        eventType: eventType,
        details: details,
        userAgent: navigator.userAgent,
        url: window.location.href
    };
    console.log('Security Event:', event);
    // In production, send this to a logging service
}

/**
 * Initializes security features on page load
 */
function initializeSecurity() {
    // Get or generate CSRF token
    const csrfToken = getCSRFToken();
    
    // Add CSRF token to all forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'csrf_token';
        input.value = csrfToken;
        form.appendChild(input);
    });
    
    // Log page load
    logSecurityEvent('page_load', 'User accessed the application');
    
    // Monitor for suspicious activity
    document.addEventListener('beforeunload', function() {
        logSecurityEvent('page_unload', 'User left the page');
    });
}

// Initialize security on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeSecurity();
});
