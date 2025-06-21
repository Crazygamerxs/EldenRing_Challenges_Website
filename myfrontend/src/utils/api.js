// src/utils/api.js - Fixed API endpoints
const getBaseUrl = () => {
    if (process.env.NODE_ENV === 'production') {
        return 'https://eldenringchallenge.xyz';
    } else {
        return 'http://localhost:8888';
    }
};

export const API_ENDPOINTS = {
    BASE_URL: getBaseUrl(),
    
    // Auth endpoints
    CSRF_TOKEN: `${getBaseUrl()}/api/csrf-token/`,
    LOGIN: `${getBaseUrl()}/api/login/`,
    SIGNUP: `${getBaseUrl()}/api/signup/`,
    LOGOUT: `${getBaseUrl()}/api/logout/`,
    USER_PROFILE: `${getBaseUrl()}/api/user-profile/`,
    
    // Challenge endpoints
    CHALLENGES: `${getBaseUrl()}/api/challenge/`,
    CHALLENGE_DETAIL: (id) => `${getBaseUrl()}/api/challenge/${id}/`,
    SUBMISSIONS: `${getBaseUrl()}/api/submissions/`,
    SUBMIT_RUN: `${getBaseUrl()}/api/submit_run/`,
    
    // Leaderboard endpoints
    LEADERBOARD_CHALLENGES: `${getBaseUrl()}/api/leaderboard/challenges/`,
    LEADERBOARD_POINTS: `${getBaseUrl()}/api/leaderboard/points/`,
    
    // Admin endpoints
    ADMIN_STATS: `${getBaseUrl()}/api/admin/stats/`,
    ADMIN_SUBMISSIONS: `${getBaseUrl()}/api/admin/submissions/`,
    ADMIN_CHALLENGES: `${getBaseUrl()}/api/admin/challenges/`,
    ADMIN_USERS: `${getBaseUrl()}/api/admin/users/`,
    ADMIN_SETTINGS: `${getBaseUrl()}/api/admin/settings/`,
    
    // Notification endpoints
    NOTIFICATIONS: `${getBaseUrl()}/api/notifications/`,
    UNREAD_COUNT: `${getBaseUrl()}/api/notifications/unread-count/`,
    
    // Health check
    HEALTH: `${getBaseUrl()}/api/health/`,
};

// Axios configuration
import axios from 'axios';

// Set default configuration
axios.defaults.withCredentials = true;
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

// Add a request interceptor to ensure CSRF token is included
axios.interceptors.request.use(
    (config) => {
        // Get CSRF token from cookie
        const csrfToken = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        
        if (csrfToken) {
            config.headers['X-CSRFToken'] = csrfToken;
        }
        
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Add a response interceptor to handle common errors
axios.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        if (error.response?.status === 403) {
            console.warn('CSRF token may have expired');
        } else if (error.response?.status === 401) {
            console.warn('Authentication required');
        }
        
        return Promise.reject(error);
    }
);

export default axios;
