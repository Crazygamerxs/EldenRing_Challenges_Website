import React, { useState } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import './Login.css';

const PasswordResetRequest = () => {
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const csrfToken = Cookies.get('csrftoken');
        console.log('Retrieved CSRF Token from Cookies:', csrfToken);
    
        try {
            const response = await axios.post('http://localhost:8888/api/password-reset/', {
                email,
            }, {
                withCredentials: true, // Include credentials for cross-site requests
                headers: {
                    'X-CSRFToken': csrfToken,
                }
            });
    
            setMessage(response.data.message);
        } catch (error) {
            console.error('Error during password reset request:', error.response ? error.response.data : error.message);
        }
    };
    

    return (
        <div className='login-page'>
            <div className="login-content">
                <h2>Password Reset</h2>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="email">Email</label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-actions">
                        <button type="submit">Send Reset Link</button>
                    </div>
                </form>
                {message && <p>{message}</p>}
            </div>
        </div>
    );
};

export default PasswordResetRequest;
