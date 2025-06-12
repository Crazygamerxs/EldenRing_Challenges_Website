// Frontend Security Utilities for EldenRing Challenges Website

/**
 * Initialize security measures on app startup
 */
export const initializeSecurity = () => {
    // Disable right-click context menu in production
    if (process.env.NODE_ENV === 'production') {
        document.addEventListener('contextmenu', (e) => {
            e.preventDefault();
        });
        
        // Disable F12, Ctrl+Shift+I, Ctrl+U
        document.addEventListener('keydown', (e) => {
            if (e.key === 'F12' || 
                (e.ctrlKey && e.shiftKey && e.key === 'I') ||
                (e.ctrlKey && e.key === 'u')) {
                e.preventDefault();
            }
        });
    }
    
    // Set security headers for fetch requests
    const originalFetch = window.fetch;
    window.fetch = function(...args) {
        if (args[1]) {
            args[1].credentials = args[1].credentials || 'include';
        } else {
            args[1] = { credentials: 'include' };
        }
        return originalFetch.apply(this, args);
    };
};

/**
 * Sanitize text input to prevent XSS
 * @param {string} input - The input string to sanitize
 * @returns {string} - Sanitized string
 */
export const sanitizeInput = (input) => {
    if (!input || typeof input !== 'string') {
        return '';
    }
    
    // HTML escape
    const div = document.createElement('div');
    div.textContent = input;
    let sanitized = div.innerHTML;
    
    // Remove null bytes and control characters
    sanitized = sanitized.replace(/[\x00-\x1F\x7F]/g, '');
    
    // Limit length to prevent DoS
    if (sanitized.length > 10000) {
        sanitized = sanitized.substring(0, 10000);
    }
    
    return sanitized.trim();
};

/**
 * Validate username format
 * @param {string} username - Username to validate
 * @returns {object} - Validation result with valid boolean and error message
 */
export const validateUsername = (username) => {
    if (!username) {
        return { valid: false, error: 'Username is required' };
    }
    
    if (username.length < 3 || username.length > 30) {
        return { valid: false, error: 'Username must be between 3 and 30 characters' };
    }
    
    if (!/^[a-zA-Z0-9_-]+$/.test(username)) {
        return { valid: false, error: 'Username can only contain letters, numbers, underscores, and hyphens' };
    }
    
    // Block common admin usernames
    const blockedUsernames = [
        'admin', 'administrator', 'root', 'system', 'api', 'www', 'mail',
        'email', 'user', 'test', 'guest', 'demo', 'support', 'help',
        'moderator', 'mod', 'owner', 'superuser', 'staff'
    ];
    
    if (blockedUsernames.includes(username.toLowerCase())) {
        return { valid: false, error: 'This username is not allowed' };
    }
    
    return { valid: true };
};

/**
 * Validate email format
 * @param {string} email - Email to validate
 * @returns {object} - Validation result with valid boolean and error message
 */
export const validateEmail = (email) => {
    if (!email) {
        return { valid: false, error: 'Email is required' };
    }
    
    // Basic format check
    if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email)) {
        return { valid: false, error: 'Invalid email format' };
    }
    
    // Check length
    if (email.length > 254) {
        return { valid: false, error: 'Email address too long' };
    }
    
    // Split local and domain parts
    const parts = email.split('@');
    if (parts.length !== 2) {
        return { valid: false, error: 'Invalid email format' };
    }
    
    const [local, domain] = parts;
    
    // Validate local part
    if (local.length > 64) {
        return { valid: false, error: 'Email local part too long' };
    }
    
    // Validate domain part
    if (domain.length > 253) {
        return { valid: false, error: 'Email domain too long' };
    }
    
    // Block temporary email domains (optional)
    const blockedDomains = [
        '10minutemail.com', 'tempmail.org', 'guerrillamail.com',
        'mailinator.com', 'throwaway.email', 'temp-mail.org',
        'yopmail.com', 'maildrop.cc', '33mail.com'
    ];
    
    if (blockedDomains.includes(domain.toLowerCase())) {
        return { valid: false, error: 'Temporary email addresses are not allowed' };
    }
    
    return { valid: true };
};

/**
 * Validate password strength
 * @param {string} password - Password to validate
 * @returns {object} - Validation result with valid boolean and error message
 */
export const validatePassword = (password) => {
    if (!password) {
        return { valid: false, error: 'Password is required' };
    }
    
    if (password.length < 8) {
        return { valid: false, error: 'Password must be at least 8 characters long' };
    }
    
    if (password.length > 128) {
        return { valid: false, error: 'Password cannot exceed 128 characters' };
    }
    
    // Check for at least one uppercase letter
    if (!/[A-Z]/.test(password)) {
        return { valid: false, error: 'Password must contain at least one uppercase letter' };
    }
    
    // Check for at least one lowercase letter
    if (!/[a-z]/.test(password)) {
        return { valid: false, error: 'Password must contain at least one lowercase letter' };
    }
    
    // Check for at least one number
    if (!/\d/.test(password)) {
        return { valid: false, error: 'Password must contain at least one number' };
    }
    
    // Check for at least one special character
    if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) {
        return { valid: false, error: 'Password must contain at least one special character' };
    }
    
    // Check for common weak passwords
    const commonPasswords = [
        'password', '12345678', 'qwerty123', 'abc123456', 'password123',
        'admin123', 'letmein123', 'welcome123', 'monkey123', '123456789'
    ];
    
    if (commonPasswords.includes(password.toLowerCase())) {
        return { valid: false, error: 'This password is too common. Please choose a stronger password' };
    }
    
    return { valid: true };
};

/**
 * Validate submission URL
 * @param {string} url - URL to validate
 * @returns {object} - Validation result with valid boolean and error message
 */
export const validateSubmissionUrl = (url) => {
    if (!url) {
        return { valid: false, error: 'URL is required' };
    }
    
    // Basic URL validation
    try {
        const urlObj = new URL(url);
        
        // Check protocol
        if (!['http:', 'https:'].includes(urlObj.protocol)) {
            return { valid: false, error: 'URL must use HTTP or HTTPS protocol' };
        }
        
        // Check if it's a safe domain
        const allowedDomains = [
            'youtube.com', 'www.youtube.com', 'youtu.be', 'm.youtube.com',
            'twitch.tv', 'www.twitch.tv', 'clips.twitch.tv',
            'drive.google.com', 'docs.google.com',
            'vimeo.com', 'www.vimeo.com', 'player.vimeo.com',
            'streamable.com', 'www.streamable.com',
            'imgur.com', 'i.imgur.com',
            'dropbox.com', 'www.dropbox.com'
        ];
        
        if (!allowedDomains.includes(urlObj.hostname.toLowerCase())) {
            return { valid: false, error: 'URL must be from an approved video hosting platform' };
        }
        
        // Block suspicious patterns in URL
        const suspiciousPatterns = [
            /javascript:/i, /data:/i, /file:/i, /ftp:/i, /blob:/i,
            /<script/i, /<\/script/i, /onclick/i, /onerror/i, /onload/i
        ];
        
        for (const pattern of suspiciousPatterns) {
            if (pattern.test(url)) {
                return { valid: false, error: 'URL contains suspicious content' };
            }
        }
        
        return { valid: true };
        
    } catch (error) {
        return { valid: false, error: 'Invalid URL format' };
    }
};

/**
 * Validate time format (HH:MM:SS)
 * @param {string} timeString - Time string to validate
 * @returns {object} - Validation result with valid boolean and error message
 */
export const validateTimeFormat = (timeString) => {
    if (!timeString) {
        return { valid: false, error: 'Time is required' };
    }
    
    if (!/^\d{2}:\d{2}:\d{2}$/.test(timeString)) {
        return { valid: false, error: 'Time must be in HH:MM:SS format' };
    }
    
    const parts = timeString.split(':');
    const hours = parseInt(parts[0], 10);
    const minutes = parseInt(parts[1], 10);
    const seconds = parseInt(parts[2], 10);
    
    if (hours < 0 || hours > 23 || minutes < 0 || minutes >= 60 || seconds < 0 || seconds >= 60) {
        return { valid: false, error: 'Invalid time values' };
    }
    
    // Check for reasonable maximum time (24 hours)
    const totalSeconds = hours * 3600 + minutes * 60 + seconds;
    if (totalSeconds > 86400) {
        return { valid: false, error: 'Time cannot exceed 24 hours' };
    }
    
    return { valid: true };
};

/**
 * Secure API wrapper with CSRF protection and error handling
 * @param {string} url - API endpoint URL
 * @param {object} options - Fetch options
 * @returns {Promise} - Fetch promise with enhanced security
 */
export const secureApiCall = async (url, options = {}) => {
    try {
        // Get CSRF token
        const csrfToken = getCsrfToken();
        
        // Default headers
        const defaultHeaders = {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        };
        
        // Merge headers
        const headers = { ...defaultHeaders, ...options.headers };
        
        // Default options
        const defaultOptions = {
            credentials: 'include',
            headers,
        };
        
        // Merge options
        const finalOptions = { ...defaultOptions, ...options };
        
        // Make the request
        const response = await fetch(url, finalOptions);
        
        // Check for security-related errors
        if (response.status === 429) {
            throw new Error('Rate limit exceeded. Please try again later.');
        }
        
        if (response.status === 403) {
            throw new Error('Access denied. Please check your permissions.');
        }
        
        if (response.status === 401) {
            throw new Error('Authentication required. Please log in.');
        }
        
        return response;
        
    } catch (error) {
        console.error('Secure API call failed:', error);
        throw error;
    }
};

/**
 * Get CSRF token from cookies or meta tag
 * @returns {string} - CSRF token
 */
export const getCsrfToken = () => {
    // Try to get from cookie first
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    
    if (cookieValue) {
        return cookieValue;
    }
    
    // Try to get from meta tag
    const metaTag = document.querySelector('meta[name="csrf-token"]');
    if (metaTag) {
        return metaTag.getAttribute('content');
    }
    
    return '';
};

/**
 * Log security events for monitoring
 * @param {string} event - Event type
 * @param {object} details - Event details
 */
export const logSecurityEvent = (event, details = {}) => {
    if (process.env.NODE_ENV === 'development') {
        console.warn('Security Event:', event, details);
    }
    
    // In production, you might want to send this to your monitoring service
    if (process.env.NODE_ENV === 'production') {
        // Example: Send to monitoring endpoint
        // fetch('/api/security-log/', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({ event, details, timestamp: new Date().toISOString() })
        // }).catch(() => {}); // Fail silently
    }
};

/**
 * Check if current session is valid
 * @returns {Promise<boolean>} - Session validity
 */
export const checkSessionValidity = async () => {
    try {
        const response = await secureApiCall('/api/user-profile/');
        return response.ok;
    } catch (error) {
        logSecurityEvent('session_check_failed', { error: error.message });
        return false;
    }
};

/**
 * Validate form data before submission
 * @param {object} formData - Form data to validate
 * @param {object} validationRules - Validation rules
 * @returns {object} - Validation result
 */
export const validateFormData = (formData, validationRules) => {
    const errors = {};
    let isValid = true;
    
    for (const [field, rules] of Object.entries(validationRules)) {
        const value = formData[field];
        
        for (const rule of rules) {
            const result = rule(value);
            if (!result.valid) {
                errors[field] = result.error;
                isValid = false;
                break;
            }
        }
    }
    
    return { isValid, errors };
};

// Export all functions as default object
export default {
    initializeSecurity,
    sanitizeInput,
    validateUsername,
    validateEmail,
    validatePassword,
    validateSubmissionUrl,
    validateTimeFormat,
    secureApiCall,
    getCsrfToken,
    logSecurityEvent,
    checkSessionValidity,
    validateFormData
};
