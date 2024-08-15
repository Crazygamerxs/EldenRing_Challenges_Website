import React, { useState, useContext } from 'react';
import { UserContext } from '../common/UserContext';
import './ChallengeDetail.css';

const SubmitRun = ({ challengeId, onClose }) => {
  const [fileUrl, setFileUrl] = useState('');
  const { user } = useContext(UserContext);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    console.log('Submitting run with data:');
    console.log('File URL:', fileUrl);
    console.log('Challenge ID:', challengeId);
    console.log('User ID:', user?.id);
    console.log('Time Taken:', 0);

    try {
      const response = await fetch('http://127.0.0.1:8888/api/submit_run/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include', // Ensure this is included
        body: JSON.stringify({
          file_url: fileUrl,
          challenge: challengeId,
          user: user?.id,
          time_taken: 0,
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
        <h2 className="submit-run-title">Tarnished’s Record</h2>
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
