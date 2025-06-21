import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios'; // Import axios
import Cookies from 'js-cookie'; // Import js-cookie

import { API_ENDPOINTS } from '../../utils/api';
export const UserContext = createContext();

export const UserProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);    


    useEffect(() => {
        // Don't automatically fetch user profile on app startup
        // This was causing 401 Unauthorized errors in production
        // User profile will be fetched after successful login
        setLoading(false);
    }, []);

    const fetchUserProfile = async () => {
        try {
            setLoading(true);
            const response = await axios.get(API_ENDPOINTS.USER_PROFILE, {
                withCredentials: true, // Ensure cookies are sent
            });
            if (response.status === 200) {
                setUser(response.data);
            } else {
                setUser(null);
            }
        } catch (error) {
            console.error('Error fetching user profile:', error);
            setUser(null);
        } finally {
            setLoading(false);
        }
    };

    const login = async (userData) => {
        try {
            setUser(userData);
        } catch (error) {
            console.error('Error during login:', error);
        }
    };

    const logout = async () => {
        try {
            // Retrieve the CSRF token from cookies
            const csrfToken = Cookies.get('csrftoken');
            console.log('CSRF Token being sent:', csrfToken);  // Debugging
    
            // Send POST request to logout endpoint
            const response = await axios.post(API_ENDPOINTS.LOGOUT, {}, {
                withCredentials: true,  // Ensure cookies are sent with the request
                headers: {
                    'X-CSRFToken': csrfToken,  // Include CSRF token in headers
                },
            });
    
            // Handle response
            if (response.status === 200) {
                console.log('Logout successful');  // Debugging
                setUser(null);  // Update user context or state
    
                // Remove cookies
                Cookies.remove('sessionid');  // Clear session cookie
                Cookies.remove('csrftoken');  // Clear CSRF token cookie
            } else {
                console.error('Error during logout, status:', response.status);  // Debugging
            }
        } catch (error) {
            console.error('Error during logout:', error);  // Debugging
        }
    };
    
    
    
    
    
    

    return (
        <UserContext.Provider value={{ user, loading, login, logout, fetchUserProfile }}>
            {children}
        </UserContext.Provider>
    );
};
