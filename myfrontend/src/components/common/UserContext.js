import React, { createContext, useState, useEffect } from 'react';

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8888/api/user-profile/', {
                    method: 'GET',
                    credentials: 'include',
                });
                if (response.ok) {
                    const data = await response.json();
                    // Log each data point separately
                    // console.log('User Data Fetched:');
                    // console.log('User ID:', data.id);
                    // console.log('Username:', data.username);
                    // console.log('Email:', data.email);
                    // console.log('Profile Image:', data.profile_image);
                    // console.log('Completed Challenges:', data.completed_challenges);
                    // console.log('Badges:', data.badges);
                    setUser(data);
                } else {
                    console.log('Failed to fetch user data:', response.status);
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
            // console.log('User logged in:');
            // console.log('User ID:', userData.id);
            // console.log('Username:', userData.username);
            // console.log('Email:', userData.email);
            // console.log('Profile Image:', userData.profile_image);
            // console.log('Completed Challenges:', userData.completed_challenges);
            // console.log('Badges:', userData.badges);
            setUser(userData);
        } catch (error) {
            console.error('Error during login:', error);
        }
    };

    const logout = async () => {
        try {
            console.log('User logged out');
            setUser(null);
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
