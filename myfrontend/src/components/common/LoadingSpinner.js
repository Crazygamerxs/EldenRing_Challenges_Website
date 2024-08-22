// src/components/common/LoadingSpinner.js
import React from 'react';
import './common.css'; // Import spinner CSS

const LoadingSpinner = () => (
    <div className="loading-spinner">
        <div className="spinner"></div>
        <p>Loading...</p>
    </div>
);

export default LoadingSpinner;
