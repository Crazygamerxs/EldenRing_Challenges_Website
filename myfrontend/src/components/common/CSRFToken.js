import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';

const CSRFToken = () => {
    const [csrfError, setCsrfError] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    const fetchCsrfToken = async () => {
        try {
            // Use relative URL for production
            const apiUrl = process.env.NODE_ENV === 'production' 
                ? '/api/csrf-token/' 
                : 'http://localhost:8888/api/csrf-token/';
                
            const response = await axios.get(apiUrl, { 
                withCredentials: true,
                timeout: 10000
            });
            
            // Wait a bit for the cookie to be set by the browser
            setTimeout(() => {
                const csrfToken = Cookies.get('csrftoken');
                
                if (!csrfToken) {
                    console.warn('CSRF token not found in cookies after fetch');
                    setCsrfError('CSRF token not found');
                } else {
                    console.log('CSRF token successfully retrieved:', csrfToken.substring(0, 10) + '...');
                    setCsrfError(null);
                }
                setIsLoading(false);
            }, 100);
            
        } catch (error) {
            console.error('Error fetching CSRF token:', error);
            setCsrfError('Failed to fetch CSRF token');
            setIsLoading(false);
        }
    };

    useEffect(() => {
        // Check if token already exists
        const existingToken = Cookies.get('csrftoken');
        if (existingToken) {
            console.log('CSRF token already exists');
            setIsLoading(false);
            setCsrfError(null);
            return;
        }

        fetchCsrfToken();
        
        // Set up interval to refresh CSRF token periodically (every 30 minutes)
        const intervalId = setInterval(fetchCsrfToken, 30 * 60 * 1000);
        
        // Clean up interval on component unmount
        return () => clearInterval(intervalId);
    }, []);

    // Listen for page visibility changes to refresh token when user comes back
    useEffect(() => {
        const handleVisibilityChange = () => {
            if (!document.hidden) {
                const token = Cookies.get('csrftoken');
                if (!token) {
                    fetchCsrfToken();
                }
            }
        };

        document.addEventListener('visibilitychange', handleVisibilityChange);
        return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
    }, []);

    // Show loading indicator while fetching initial token
    if (isLoading) {
        return (
            <div style={{ 
                position: 'fixed', 
                top: 0, 
                left: 0, 
                right: 0, 
                background: 'linear-gradient(90deg, #a98b2d 0%, #ce9e10 100%)', 
                color: 'white', 
                padding: '5px', 
                textAlign: 'center',
                zIndex: 9999,
                fontSize: '12px'
            }}>
                Initializing security...
            </div>
        );
    }

    // Only render error message if there's an issue with CSRF
    return csrfError ? (
        <div style={{ 
            position: 'fixed', 
            bottom: 0, 
            left: 0, 
            right: 0, 
            background: '#f44336', 
            color: 'white', 
            padding: '10px', 
            textAlign: 'center',
            zIndex: 9999
        }}>
            Security Error: {csrfError}. Please refresh the page.
            <button 
                onClick={() => window.location.reload()} 
                style={{
                    marginLeft: '10px',
                    background: 'white',
                    color: '#f44336',
                    border: 'none',
                    padding: '5px 10px',
                    borderRadius: '3px',
                    cursor: 'pointer'
                }}
            >
                Refresh
            </button>
        </div>
    ) : null;
};

export default CSRFToken;