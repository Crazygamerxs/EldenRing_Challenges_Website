import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { UserContext } from './UserContext';
import LoadingSpinner from './LoadingSpinner';

/**
 * AdminRoute component for protecting admin-only routes
 * Checks if the user is logged in and is an admin
 * Redirects to login page if not authenticated
 * Redirects to home page if authenticated but not an admin
 */
const AdminRoute = ({ element }) => {
    const { user, loading } = useContext(UserContext);

    // Show loading spinner while checking authentication
    if (loading) {
        return (
            <div style={{ 
                display: 'flex', 
                justifyContent: 'center', 
                alignItems: 'center', 
                height: '100vh',
                backgroundColor: '#111618'
            }}>
                <LoadingSpinner />
            </div>
        );
    }

    // If user is not logged in, redirect to login page
    if (!user) {
        return <Navigate to="/login" replace />;
    }

    // If user is logged in but not an admin, redirect to home page
    if (!user.is_superuser && !user.is_staff) {
        return <Navigate to="/home" replace />;
    }

    // If user is an admin, render the protected component
    return element;
};

export default AdminRoute;
