import React, { useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';

const CSRFToken = () => {
    useEffect(() => {
        const fetchCsrfToken = async () => {
            try {
                const response = await axios.get('http://localhost:8888/api/csrf-token/', { withCredentials: true });
                // Cookies.set('csrftoken', response.data.csrfToken, { path: '', domain: 'localhost' });
                console.log('Fetching CSRF token');
                console.log('CSRF Token:', response);
            } catch (error) {
                console.error('Error fetching CSRF token:', error);
            }
        };
        fetchCsrfToken();
    }, []);

    return null; // No need to render anything
};

export default CSRFToken;
