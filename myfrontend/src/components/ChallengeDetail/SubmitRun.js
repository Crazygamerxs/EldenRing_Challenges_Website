import React, { useState, useContext, useEffect } from 'react';
import './ChallengeDetail.css';
import { UserContext } from '../common/UserContext';
import Notification from '../common/Notification';
import Cookies from 'js-cookie';

const SubmitRun = ({ challengeId, onClose, onOpenMultiSubmit }) => {
  const [challenge, setChallenge] = useState(null);
  const [fileUrl, setFileUrl] = useState('');
  const [completionTime, setCompletionTime] = useState('');
  const [notification, setNotification] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showInstructions, setShowInstructions] = useState(false);
  const { user } = useContext(UserContext);

  // Fetch challenge details when component mounts
  useEffect(() => {
    const fetchChallenge = async () => {
      if (!challengeId) return;
      
      try {
        const csrfToken = Cookies.get('csrftoken');
        const response = await fetch(`http://localhost:8888/api/challenge/${challengeId}`, {
          method: 'GET',
          credentials: 'include',
          headers: {
            'X-CSRFToken': csrfToken,
          },
        });
        
        if (!response.ok) {
          throw new Error('Failed to fetch challenge details');
        }
        
        const data = await response.json();
        setChallenge(data);
      } catch (error) {
        console.error('Error fetching challenge:', error);
        setNotification({ message: 'Failed to load challenge details.', type: 'error' });
      }
    };

    fetchChallenge();
  }, [challengeId]);

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

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!user) {
      setNotification({ message: 'You need to be logged in to submit a run.', type: 'error' });
      return;
    }

    if (!challenge) {
      setNotification({ message: 'Challenge details not loaded. Please try again.', type: 'error' });
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
      console.log('Using CSRF token for submission:', csrfToken.substring(0, 10) + '...');

      const response = await fetch('http://localhost:8888/api/submit_run/', {
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
        const result = await response.json();
        console.log('Run submitted successfully:', result);
        
        setNotification({ 
          message: result.message || 'Run submitted successfully! Your submission will be reviewed by an admin.', 
          type: 'success' 
        });
        
        setFileUrl('');
        setCompletionTime('');
        
        // Close modal after showing success message
        setTimeout(() => {
          onClose();
        }, 2000);
      } else {
        const errorData = await response.json();
        console.error('Submission failed:', errorData);
        setNotification({ 
          message: errorData.error || 'Failed to submit run. Please try again.', 
          type: 'error' 
        });
      }
    } catch (error) {
      console.error('Error submitting run:', error);
      setNotification({ 
        message: error.message.includes('CSRF') 
          ? 'Security token not ready. Please wait a moment and try again.' 
          : 'An error occurred while submitting the run. Please try again.', 
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

  const formatTimeExample = () => {
    return 'Format: HH:MM:SS (e.g., 01:30:45 for 1 hour, 30 minutes, 45 seconds)';
  };

  // Show loading if challenge is not loaded yet
  if (!challenge) {
    return (
      <div 
        className="submit-run-overlay"
        onClick={(e) => {
          if (e.target.className === 'submit-run-overlay') {
            onClose();
          }
        }}
      >
        <div className="submit-run-modal">
          <button className="submit-run-close-btn" onClick={onClose}>×</button>
          <h2 className="submit-run-title">Loading...</h2>
          <div style={{ textAlign: 'center', padding: '20px' }}>
            <p>Loading challenge details...</p>
          </div>
        </div>
      </div>
    );
  }

  if (showInstructions) {
    return (
      <div 
        className="submit-run-overlay"
        onClick={(e) => {
          if (e.target.className === 'submit-run-overlay') {
            onClose();
          }
        }}
      >
        <div className="submit-run-modal">
          <button className="submit-run-close-btn" onClick={onClose}>×</button>
          <h2 className="submit-run-title">Submission Instructions</h2>
          <div className="submit-run-form-container">
            <h3>How to Submit Your Run</h3>
            <ol style={{ color: '#f0f0f0', lineHeight: '1.6' }}>
              <li><strong>Record Your Run:</strong> Capture your entire challenge run from start to finish using screen recording software or streaming platforms.</li>
              <li><strong>Upload to Platform:</strong> Upload your recording to YouTube, Twitch, Google Drive, or another accessible platform.</li>
              <li><strong>Get Share Link:</strong> Copy the direct link to your uploaded video.</li>
              <li><strong>Track Your Time:</strong> Note your exact completion time in HH:MM:SS format.</li>
              <li><strong>Submit Here:</strong> Use the form to submit your link and completion time.</li>
            </ol>
            
            <h3>Requirements</h3>
            <ul style={{ color: '#f0f0f0', lineHeight: '1.6' }}>
              <li>Video must show the complete run without cuts or edits</li>
              <li>Challenge rules must be followed exactly as described</li>
              <li>Video quality should be clear enough to verify the run</li>
              <li>Include audio if possible to verify no cheats/exploits were used</li>
            </ul>

            <h3>Supported Platforms</h3>
            <ul style={{ color: '#f0f0f0', lineHeight: '1.6' }}>
              <li>YouTube (youtube.com)</li>
              <li>Twitch (twitch.tv)</li>
              <li>Google Drive (drive.google.com)</li>
              <li>Other direct video links</li>
            </ul>
          </div>
          <div className="submit-run-btn-container">
            <button 
              className="instructions-back-btn"
              onClick={() => setShowInstructions(false)}
            >
              Back to Submission
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div 
      className="submit-run-overlay"
      onClick={(e) => {
        if (e.target.className === 'submit-run-overlay') {
          onClose();
        }
      }}
    >
      <div className="submit-run-modal">
        <button className="submit-run-close-btn" onClick={onClose}>×</button>
        <h2 className="submit-run-title">Submit Run for "{challenge.name}"</h2>
        <form onSubmit={handleSubmit} className="submit-run-form">
          <div className="submit-run-form-container">
            <label>
              Enter the URL for your run:
              <button 
                type="button" 
                className="instructions-btn"
                onClick={() => setShowInstructions(true)}
                style={{ marginLeft: '10px' }}
              >
                📋 Instructions
              </button>
            </label>
            <input
              type="url"
              value={fileUrl}
              onChange={(e) => setFileUrl(e.target.value)}
              placeholder="https://youtube.com/watch?v=... or https://drive.google.com/..."
              required
              className="submit-run-input"
              disabled={isSubmitting}
            />
            
            <label style={{ marginTop: '20px' }}>
              Completion Time:
            </label>
            <input
              type="text"
              value={completionTime}
              onChange={(e) => setCompletionTime(e.target.value)}
              placeholder="01:30:45"
              required
              className="submit-run-input"
              disabled={isSubmitting}
              pattern="\d{2}:\d{2}:\d{2}"
            />
            <small style={{ color: '#909090', fontSize: '14px', marginTop: '5px', display: 'block' }}>
              {formatTimeExample()}
            </small>
            {completionTime && !validateTimeFormat(completionTime) && (
              <small style={{ color: '#f44336', fontSize: '14px', marginTop: '5px', display: 'block' }}>
                Invalid time format. Use HH:MM:SS
              </small>
            )}
          </div>

          <div className="submit-run-btn-container">
            <button 
              type="submit" 
              className="submit-run-submit-btn"
              disabled={isSubmitting || !completionTime.trim() || !validateTimeFormat(completionTime)}
            >
              {isSubmitting ? 'Submitting...' : 'Submit Run'}
            </button>
            <button 
              type="button"
              className="multi-submit-btn"
              onClick={onOpenMultiSubmit}
              disabled={isSubmitting}
            >
              Submit Multiple Runs
            </button>
          </div>
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

export default SubmitRun;