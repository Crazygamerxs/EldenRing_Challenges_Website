import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios'; // Import axios
import Cookies from 'js-cookie'; // Import js-cookie
import CSRFTOKEN from "../common/CSRFToken"

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);    


    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8888/api/user-profile/', {
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

        fetchUser();
    }, []);

    const login = async (userData) => {
        try {
            setUser(userData);
        } catch (error) {
            console.error('Error during login:', error);
        }
    };

    const logout = async () => {
        try {
            const csrfToken = Cookies.get('csrftoken');  // Retrieve the CSRF token
            console.log('CSRF Token being sent:', csrfToken);  // Debugging
    
            const response = await axios.post('http://127.0.0.1:8888/api/logout/', {}, {
                withCredentials: true,  // Ensure cookies are sent with the request
                headers: {
                    'X-CSRFToken': csrfToken,  // Include CSRF token in headers
                },
            });
    
            if (response.status === 200) {
                // Handle successful logout
                setUser(null);
                Cookies.remove('sessionid');
                Cookies.remove('csrftoken');
            } else {
                console.log('Error during logout');
            }
        } catch (error) {
            console.error('Error during logout:', error);
        }
    };
    
    
    
    
    

    return (
        <UserContext.Provider value={{ user, loading, login, logout }}>
            {children}
        </UserContext.Provider>
    );
};
