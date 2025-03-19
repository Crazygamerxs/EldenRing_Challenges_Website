// src/components/common/LoadingSpinner.js
import React from 'react';
import './common.css'; // Import spinner CSS

const LoadingSpinner = ({ size = 'medium', color = '#a98b2d', text = 'Loading...' }) => {
    // Size classes
    const sizeClasses = {
        small: { spinner: '30px', text: '14px' },
        medium: { spinner: '50px', text: '16px' },
        large: { spinner: '70px', text: '18px' }
    };
    
    const selectedSize = sizeClasses[size] || sizeClasses.medium;
    
    return (
        <div className="loading-spinner">
            <div 
                className="spinner" 
                style={{ 
                    width: selectedSize.spinner, 
                    height: selectedSize.spinner,
                    borderColor: `rgba(255, 255, 255, 0.2)`,
                    borderTopColor: color
                }}
            ></div>
            {text && <p style={{ fontSize: selectedSize.text, color: '#f0f0f0', marginTop: '15px' }}>{text}</p>}
        </div>
    );
};

export default LoadingSpinner;
