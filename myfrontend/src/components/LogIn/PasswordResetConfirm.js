import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'js-cookie';
import './Login.css';

const PasswordResetConfirm = () => {
    const { uidb64, token } = useParams();
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Check if passwords match
        if (password !== confirmPassword) {
            setMessage('Passwords do not match');
            return;
        }

        const csrfToken = Cookies.get('csrftoken');
        console.log('Retrieved CSRF Token from Cookies:', csrfToken);

        try {
            const response = await axios.post(`http://localhost:8888/api/password-reset-confirm/${uidb64}/${token}/`, {
                password,
            }, {
                withCredentials: true, // Include credentials for cross-site requests
                headers: {
                    'X-CSRFToken': csrfToken,
                }
            });

            setMessage(response.data.message);
            navigate('/login');
        } catch (error) {
            console.error('Error during password reset confirmation:', error.response ? error.response.data : error.message);
        }
    };

    return (
        <div className='login-page'>
            <div className="login-content">
                <h2>Reset Your Password</h2>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="password">New Password</label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="confirm-password">Confirm New Password</label>
                        <input
                            type="password"
                            id="confirm-password"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-actions">
                        <button type="submit">Reset Password</button>
                    </div>
                </form>
                {message && <p>{message}</p>}
            </div>
        </div>
    );
};

export default PasswordResetConfirm;
