import React, { useState } from 'react';
import './ChallengeDetail'; // Import the CSS file

const SubmitRun = ({ onClose }) => {
  const [time, setTime] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission here

    // Close the modal after submission
    onClose();
  };

  return (
    <div className="submit-run-overlay">
      <div className="submit-run-modal">
        <button className="submit-run-close-btn" onClick={onClose}>X</button>
        <h2 className="submit-run-title">Tarnished’s Record</h2>
        <div className="submit-run-form-container">
          <label className="submit-run-form-label">
            Enter the URL for your run:
          </label>
          <input
            type="text"
            value={time}
            onChange={(e) => setTime(e.target.value)}
            placeholder="Enter the link..."
            required
            className="submit-run-input"
          />
        </div>
          <button type="submit" onClick={handleSubmit} className="submit-run-submit-btn">Submit Run</button>
      </div>
    </div>
  );
};

export default SubmitRun;
