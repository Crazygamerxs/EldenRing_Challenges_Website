/**
 * Utility functions for API requests and error handling
 */

import Cookies from 'js-cookie';

import { API_ENDPOINTS } from '../utils/api';
/**
 * Default fetch options with CSRF token and credentials
 * @returns {Object} Fetch options with CSRF token and credentials
 */
export const getDefaultFetchOptions = (method = 'GET') => {
  const csrfToken = Cookies.get('csrftoken');
  return {
    method,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
  };
};

/**
 * Handles API errors and returns a standardized error object
 * @param {Error} error - The error object
 * @param {string} fallbackMessage - Fallback message if error doesn't have a message
 * @returns {Object} Standardized error object
 */
export const handleApiError = (error, fallbackMessage = 'An unexpected error occurred') => {
  console.error('API Error:', error);

  // Network error
  if (!navigator.onLine) {
    return {
      message: 'Network error. Please check your internet connection.',
      status: 0,
      type: 'network',
    };
  }

  // Response error with status code
  if (error.response) {
    const status = error.response.status;
    
    // Authentication errors
    if (status === 401) {
      return {
        message: 'Your session has expired. Please log in again.',
        status,
        type: 'auth',
      };
    }
    
    // Permission errors
    if (status === 403) {
      return {
        message: 'You do not have permission to perform this action.',
        status,
        type: 'permission',
      };
    }
    
    // Not found errors
    if (status === 404) {
      return {
        message: 'The requested resource was not found.',
        status,
        type: 'not_found',
      };
    }
    
    // Validation errors
    if (status === 400) {
      let message = 'Invalid request. Please check your input.';
      
      // Try to extract validation error messages
      try {
        const data = error.response.data;
        if (data && typeof data === 'object') {
          const errorMessages = [];
          
          // Extract error messages from response data
          Object.keys(data).forEach(key => {
            const value = data[key];
            if (Array.isArray(value)) {
              errorMessages.push(`${key}: ${value.join(', ')}`);
            } else if (typeof value === 'string') {
              errorMessages.push(`${key}: ${value}`);
            }
          });
          
          if (errorMessages.length > 0) {
            message = errorMessages.join('. ');
          }
        }
      } catch (e) {
        console.error('Error parsing validation errors:', e);
      }
      
      return {
        message,
        status,
        type: 'validation',
        details: error.response.data,
      };
    }
    
    // Server errors
    if (status >= 500) {
      return {
        message: 'Server error. Please try again later.',
        status,
        type: 'server',
      };
    }
    
    // Other status codes
    return {
      message: error.response.data?.message || `Error: ${status}`,
      status,
      type: 'http',
      details: error.response.data,
    };
  }
  
  // Request was made but no response was received
  if (error.request) {
    return {
      message: 'No response from server. Please try again later.',
      type: 'timeout',
    };
  }
  
  // Something else happened in setting up the request
  return {
    message: error.message || fallbackMessage,
    type: 'unknown',
  };
};

/**
 * Makes an API request with error handling
 * @param {string} url - The URL to fetch
 * @param {Object} options - Fetch options
 * @returns {Promise} Promise that resolves to the response data or rejects with an error
 */
export const apiRequest = async (url, options = {}) => {
  try {
    const defaultOptions = getDefaultFetchOptions(options.method || 'GET');
    const fetchOptions = { ...defaultOptions, ...options };
    
    // If body is provided and is an object, stringify it
    if (options.body && typeof options.body === 'object') {
      fetchOptions.body = JSON.stringify(options.body);
    }
    
    const response = await fetch(url, fetchOptions);
    
    // Check if response is ok
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw {
        response: {
          status: response.status,
          data: errorData,
        },
      };
    }
    
    // Parse response as JSON if it has content
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      return await response.json();
    }
    
    return await response.text();
  } catch (error) {
    throw handleApiError(error);
  }
};

/**
 * Makes a GET request with error handling
 * @param {string} url - The URL to fetch
 * @param {Object} options - Additional fetch options
 * @returns {Promise} Promise that resolves to the response data
 */
export const get = (url, options = {}) => {
  return apiRequest(url, { ...options, method: 'GET' });
};

/**
 * Makes a POST request with error handling
 * @param {string} url - The URL to fetch
 * @param {Object} data - The data to send
 * @param {Object} options - Additional fetch options
 * @returns {Promise} Promise that resolves to the response data
 */
export const post = (url, data = {}, options = {}) => {
  return apiRequest(url, { ...options, method: 'POST', body: data });
};

/**
 * Makes a PUT request with error handling
 * @param {string} url - The URL to fetch
 * @param {Object} data - The data to send
 * @param {Object} options - Additional fetch options
 * @returns {Promise} Promise that resolves to the response data
 */
export const put = (url, data = {}, options = {}) => {
  return apiRequest(url, { ...options, method: 'PUT', body: data });
};

/**
 * Makes a DELETE request with error handling
 * @param {string} url - The URL to fetch
 * @param {Object} options - Additional fetch options
 * @returns {Promise} Promise that resolves to the response data
 */
export const del = (url, options = {}) => {
  return apiRequest(url, { ...options, method: 'DELETE' });
};

/**
 * Makes a PATCH request with error handling
 * @param {string} url - The URL to fetch
 * @param {Object} data - The data to send
 * @param {Object} options - Additional fetch options
 * @returns {Promise} Promise that resolves to the response data
 */
export const patch = (url, data = {}, options = {}) => {
  return apiRequest(url, { ...options, method: 'PATCH', body: data });
};

/**
 * Formats API URLs with the base URL
 * @param {string} path - The API path
 * @returns {string} The full API URL
 */
export const formatApiUrl = (path) => {
  // In production, use the domain name
  const baseUrl = process.env.NODE_ENV === 'production' 
    ? 'https://eldenring.biz/api'
    : 'http://localhost:8888/api';
    
  // Remove leading slash if present
  const cleanPath = path.startsWith('/') ? path.substring(1) : path;
  
  return `${baseUrl}/${cleanPath}`;
};
