import React, { useState, useEffect, useContext } from 'react';
import './ChallengeDetail.css'; 
import { UserContext } from '../common/UserContext'; 
import Notification from '../common/Notification'; 
import Cookies from 'js-cookie';

import { API_ENDPOINTS } from '../../utils/api';
const MultipleRunSubmit = ({ onClose }) => {
  const [challenges, setChallenges] = useState([]);
  const [selectedChallenges, setSelectedChallenges] = useState([]);
  const [fileUrl, setFileUrl] = useState('');
  const [completionTime, setCompletionTime] = useState('');
  const [notification, setNotification] = useState(null);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { user } = useContext(UserContext);

  useEffect(() => {
    const fetchChallenges = async () => {
      try {
        const csrfToken = Cookies.get('csrftoken');
        const response = await fetch(API_ENDPOINTS.CHALLENGES, {
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
        setNotification({ message: 'Failed to load challenges. Please try again.', type: 'error' });
      }
    };

    fetchChallenges();
  }, []);

  // Ensure CSRF token is available before allowing submit
  const waitForCsrfToken = async (maxWait = 5000) => {
    const startTime = Date.now();
    
    while (Date.now() - startTime < maxWait) {
      const token = Cookies.get('csrftoken');
      if (token) {
        return token;
      }
      // Wait 100ms before checking again
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    
    throw new Error('CSRF token not available');
  };

  const validateTimeFormat = (timeString) => {
    // Check if format is HH:MM:SS
    const timePattern = /^\d{2}:\d{2}:\d{2}$/;
    if (!timePattern.test(timeString)) {
      return false;
    }
    
    // Check if values are valid
    const [hours, minutes, seconds] = timeString.split(':').map(Number);
    return hours >= 0 && minutes >= 0 && minutes < 60 && seconds >= 0 && seconds < 60;
  };

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

    if (selectedChallenges.length === 0) {
      setNotification({ message: 'Please select at least one challenge.', type: 'error' });
      return;
    }

    if (!fileUrl.trim()) {
      setNotification({ message: 'Please enter a valid URL for your run.', type: 'error' });
      return;
    }

    if (!completionTime.trim()) {
      setNotification({ message: 'Please enter your completion time.', type: 'error' });
      return;
    }

    if (!validateTimeFormat(completionTime)) {
      setNotification({ message: 'Please enter time in HH:MM:SS format (e.g., 01:30:45).', type: 'error' });
      return;
    }

    // Validate URL format
    try {
      new URL(fileUrl);
    } catch {
      setNotification({ message: 'Please enter a valid URL.', type: 'error' });
      return;
    }

    setIsSubmitting(true);

    try {
      // Wait for CSRF token to be available
      const csrfToken = await waitForCsrfToken();
      console.log('Using CSRF token for multiple submission:', csrfToken.substring(0, 10) + '...');

      let successCount = 0;
      let errorCount = 0;
      let lastError = null;

      for (const challengeId of selectedChallenges) {
        try {
          const response = await fetch(API_ENDPOINTS.SUBMIT_RUN, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken,
            },
            credentials: 'include',
            body: JSON.stringify({
              file_url: fileUrl.trim(),
              challenge: challengeId,
              user: user.id,
              completion_time: completionTime.trim(),
            }),
          });

          if (response.ok) {
            successCount++;
            console.log(`Successfully submitted run for challenge ${challengeId}`);
          } else {
            errorCount++;
            const errorData = await response.json();
            lastError = errorData.error || `Failed to submit run for challenge ${challengeId}`;
            console.error(`Failed to submit run for challenge ${challengeId}:`, errorData);
          }
        } catch (submitError) {
          errorCount++;
          lastError = submitError.message;
          console.error(`Error submitting run for challenge ${challengeId}:`, submitError);
        }
      }

      // Show results
      if (successCount > 0 && errorCount === 0) {
        setNotification({ 
          message: `All ${successCount} runs submitted successfully! Your submissions will be reviewed by an admin.`, 
          type: 'success' 
        });
        setFileUrl('');
        setCompletionTime('');
        setSelectedChallenges([]);
        setIsDropdownOpen(false);
        
        // Close modal after showing success message
        setTimeout(() => {
          onClose();
        }, 2000);
      } else if (successCount > 0 && errorCount > 0) {
        setNotification({ 
          message: `${successCount} runs submitted successfully, but ${errorCount} failed. Last error: ${lastError}`, 
          type: 'error' 
        });
      } else {
        setNotification({ 
          message: `All submissions failed. Error: ${lastError}`, 
          type: 'error' 
        });
      }
    } catch (error) {
      console.error('Error in submission process:', error);
      setNotification({ 
        message: error.message.includes('CSRF') 
          ? 'Security token not ready. Please wait a moment and try again.' 
          : 'An error occurred while submitting the runs. Please try again.', 
        type: 'error' 
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  // Close modal with escape key
  useEffect(() => {
    const handleEscKey = (event) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    window.addEventListener('keydown', handleEscKey);
    return () => {
      window.removeEventListener('keydown', handleEscKey);
    };
  }, [onClose]);

  const firstChallengeName = selectedChallenges.length > 0 
    ? challenges.find(challenge => selectedChallenges.includes(challenge.id))?.name || 'Select Challenges'
    : 'Select Challenges';

  const displayText = selectedChallenges.length > 1 
    ? `${firstChallengeName} (+${selectedChallenges.length - 1} more)`
    : firstChallengeName;

  const formatTimeExample = () => {
    return 'Format: HH:MM:SS (e.g., 01:30:45 for 1 hour, 30 minutes, 45 seconds)';
  };

  return (
    <div 
      className="multiple-run-overlay"
      onClick={(e) => {
        if (e.target.className === 'multiple-run-overlay') {
          onClose();
        }
      }}
    >
      <div className="multiple-run-modal">
        <button className="multiple-run-close-btn" onClick={onClose}>×</button>
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
                disabled={isSubmitting}
              >
                {displayText}
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
                        disabled={isSubmitting}
                      />
                      <label htmlFor={`challenge-${challenge.id}`} className="multiple-run-dropdown-label">
                        {challenge.name}
                        {challenge.is_combination && (
                          <span className="combo-indicator"> [COMBO]</span>
                        )}
                        {challenge.is_dlc && (
                          <span className="dlc-indicator"> [DLC]</span>
                        )}
                      </label>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Display Selected Challenges */}
            {selectedChallenges.length > 0 && (
              <div className="multiple-run-selected-box">
                <h3>Selected Challenges ({selectedChallenges.length}):</h3>
                <div className="multiple-run-selected-paragraph">
                  {selectedChallenges.map((challengeId) => {
                    const challenge = challenges.find(ch => ch.id === challengeId);
                    return (
                      <span key={challengeId} className="multiple-run-selected-item">
                        {challenge ? challenge.name : 'Unknown Challenge'}
                        {challenge?.is_combination && <span className="combo-tag">COMBO</span>}
                        {challenge?.is_dlc && <span className="dlc-tag">DLC</span>}
                        <button
                          type="button"
                          className='multiple-run-remove-btn'
                          onClick={() => handleRemoveChallenge(challengeId)}
                          disabled={isSubmitting}
                        >
                          &times;
                        </button>
                      </span>
                    );
                  })}
                </div>
              </div>
            )}

            {/* URL Input */}
            <label className="multiple-run-form-label-url">
              Enter the URL for your run:
            </label>
            <input
              type="url"
              value={fileUrl}
              onChange={(e) => setFileUrl(e.target.value)}
              placeholder="https://youtube.com/watch?v=... or https://drive.google.com/..."
              required
              className="multiple-run-input"
              disabled={isSubmitting}
            />

            {/* Completion Time Input */}
            <label className="multiple-run-form-label-time">
              Completion Time:
            </label>
            <input
              type="text"
              value={completionTime}
              onChange={(e) => setCompletionTime(e.target.value)}
              placeholder="01:30:45"
              required
              className="multiple-run-input"
              disabled={isSubmitting}
              pattern="\d{2}:\d{2}:\d{2}"
            />
            <small className="multiple-run-input-help">
              {formatTimeExample()}
            </small>
            {completionTime && !validateTimeFormat(completionTime) && (
              <small className="error-text">
                Invalid time format. Use HH:MM:SS
              </small>
            )}
          </div>

          <button 
            type="submit" 
            className="multiple-run-submit-btn"
            disabled={isSubmitting || selectedChallenges.length === 0 || !completionTime.trim() || !validateTimeFormat(completionTime)}
          >
            {isSubmitting 
              ? `Submitting ${selectedChallenges.length} runs...` 
              : `Submit All Selected Runs (${selectedChallenges.length})`}
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