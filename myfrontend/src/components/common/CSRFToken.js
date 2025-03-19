import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';

const CSRFToken = () => {
    const [csrfError, setCsrfError] = useState(null);

    useEffect(() => {
        const fetchCsrfToken = async () => {
            try {
                const response = await axios.get('http://localhost:8888/api/csrf-token/', { withCredentials: true });
                
                // The Django server should set the CSRF cookie automatically
                // This is just a verification step
                const csrfToken = Cookies.get('csrftoken');
                
                if (!csrfToken) {
                    console.warn('CSRF token not found in cookies after fetch');
                    setCsrfError('CSRF token not found');
                } else {
                    console.log('CSRF token successfully retrieved');
                    setCsrfError(null);
                }
            } catch (error) {
                console.error('Error fetching CSRF token:', error);
                setCsrfError('Failed to fetch CSRF token');
            }
        };
        
        fetchCsrfToken();
        
        // Set up interval to refresh CSRF token periodically (every 30 minutes)
        const intervalId = setInterval(fetchCsrfToken, 30 * 60 * 1000);
        
        // Clean up interval on component unmount
        return () => clearInterval(intervalId);
    }, []);

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
        </div>
    ) : null;
};

export default CSRFToken;
