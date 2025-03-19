import React, { useState, useContext, useEffect } from 'react';
import './ChallengeDetail.css';
import { UserContext } from '../common/UserContext';
import Notification from '../common/Notification';
import images from '../../images';
import Cookies from 'js-cookie';
// Removed framer-motion and confetti for better performance

const SubmitRun = ({ challengeId, onClose, onOpenMultiSubmit }) => {
  const [fileUrl, setFileUrl] = useState('');
  const [notification, setNotification] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showInstructions, setShowInstructions] = useState(false);
  const { user } = useContext(UserContext);

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!user) {
      setNotification({ message: 'You need to be logged in to submit a run.', type: 'error' });
      return;
    }

    if (!fileUrl.trim()) {
      setNotification({ message: 'Please enter a valid URL for your run.', type: 'error' });
      return;
    }

    setIsSubmitting(true);

    try {
      // Get CSRF token from cookie
      const csrfToken = Cookies.get('csrftoken');
      
      const response = await fetch('http://localhost:8888/api/submit_run/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        credentials: 'include',
        body: JSON.stringify({
          file_url: fileUrl,
          challenge: challengeId,
          user: user.id,
          time_taken: 0,
        }),
      });

      if (response.ok) {
        setNotification({ 
          message: 'Run submitted successfully! Your submission will be reviewed by an admin.', 
          type: 'success' 
        });
        setFileUrl('');
        
        // Close modal after a short delay to show success message
        setTimeout(() => {
          onClose();
        }, 2000);
      } else {
        const errorData = await response.json();
        setNotification({ 
          message: `Error: ${errorData.error || 'Failed to submit run'}`, 
          type: 'error' 
        });
      }
    } catch (error) {
      console.error('Error submitting run:', error);
      setNotification({ 
        message: 'An error occurred while submitting the run. Please try again.', 
        type: 'error' 
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const toggleInstructions = () => {
    setShowInstructions(!showInstructions);
  };

  const renderInstructions = () => (
    <div key="instructions" className="submit-run-form-container">
      <h3 style={{ color: '#a98b2d', marginTop: 0, marginBottom: '15px' }}>Submission Guidelines</h3>
      <div style={{ marginBottom: '25px', lineHeight: '1.6' }}>
        <div style={{ marginBottom: '15px', padding: '12px 15px', backgroundColor: 'rgba(169, 139, 45, 0.1)', borderRadius: '8px', borderLeft: '3px solid #a98b2d' }}>
          <h4 style={{ margin: '0 0 8px 0', color: '#a98b2d' }}>Video Requirements</h4>
          <ul style={{ paddingLeft: '20px', margin: '0' }}>
            <li>Upload your run to YouTube, Twitch, or any video hosting platform</li>
            <li>Video must be public or unlisted (not private)</li>
            <li>Minimum resolution of 720p is recommended</li>
            <li>Ensure the entire challenge completion is visible</li>
          </ul>
        </div>
        
        <div style={{ marginBottom: '15px', padding: '12px 15px', backgroundColor: 'rgba(76, 175, 80, 0.1)', borderRadius: '8px', borderLeft: '3px solid #4caf50' }}>
          <h4 style={{ margin: '0 0 8px 0', color: '#4caf50' }}>Gameplay Verification</h4>
          <ul style={{ paddingLeft: '20px', margin: '0' }}>
            <li>Your in-game username must be clearly visible</li>
            <li>Game UI elements showing challenge progress must be visible</li>
            <li>No editing that obscures challenge completion verification</li>
            <li>Timestamp of completion should be visible if possible</li>
          </ul>
        </div>
        
        <div style={{ padding: '12px 15px', backgroundColor: 'rgba(33, 150, 243, 0.1)', borderRadius: '8px', borderLeft: '3px solid #2196f3' }}>
          <h4 style={{ margin: '0 0 8px 0', color: '#2196f3' }}>Review Process</h4>
          <ul style={{ paddingLeft: '20px', margin: '0' }}>
            <li>All submissions are reviewed by admins before appearing on the leaderboard</li>
            <li>You'll receive a notification when your submission is approved or rejected</li>
            <li>Review typically takes 1-2 days</li>
            <li>If rejected, you'll receive feedback on why and can resubmit</li>
          </ul>
        </div>
      </div>
      <div style={{ display: 'flex', justifyContent: 'center', marginTop: '10px' }}>
        <button 
          onClick={toggleInstructions}
          style={{
            background: 'rgba(169, 139, 45, 0.1)',
            border: '1px solid #a98b2d',
            color: '#a98b2d',
            cursor: 'pointer',
            padding: '10px 20px',
            borderRadius: '6px',
            fontSize: '16px',
            fontWeight: '500',
            transition: 'all 0.3s ease',
            display: 'flex',
            alignItems: 'center'
          }}
        >
          <i className="fas fa-arrow-left" style={{ marginRight: '8px' }}></i>
          Back to submission form
        </button>
      </div>
    </div>
  );

  const renderSubmitForm = () => (
    <form 
      key="form"
      onSubmit={handleSubmit} 
      className="submit-run-form"
    >
      <div className="submit-run-form-container">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
          <label style={{ fontSize: '18px', color: '#f0f0f0', fontWeight: '500' }}>
            Enter the URL for your run:
          </label>
          <button 
            type="button" 
            onClick={toggleInstructions}
            style={{
              background: 'rgba(169, 139, 45, 0.1)',
              border: '1px solid #a98b2d',
              color: '#a98b2d',
              cursor: 'pointer',
              padding: '8px 12px',
              borderRadius: '6px',
              fontSize: '14px',
              fontWeight: '500',
              transition: 'all 0.3s ease',
              display: 'flex',
              alignItems: 'center'
            }}
          >
            <i className="fas fa-info-circle" style={{ marginRight: '8px' }}></i>
            View submission guidelines
          </button>
        </div>
        <input
          type="text"
          value={fileUrl}
          onChange={(e) => setFileUrl(e.target.value)}
          placeholder="Paste your video URL here (YouTube, Twitch, or other video platforms)"
          required
          className="submit-run-input"
          disabled={isSubmitting}
          autoFocus
        />
      </div>
      <div className="submit-run-btn-container">
        <button 
          type="submit" 
          className="submit-run-submit-btn"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Submitting...' : 'Submit Run'}
          {!isSubmitting && (
            <img 
              src={images.success_icon} 
              alt="submit" 
              style={{ width: '20px', height: '20px', marginLeft: '8px' }}
            />
          )}
        </button>
        <button
          type="button"
          className="multi-submit-btn"
          onClick={() => {
            onClose();
            onOpenMultiSubmit();
          }}
          disabled={isSubmitting}
        >
          Submit Multiple Runs
        </button>
      </div>
    </form>
  );

  return (
    <div 
      className="submit-run-overlay" 
      onClick={(e) => {
        // Close when clicking outside the modal
        if (e.target.className === 'submit-run-overlay') {
          onClose();
        }
      }}
    >
      <div className="submit-run-modal">
        <button 
          className="submit-run-close-btn" 
          onClick={onClose}
        >
          ×
        </button>
        <h2 className="submit-run-title">
          Submit Your Run
        </h2>
        
        {showInstructions ? renderInstructions() : renderSubmitForm()}

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
