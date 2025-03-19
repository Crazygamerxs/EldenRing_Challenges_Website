import React, { useState, useEffect, useContext } from 'react';
import './ChallengeDetail.css'; 
import { UserContext } from '../common/UserContext'; 
import Notification from '../common/Notification'; 
import Cookies from 'js-cookie'; // Import Cookies for CSRF token

const MultipleRunSubmit = ({ onClose }) => {
  const [challenges, setChallenges] = useState([]);
  const [selectedChallenges, setSelectedChallenges] = useState([]);
  const [fileUrl, setFileUrl] = useState('');
  const [notification, setNotification] = useState(null); // State to manage notifications
  const [isDropdownOpen, setIsDropdownOpen] = useState(false); // State to manage dropdown visibility
  const { user } = useContext(UserContext); // Access user from context

  useEffect(() => {
    const fetchChallenges = async () => {
      try {
        const csrfToken = Cookies.get('csrftoken');
        const response = await fetch('http://localhost:8888/api/challenge/', {
          method: 'GET',
          credentials: 'include',
          headers: {
            'X-CSRFToken': csrfToken,
          },
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setChallenges(data);
      } catch (error) {
        console.error('Error fetching challenges:', error);
      }
    };

    fetchChallenges();
  }, []);

  const handleChallengeSelect = (challengeId) => {
    setSelectedChallenges((prev) =>
      prev.includes(challengeId)
        ? prev.filter((id) => id !== challengeId)
        : [...prev, challengeId]
    );
  };

  const handleRemoveChallenge = (challengeId) => {
    setSelectedChallenges((prev) => prev.filter((id) => id !== challengeId));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!user) {
      setNotification({ message: 'You need to be logged in to submit a run.', type: 'error' });
      return;
    }

    try {
      for (const challengeId of selectedChallenges) {
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
            status: 'pending', // Status is set to pending by default
          }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          setNotification({ message: `Error: ${errorData.error || 'Failed to submit run for challenge ${challengeId}'}`, type: 'error' });
          return;
        }
      }
      
      setNotification({ message: 'Runs submitted successfully!', type: 'success' });
      setFileUrl(''); // Clear the input
      setSelectedChallenges([]);
      setIsDropdownOpen(false); // Close the dropdown on submit
      onClose();
    } catch (error) {
      console.error('Error submitting run:', error);
      setNotification({ message: 'An error occurred while submitting the runs', type: 'error' });
    }
  };

  const firstChallengeName = challenges.find(challenge => selectedChallenges.includes(challenge.id))?.name || 'Select Challenges';

  return (
    <div className="multiple-run-overlay">
      <div className="multiple-run-modal">
        <button className="multiple-run-close-btn" onClick={onClose}>X</button>
        <h2 className="multiple-run-title">Submit Multiple Runs</h2>
        <form onSubmit={handleSubmit} className="multiple-run-form">
          <div className="multiple-run-form-container">
            {/* Dropdown with Checkboxes */}
            <label className="multiple-run-form-label">Select Challenges:</label>
            <div className="multiple-run-dropdown">
              <button
                type="button"
                className="multiple-run-dropdown-toggle"
                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              >
                {firstChallengeName}
                <span className="multiple-run-dropdown-arrow">&#9662;</span>
              </button>
              {isDropdownOpen && (
                <div className="multiple-run-dropdown-menu">
                  {challenges.map((challenge) => (
                    <div key={challenge.id} className="multiple-run-dropdown-item">
                      <input
                        type="checkbox"
                        id={`challenge-${challenge.id}`}
                        checked={selectedChallenges.includes(challenge.id)}
                        onChange={() => handleChallengeSelect(challenge.id)}
                      />
                      <label htmlFor={`challenge-${challenge.id}`} className="multiple-run-dropdown-label">
                        {challenge.name}
                      </label>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Display Selected Challenges */}
            <div className="multiple-run-selected-box">
              <h3>Selected Challenges:</h3>
              <p className="multiple-run-selected-paragraph">
                {selectedChallenges.map((challengeId) => {
                  const challenge = challenges.find(ch => ch.id === challengeId);
                  return (
                    <span key={challengeId} className="multiple-run-selected-item">
                      {challenge ? (
                        <>
                          {challenge.name}
                          <button
                            type="button"
                            className='multiple-run-remove-btn'
                            onClick={() => handleRemoveChallenge(challengeId)}
                          >
                            &times;
                          </button>
                        </>
                      ) : 'Unknown Challenge'}
                    </span>
                  );
                })}
              </p>
            </div>

            {/* URL Input */}
            <label className="multiple-run-form-label-url">
              Enter the URL for your run:
            </label>
            <input
              type="text"
              value={fileUrl}
              onChange={(e) => setFileUrl(e.target.value)}
              placeholder="Enter the link..."
              required
              className="multiple-run-input"
            />
          </div>
          <button type="submit" className="multiple-run-submit-btn">
            Submit All Selected Runs
          </button>
        </form>

        {notification && (
          <Notification
            message={notification.message}
            type={notification.type}
            onClose={() => setNotification(null)}
          />
        )}
      </div>
    </div>
  );
};

export default MultipleRunSubmit;
