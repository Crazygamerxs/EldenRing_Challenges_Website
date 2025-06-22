import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './SignUp.css';
import { API_ENDPOINTS } from '../../utils/api';

const SignUp = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();

    // Validate form inputs
    const validateForm = () => {
        if (username.length < 3) {
            setError('Username must be at least 3 characters long.');
            return false;
        }

        if (username.length > 30) {
            setError('Username must be less than 30 characters.');
            return false;
        }

        if (!/^[a-zA-Z0-9_-]+$/.test(username)) {
            setError('Username can only contain letters, numbers, underscores, and hyphens.');
            return false;
        }

        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            setError('Please enter a valid email address.');
            return false;
        }

        if (password.length < 8) {
            setError('Password must be at least 8 characters long.');
            return false;
        }

        return true;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        if (!validateForm()) {
            return;
        }

        setIsLoading(true);

        try {
            const response = await axios.post(API_ENDPOINTS.SIGNUP, {
                username,
                email,
                password
            }, {
                withCredentials: true,
                timeout: 10000
            });

            setSuccess('Account created successfully! Redirecting to login...');
            
            // Clear form
            setUsername('');
            setEmail('');
            setPassword('');
            
            // Redirect to login page after a short delay
            setTimeout(() => {
                navigate('/login?signupSuccess=Account created successfully! Please log in.');
            }, 2000);
        } catch (error) {
            console.error('Error during signup:', error);
            
            if (error.response?.data?.error) {
                setError(error.response.data.error);
            } else if (error.response?.status === 400) {
                setError('Invalid input. Please check your information and try again.');
            } else if (error.response?.status === 403) {
                setError('Authentication failed. Please try again.');
            } else {
                setError('Sign up failed. Please try again.');
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className='signup-page'>
            <div className="sign-up-content">
                <h2>SIGN UP FOR ELDENRING.CA</h2>
                
                {error && (
                    <div style={{ 
                        background: '#f44336', 
                        color: 'white', 
                        padding: '10px', 
                        borderRadius: '5px', 
                        marginBottom: '15px' 
                    }}>
                        {error}
                    </div>
                )}
                
                {success && (
                    <div style={{ 
                        background: '#4caf50', 
                        color: 'white', 
                        padding: '10px', 
                        borderRadius: '5px', 
                        marginBottom: '15px' 
                    }}>
                        {success}
                    </div>
                )}
                
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="username">Username</label>
                        <input
                            type="text"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                            disabled={isLoading}
                            placeholder="Enter a unique username"
                            maxLength={30}
                        />
                        <small style={{ color: '#909090', fontSize: '12px' }}>
                            3-30 characters, letters, numbers, underscore, and hyphen only
                        </small>
                    </div>
                    <div className="form-group">
                        <label htmlFor="email">Email Address</label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            disabled={isLoading}
                            placeholder="Enter your email address"
                        />
                        <small style={{ color: '#909090', fontSize: '12px' }}>
                            We'll use this for password resets and important updates
                        </small>
                    </div>
                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            disabled={isLoading}
                            placeholder="Create a strong password"
                            minLength={8}
                        />
                        <small style={{ color: '#909090', fontSize: '12px' }}>
                            At least 8 characters long
                        </small>
                    </div>
                    <div className="form-actions">
                        <button 
                            type="submit" 
                            disabled={isLoading}
                        >
                            {isLoading ? 'Creating Account...' : 'Sign Up'}
                        </button>
                        <button 
                            type="button" 
                            onClick={() => navigate('/login')}
                            disabled={isLoading}
                        >
                            Already have an account?
                        </button>
                    </div>
                </form>
                
                {/* <div style={{ 
                    marginTop: '20px', 
                    padding: '10px', 
                    background: 'rgba(169, 139, 45, 0.1)', 
                    borderRadius: '5px',
                    fontSize: '14px',
                    color: '#f0f0f0'
                }}> */}
                    {/* <strong>Account Guidelines:</strong> */}
                    {/* <ul style={{ margin: '5px 0', paddingLeft: '20px' }}>
                        <li>Choose a unique username you'll remember</li>
                        <li>Use a valid email address for account verification</li>
                        <li>Create a strong password to keep your account secure</li>
                        <li>All usernames and emails are converted to lowercase</li>
                    </ul> */}
                {/* </div> */}
            </div>
        </div>
    );
};

export default SignUp;
