import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'js-cookie';
import './SignUp.css';

const SignUp = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [csrfReady, setCsrfReady] = useState(false);
    const navigate = useNavigate();

    // Wait for CSRF token to be available
    const waitForCsrfToken = async (maxWait = 5000) => {
        const startTime = Date.now();
        
        while (Date.now() - startTime < maxWait) {
            const token = Cookies.get('csrftoken');
            if (token) {
                console.log('CSRF token found:', token.substring(0, 10) + '...');
                return token;
            }
            // Wait 100ms before checking again
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        
        throw new Error('CSRF token not available after waiting');
    };

    // Ensure CSRF token is available when component mounts
    useEffect(() => {
        const ensureCsrfToken = async () => {
            try {
                // First check if token already exists
                let token = Cookies.get('csrftoken');
                
                if (!token) {
                    console.log('No CSRF token found, fetching...');
                    // Fetch CSRF token
                    await axios.get('http://localhost:8888/api/csrf-token/', { 
                        withCredentials: true,
                        timeout: 10000
                    });
                    
                    // Wait for token to be set
                    token = await waitForCsrfToken();
                }
                
                setCsrfReady(true);
                console.log('CSRF token ready for signup page');
            } catch (error) {
                console.error('Error ensuring CSRF token:', error);
                setError('Security initialization failed. Please refresh the page.');
            }
        };

        ensureCsrfToken();
    }, []);

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

        if (!csrfReady) {
            setError('Security token not ready. Please wait a moment.');
            return;
        }

        if (!validateForm()) {
            return;
        }

        setIsLoading(true);

        try {
            // Get CSRF token with retry
            const csrfToken = await waitForCsrfToken();
            console.log('Using CSRF Token for signup:', csrfToken.substring(0, 10) + '...');

            const response = await fetch('http://localhost:8888/api/signup/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({ 
                    username: username.trim().toLowerCase(), 
                    email: email.trim().toLowerCase(), 
                    password 
                }),
                credentials: 'include',
            });

            if (response.ok) {
                setSuccess('Account created successfully! Redirecting to login...');
                
                // Clear form
                setUsername('');
                setEmail('');
                setPassword('');
                
                // Redirect to login page after a short delay
                setTimeout(() => {
                    navigate('/login?signupSuccess=Account created successfully! Please log in.');
                }, 2000);
            } else {
                const errorData = await response.json();
                
                if (errorData.error) {
                    setError(errorData.error);
                } else if (response.status === 400) {
                    setError('Invalid input. Please check your information and try again.');
                } else if (response.status === 403) {
                    setError('Security token expired. Please refresh the page and try again.');
                } else {
                    setError('Sign up failed. Please try again.');
                }
            }
        } catch (error) {
            console.error('Error during signup:', error);
            
            if (error.message.includes('CSRF')) {
                setError('Security token not available. Please refresh the page.');
            } else if (error.name === 'TypeError' && error.message.includes('fetch')) {
                setError('Network error. Please check your connection and try again.');
            } else {
                setError('An unexpected error occurred. Please try again.');
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className='signup-page'>
            <div className="sign-up-content">
                <h2>SIGN UP FOR ELDENRING.CA</h2>
                
                {!csrfReady && (
                    <div style={{ 
                        background: '#a98b2d', 
                        color: 'white', 
                        padding: '10px', 
                        borderRadius: '5px', 
                        marginBottom: '15px',
                        textAlign: 'center'
                    }}>
                        Initializing security...
                    </div>
                )}
                
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
                            disabled={!csrfReady || isLoading}
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
                            disabled={!csrfReady || isLoading}
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
                            disabled={!csrfReady || isLoading}
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
                            disabled={!csrfReady || isLoading}
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