// src/components/Login/LogIn.js
import React, { useState, useContext, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { UserContext } from '../common/UserContext';
import './Login.css';
import { API_ENDPOINTS } from '../../utils/api';
import axios from 'axios';

const LogIn = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const { login } = useContext(UserContext);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);
    
        try {
            const response = await axios.post(API_ENDPOINTS.LOGIN, {
                username,
                password
            }, {
                withCredentials: true,
                timeout: 10000
            });
            
            // Update user context with the returned user data
            await login(response.data.user);
            
            navigate('/home?loginSuccess=Login successful!');
        } catch (error) {
            console.error('Error during login:', error);
            
            if (error.response?.status === 401) {
                setError('Invalid username or password.');
            } else if (error.response?.status === 403) {
                setError('Authentication failed. Please try again.');
            } else if (error.response?.data?.error) {
                setError(error.response.data.error);
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
                            disabled={isLoading}
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
                            disabled={isLoading}
                        />
                    </div>
                    <div className="form-actions">
                        <button 
                            type="submit" 
                            disabled={isLoading}
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
