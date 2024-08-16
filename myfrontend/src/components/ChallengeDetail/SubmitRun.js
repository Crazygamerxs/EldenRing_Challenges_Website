import React, { useState, useContext } from 'react';
import './ChallengeDetail.css'; // Ensure you have the required CSS styles
import { UserContext } from '../common/UserContext'; // Adjust the path to where UserProvider is located

const SubmitRun = ({ challengeId, onClose }) => {
  const [fileUrl, setFileUrl] = useState('');
  const { user } = useContext(UserContext); // Access user from context

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!user) {
      alert('You need to be logged in to submit a run.');
      return;
    }

    console.log('Submitting run with data:');
    console.log('File URL:', fileUrl);
    console.log('Challenge ID:', challengeId);
    console.log('User ID:', user.id);
    console.log('Time Taken:', 0);

    try {
      const response = await fetch('http://127.0.0.1:8888/api/submit_run/', {
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
        alert('Run submitted successfully!');
        onClose();
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.error || 'Failed to submit run'}`);
      }
    } catch (error) {
      console.error('Error submitting run:', error);
      alert('An error occurred while submitting the run');
    }
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
      </div>
    </div>
  );
};

export default SubmitRun;
