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
    ADMIN_CATEGORIES: `${getBaseUrl()}/api/admin/categories/`,
    ADMIN_RECENT_SUBMISSIONS: `${getBaseUrl()}/api/admin/recent-submissions/`,
    ADMIN_CHALLENGE_DETAIL: (id) => `${getBaseUrl()}/api/admin/challenges/${id}/`,
    ADMIN_USER_DETAIL: (id) => `${getBaseUrl()}/api/admin/users/${id}/`,
    ADMIN_APPROVE_SUBMISSION: (id) => `${getBaseUrl()}/api/admin/submissions/${id}/approve/`,
    ADMIN_REJECT_SUBMISSION: (id) => `${getBaseUrl()}/api/admin/submissions/${id}/reject/`,
    
    // Notification endpoints
    NOTIFICATIONS: `${getBaseUrl()}/api/notifications/`,
    UNREAD_COUNT: `${getBaseUrl()}/api/notifications/unread-count/`,
    
    // Health check
    HEALTH: `${getBaseUrl()}/api/health/`,
};

// Axios configuration
import axios from 'axios';

// Set default configuration for session-based auth
axios.defaults.withCredentials = true;

// Add a response interceptor to handle common errors
axios.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        if (error.response?.status === 401) {
            console.warn('Authentication required');
        } else if (error.response?.status === 403) {
            console.warn('Access forbidden');
        }
        
        return Promise.reject(error);
    }
);

export default axios;
