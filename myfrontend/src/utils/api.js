// API configuration utility
// Handles different API URLs for development and production

const getApiUrl = () => {
    // In production (when served from Django), use relative URLs
    // In development, use the development server URL
    if (process.env.NODE_ENV === 'production') {
        return ''; // Use relative URLs in production
    } else {
        return 'http://localhost:8888'; // Development server
    }
};

export const API_BASE_URL = getApiUrl();

// Helper function to build full API URLs
export const buildApiUrl = (endpoint) => {
    // Remove leading slash if present to avoid double slashes
    const cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint;
    
    if (API_BASE_URL) {
        return `${API_BASE_URL}/${cleanEndpoint}`;
    } else {
        return `/${cleanEndpoint}`;
    }
};

// Common API endpoints
export const API_ENDPOINTS = {
    // Authentication
    CSRF_TOKEN: buildApiUrl('api/csrf-token/'),
    LOGIN: buildApiUrl('api/login/'),
    LOGOUT: buildApiUrl('api/logout/'),
    SIGNUP: buildApiUrl('api/signup/'),
    PASSWORD_RESET: buildApiUrl('api/password-reset/'),
    PASSWORD_RESET_CONFIRM: (uidb64, token) => buildApiUrl(`api/password-reset-confirm/${uidb64}/${token}/`),
    USER_PROFILE: buildApiUrl('api/user-profile/'),
    
    // Challenges
    CHALLENGES: buildApiUrl('api/challenge/'),
    CHALLENGE_DETAIL: (id) => buildApiUrl(`api/challenge/${id}/`),
    SUBMIT_RUN: buildApiUrl('api/submit_run/'),
    SUBMISSIONS: buildApiUrl('api/submissions/'),
    
    // Leaderboard
    LEADERBOARD_CHALLENGES: buildApiUrl('api/leaderboard/challenges/'),
    LEADERBOARD_POINTS: buildApiUrl('api/leaderboard/points/'),
    LEADERBOARD_STATS: buildApiUrl('api/leaderboard/stats/'),
    USER_LEADERBOARD_STATS: (userId) => buildApiUrl(`api/leaderboard/user/${userId}/`),
    
    // Notifications
    NOTIFICATIONS: buildApiUrl('api/notifications/'),
    NOTIFICATIONS_UNREAD_COUNT: buildApiUrl('api/notifications/unread-count/'),
    MARK_NOTIFICATION_READ: (id) => buildApiUrl(`api/notifications/${id}/read/`),
    MARK_ALL_NOTIFICATIONS_READ: buildApiUrl('api/notifications/mark-all-read/'),
    
    // Admin
    ADMIN_STATS: buildApiUrl('api/admin/stats/'),
    ADMIN_SUBMISSIONS: buildApiUrl('api/admin/submissions/'),
    ADMIN_RECENT_SUBMISSIONS: buildApiUrl('api/admin/submissions/recent/'),
    ADMIN_APPROVE_SUBMISSION: (id) => buildApiUrl(`api/admin/submissions/${id}/approve/`),
    ADMIN_REJECT_SUBMISSION: (id) => buildApiUrl(`api/admin/submissions/${id}/reject/`),
    ADMIN_CHALLENGES: buildApiUrl('api/admin/challenges/'),
    ADMIN_CHALLENGE_DETAIL: (id) => buildApiUrl(`api/admin/challenges/${id}/`),
    ADMIN_CATEGORIES: buildApiUrl('api/categories/'),
    ADMIN_USERS: buildApiUrl('api/admin/users/'),
    ADMIN_USER_DETAIL: (id) => buildApiUrl(`api/admin/users/${id}/`),
    ADMIN_USER_STATUS: (id) => buildApiUrl(`api/admin/users/${id}/status/`),
    ADMIN_SETTINGS: buildApiUrl('api/admin/settings/'),
    
    // Community
    THREADS: buildApiUrl('api/threads/'),
    THREAD_DETAIL: (id) => buildApiUrl(`api/threads/${id}/`),
    THREADS_BY_CATEGORY: (categoryId) => buildApiUrl(`api/threads/?category_id=${categoryId}`),
    
    // Health check
    HEALTH: buildApiUrl('api/health/'),
};

export default {
    API_BASE_URL,
    buildApiUrl,
    API_ENDPOINTS
};
