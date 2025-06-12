import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { UserContext } from './UserContext'; // Adjust the import path as needed

import { API_ENDPOINTS } from '../../utils/api';
const PrivateRoute = ({ element: Component, ...rest }) => {
    const { user, loading } = useContext(UserContext);

    // If the user is still loading, you might want to show a loading spinner or similar
    if (loading) {
        return <div>Loading...</div>;
    }

    return user ? Component : <Navigate to="/login" />;
};

export default PrivateRoute;
