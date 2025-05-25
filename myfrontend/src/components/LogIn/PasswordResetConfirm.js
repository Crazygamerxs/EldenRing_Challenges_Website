import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'js-cookie';
import './Login.css';

const PasswordResetConfirm = () => {
    const { uidb64, token } = useParams();
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [csrfReady, setCsrfReady] = useState(false);
    const navigate = useNavigate();

    // Wait for CSRF token to be available
    const waitForCsrfToken = async (maxWait = 5000) => {
        const startTime = Date.now();
        
        while (Date.now() - startTime < maxWait) {
            const token = Cookies.get('csrftoken');
            if (token) {
                return token;
            }
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        
        throw new Error('CSRF token not available after waiting');
    };

    // Ensure CSRF token is available when component mounts
    useEffect(() => {
        const ensureCsrfToken = async () => {
            try {
                let token = Cookies.get('csrftoken');
                
                if (!token) {
                    console.log('No CSRF token found, fetching...');
                    await axios.get('http://localhost:8888/api/csrf-token/', { 
                        withCredentials: true,
                        timeout: 10000
                    });
                    
                    token = await waitForCsrfToken();
                }
                
                setCsrfReady(true);
                console.log('CSRF token ready for password reset confirm page');
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
        setMessage('');

        // Check if passwords match
        if (password !== confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        if (!csrfReady) {
            setError('Security token not ready. Please wait a moment.');
            return;
        }

        setIsLoading(true);

        try {
            const csrfToken = await waitForCsrfToken();
            console.log('Using CSRF Token for password reset confirm:', csrfToken.substring(0, 10) + '...');

            const response = await axios.post(`http://localhost:8888/api/password-reset-confirm/${uidb64}/${token}/`, {
                password,
            }, {
                withCredentials: true,
                headers: {
                    'X-CSRFToken': csrfToken,
                },
                timeout: 10000
            });

            setMessage(response.data.message);
            
            // Redirect to login after successful password reset
            setTimeout(() => {
                navigate('/login');
            }, 2000);
            
        } catch (error) {
            console.error('Error during password reset confirmation:', error);
            
            if (error.response?.status === 403) {
                setError('Security token expired. Please refresh the page and try again.');
            } else if (error.response?.status === 400) {
                setError('Invalid or expired reset link. Please request a new password reset.');
            } else if (error.message.includes('CSRF')) {
                setError('Security token not available. Please refresh the page.');
            } else {
                setError('Failed to reset password. Please try again.');
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className='login-page'>
            <div className="login-content">
                <h2>Reset Your Password</h2>
                
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
                
                {message && (
                    <div style={{ 
                        background: '#4caf50', 
                        color: 'white', 
                        padding: '10px', 
                        borderRadius: '5px', 
                        marginBottom: '15px' 
                    }}>
                        {message}
                        <br />
                        <small>Redirecting to login page...</small>
                    </div>
                )}
                
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="password">New Password</label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            disabled={!csrfReady || isLoading}
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
                            disabled={!csrfReady || isLoading}
                        />
                    </div>
                    <div className="form-actions">
                        <button 
                            type="submit"
                            disabled={!csrfReady || isLoading}
                        >
                            {isLoading ? 'Resetting...' : 'Reset Password'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default PasswordResetConfirm;