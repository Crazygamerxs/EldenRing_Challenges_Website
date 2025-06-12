// src/components/Login/LogIn.js
import React, { useState, useContext, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { UserContext } from '../common/UserContext';
import './Login.css';
import Cookies from 'js-cookie';
import axios from 'axios';

import { API_ENDPOINTS } from '../../utils/api';
const LogIn = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const [csrfReady, setCsrfReady] = useState(false);
    const navigate = useNavigate();
    const { login } = useContext(UserContext);

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
                    await axios.get(API_ENDPOINTS.CSRF_TOKEN, { 
                        withCredentials: true,
                        timeout: 10000
                    });
                    
                    // Wait for token to be set
                    token = await waitForCsrfToken();
                }
                
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
        
        setIsLoading(true);
    
        try {
            // Get CSRF token with retry
            const csrfToken = await waitForCsrfToken();
            console.log('Using CSRF Token for login:', csrfToken.substring(0, 10) + '...');
    
            const response = await axios.post(API_ENDPOINTS.LOGIN, {
                username: username.trim().toLowerCase(), // Ensure lowercase
                password
            }, {
                withCredentials: true,
                headers: {
                    'X-CSRFToken': csrfToken,
                },
                timeout: 10000
            });

            console.log('Login successful:', response.data);
            
            // Update user context
            await login({ username });
            
            navigate('/home?loginSuccess=Login successful!');
        } catch (error) {
            console.error('Error during login:', error);
            
            if (error.response?.status === 403) {
                setError('Security token expired. Please refresh the page and try again.');
            } else if (error.response?.status === 401) {
                setError('Invalid username or password.');
            } else if (error.message.includes('CSRF')) {
                setError('Security token not available. Please refresh the page.');
            } else {
                setError('Login failed. Please try again.');
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className='login-page'>
            <div className="login-content">
                <h2>LOGIN TO ELDENRING.CA</h2>
                
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
                        />
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
                        />
                    </div>
                    <div className="form-actions">
                        <button 
                            type="submit" 
                            disabled={!csrfReady || isLoading}
                        >
                            {isLoading ? 'Logging in...' : 'Log In'}
                        </button>
                        <Link to="/password-reset" className='forgot-password'>Forgot Password?</Link>
                        <button 
                            type="button" 
                            onClick={() => navigate('/signup')}
                            disabled={isLoading}
                        >
                            Sign up
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default LogIn;