import React, { useEffect, useState } from 'react';
import './common.css'; // Ensure this file is correctly imported

import { API_ENDPOINTS } from '../../utils/api';
const LoadingIndicator = ({ isVisible }) => {
  const [show, setShow] = useState(false); // Track if indicator should be shown

  useEffect(() => {
    if (isVisible) {
      setShow(true); // Show the indicator
    } else {
      setTimeout(() => {
        setShow(false); // Hide the indicator after it completes the fade-out
      }, 500); // Match this duration with the animation duration
    }
  }, [isVisible]);

  return (
    <div className={`loading-indicator ${show ? 'visible' : ''}`}></div>
  );
};

export default LoadingIndicator;
