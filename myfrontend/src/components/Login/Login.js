// Updated Login.js with proper CSRF handling for production
import React, { useState, useContext, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { UserContext } from '../common/UserContext';
import './Login.css';
import Cookies from 'js-cookie';
import axios from 'axios';

const LogIn = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const [csrfReady, setCsrfReady] = useState(false);
    const navigate = useNavigate();
    const { login } = useContext(UserContext);

    // Get API URL based on environment
    const getApiUrl = (endpoint) => {
        if (process.env.NODE_ENV === 'production') {
            return endpoint; // Use relative URLs in production
        } else {
            return `http://localhost:8888${endpoint}`;
        }
    };

    // Configure axios defaults
    axios.defaults.withCredentials = true;
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFToken';

    // Get fresh CSRF token
    const getCsrfToken = async () => {
        try {
            console.log('Fetching fresh CSRF token...');
            const response = await axios.get(getApiUrl('/api/csrf-token/'), {
                withCredentials: true,
                timeout: 10000
            });
            
            // Wait a moment for cookie to be set
            await new Promise(resolve => setTimeout(resolve, 100));
            
            const token = Cookies.get('csrftoken');
            if (token) {
                console.log('Fresh CSRF token obtained');
                return token;
            } else {
                throw new Error('CSRF token not set after fetch');
            }
        } catch (error) {
            console.error('Error fetching CSRF token:', error);
            throw error;
        }
    };

    // Ensure CSRF token is available when component mounts
    useEffect(() => {
        const ensureCsrfToken = async () => {
            try {
                await getCsrfToken();
                setCsrfReady(true);
                console.log('CSRF token ready for login page');
            } catch (error) {
                console.error('Error ensuring CSRF token:', error);
                setError('Security initialization failed. Please refresh the page.');
            }
        };

        ensureCsrfToken();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        
        if (!csrfReady) {
            setError('Security token not ready. Please wait a moment.');
            return;
        }
        
        if (!username.trim() || !password.trim()) {
            setError('Please enter both username and password.');
            return;
        }

        setIsLoading(true);

        try {
            // Get a fresh CSRF token before login attempt
            const csrfToken = await getCsrfToken();
            
            console.log('Attempting login...');
            const response = await axios.post(
                getApiUrl('/api/login/'), 
                {
                    username: username.trim(),
                    password: password
                },
                {
                    withCredentials: true,
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    timeout: 15000
                }
            );

            if (response.status === 200 && response.data.success) {
                console.log('Login successful');
                login(response.data.user);
                navigate('/dashboard');
            } else {
                setError(response.data.message || 'Login failed. Please try again.');
            }
        } catch (error) {
            console.error('Login error:', error);
            
            if (error.response) {
                const status = error.response.status;
                const data = error.response.data;
                
                if (status === 403) {
                    // CSRF token issue - try to refresh and retry once
                    try {
                        console.log('CSRF token issue, getting fresh token...');
                        await getCsrfToken();
                        // Don't retry automatically to avoid infinite loops
                        setError('Security token expired. Please try logging in again.');
                    } catch (refreshError) {
                        setError('Security token refresh failed. Please refresh the page.');
                    }
                } else if (status === 401) {
                    setError(data.message || 'Invalid username or password.');
                } else if (status >= 500) {
                    setError('Server error. Please try again later.');
                } else {
                    setError(data.message || 'Login failed. Please try again.');
                }
            } else if (error.code === 'ECONNABORTED') {
                setError('Request timed out. Please check your connection and try again.');
            } else {
                setError('Connection error. Please check your internet connection.');
            }
        } finally {
            setIsLoading(false);
        }
    };

    if (!csrfReady) {
        return (
            <div className="login-container">
                <div className="login-box">
                    <h2>LOGIN TO ELDENRING.CA</h2>
                    <div className="loading">Initializing security...</div>
                </div>
            </div>
        );
    }

    return (
        <div className="login-container">
            <div className="login-box">
                <h2>LOGIN TO ELDENRING.CA</h2>
                
                {error && (
                    <div className="error-message">
                        {error}
                    </div>
                )}
                
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="username">Username *</label>
                        <input
                            type="text"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            disabled={isLoading}
                            autoComplete="username"
                            required
                        />
                    </div>
                    
                    <div className="form-group">
                        <label htmlFor="password">Password *</label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            disabled={isLoading}
                            autoComplete="current-password"
                            required
                        />
                    </div>
                    
                    <button 
                        type="submit" 
                        disabled={isLoading}
                        className="login-button"
                    >
                        {isLoading ? 'Logging in...' : 'Log In'}
                    </button>
                </form>
                
                <div className="form-links">
                    <Link to="/forgot-password">Forgot Password?</Link>
                    <Link to="/signup">Sign up</Link>
                </div>
            </div>
        </div>
    );
};

export default LogIn;