import React, { useEffect, useState } from 'react';
import './common.css'; // Import your CSS file
import images from '../../images'; // Import your images

import { API_ENDPOINTS } from '../../utils/api';
const Notification = ({ message, type, onClose }) => {
  const [progress, setProgress] = useState(100);

  useEffect(() => {
    // Start the progress bar animation
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev <= 0) {
          clearInterval(interval);
          onClose(); // Close the notification when progress reaches 0
          return 0;
        }
        return prev - 0.5; // Adjust the decrement value as needed
      });
    }, 20); // Adjust the interval timing as needed

    return () => clearInterval(interval); // Cleanup on unmount
  }, [onClose]);

  return (
    <div className={`notification ${type}`}>
      <div className="notification-content">
        <div className="notification-header">
          <img src={type === 'success' ? images.success_icon : '/path/to/error-icon.png'} alt="icon" className="notification-icon" />
          <span className="notification-title">{type === 'success' ? 'Success' : 'Error'}</span>
        </div>
        <div className="notification-message">
          {message}
        </div>
      </div>
      <button className="notification-close-btn" onClick={onClose}>X</button>
      <div className="notification-progress-bar" style={{ width: `${progress}%` }} />
    </div>
  );
};

export default Notification;
