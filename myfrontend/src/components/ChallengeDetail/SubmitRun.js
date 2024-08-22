import React, { useState, useContext, useEffect } from 'react';
import './ChallengeDetail.css'; // Ensure you have the required CSS styles
import { UserContext } from '../common/UserContext'; // Adjust the path to where UserProvider is located
import Notification from '../common/Notification'; // Import the Notification component

const SubmitRun = ({ challengeId, onClose }) => {
  const [fileUrl, setFileUrl] = useState('');
  const [notification, setNotification] = useState(null); // State to manage notifications
  const { user } = useContext(UserContext); // Access user from context

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!user) {
      setNotification({ message: 'You need to be logged in to submit a run.', type: 'error' });
      return;
    }

    try {
      const response = await fetch('http://localhost:8888/api/submit_run/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          file_url: fileUrl,
          challenge: challengeId,
          user: user.id, // Include user ID in the request body
          time_taken: 0, // Time Taken is set to 0 by default
        }),
      });

      if (response.ok) {
        setNotification({ message: 'Run submitted successfully!', type: 'success' });
        setFileUrl(''); // Clear the input
        onClose();
      } else {
        const errorData = await response.json();
        setNotification({ message: `Error: ${errorData.error || 'Failed to submit run'}`, type: 'error' });
      }
    } catch (error) {
      console.error('Error submitting run:', error);
      setNotification({ message: 'An error occurred while submitting the run', type: 'error' });
    }
  };

  const handleShowNotification = () => {
    setNotification({
      message: ' Success This is a test notification triggered by the button!',
      type: 'success',
    });
  };

  const handleCloseNotification = () => {
    setNotification(null);
  };

  return (
    <div className="submit-run-overlay">
      <div className="submit-run-modal">
        <button className="submit-run-close-btn" onClick={onClose}>X</button>
        <h2 className="submit-run-title">Submit Your Run</h2>
        <form onSubmit={handleSubmit} className="submit-run-form">
          <div className="submit-run-form-container">
            <label className="submit-run-form-label">
              Enter the URL for your run:
            </label>
            <input
              type="text"
              value={fileUrl}
              onChange={(e) => setFileUrl(e.target.value)}
              placeholder="Enter the link..."
              required
              className="submit-run-input"
            />
          </div>
          <button type="submit" className="submit-run-submit-btn">Submit Run</button>
        </form>
        <button onClick={handleShowNotification} className="test-notification-btn">
          Show Test Notification
        </button>
        {notification && (
          <Notification
            message={notification.message}
            type={notification.type}
            onClose={handleCloseNotification}
          />
        )}
      </div>
    </div>
  );
};

export default SubmitRun;
