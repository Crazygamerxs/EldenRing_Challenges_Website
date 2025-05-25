// src/utils/csrfUtils.js
import Cookies from 'js-cookie';
import axios from 'axios';

/**
 * Utility functions for managing CSRF tokens
 */

// Wait for CSRF token to be available
export const waitForCsrfToken = async (maxWait = 5000) => {
  const startTime = Date.now();
  
  while (Date.now() - startTime < maxWait) {
    const token = Cookies.get('csrftoken');
    if (token) {
      return token;
    }
    // Wait 100ms before checking again
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  
  throw new Error('CSRF token not available after waiting');
};

// Force fetch a new CSRF token
export const fetchCsrfToken = async () => {
  try {
    const response = await axios.get('http://localhost:8888/api/csrf-token/', { 
      withCredentials: true,
      timeout: 10000
    });
    
    // Wait a bit for the cookie to be set
    await new Promise(resolve => setTimeout(resolve, 200));
    
    const token = Cookies.get('csrftoken');
    if (!token) {
      throw new Error('CSRF token not set after fetch');
    }
    
    return token;
  } catch (error) {
    console.error('Error fetching CSRF token:', error);
    throw error;
  }
};

// Get CSRF token with fallback
export const getCsrfToken = async () => {
  // First try to get existing token
  let token = Cookies.get('csrftoken');
  
  if (token) {
    return token;
  }
  
  // If no token exists, fetch a new one
  return await fetchCsrfToken();
};

// Make a CSRF-protected API call
export const makeApiCall = async (url, options = {}) => {
  try {
    const token = await getCsrfToken();
    
    const response = await fetch(url, {
      ...options,
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': token,
        ...options.headers
      }
    });
    
    return response;
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
};

// Retry API call if CSRF token fails
export const makeApiCallWithRetry = async (url, options = {}, maxRetries = 2) => {
  let lastError;
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      const response = await makeApiCall(url, options);
      
      // If we get a 403 CSRF error, try to refresh the token
      if (response.status === 403 && attempt < maxRetries) {
        const errorText = await response.text();
        if (errorText.includes('CSRF')) {
          console.log('CSRF token expired, fetching new token...');
          await fetchCsrfToken();
          continue; // Retry with new token
        }
      }
      
      return response;
    } catch (error) {
      lastError = error;
      if (attempt < maxRetries) {
        console.log(`Attempt ${attempt + 1} failed, retrying...`);
        // Wait before retry
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }
  }
  
  throw lastError;
};