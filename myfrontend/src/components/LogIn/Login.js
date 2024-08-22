// src/components/Login/LogIn.js
import React, { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { UserContext } from '../common/UserContext';
import './Login.css';
import Cookies from 'js-cookie';
import CSRFTOKEN from "../common/CSRFToken";
import axios from 'axios';

const LogIn = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    const { login } = useContext(UserContext);

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        const csrfToken = Cookies.get('csrftoken');
        console.log('Retrieved CSRF Token from Cookies:', csrfToken);
    
        try {
            const response = await axios.post('http://localhost:8888/api/login/', {
                username,
                password
            }, {
                withCredentials: true,
                headers: {
                    'X-CSRFToken': csrfToken,
                }
            });

            console.log('Login successful:', response.data);
            login({ username });
            navigate('/home?loginSuccess=Login successful!');
        } catch (error) {
            console.error('Error during login:', error.response ? error.response.data : error.message);
        }
    };

    return (
        <div className='login-page'>
            <div className="login-content">
                <h2>LOGIN TO ELDENRING.CA</h2>
                <form onSubmit={handleSubmit}>
                    <CSRFTOKEN />
                    <div className="form-group">
                        <label htmlFor="username">Username</label>
                        <input
                            type="text"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
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
                        />
                    </div>
                    <div className="form-actions">
                        <button type="submit">Log In</button>
                        <Link to="/password-reset" className='forgot-password'>Forgot Password?</Link>
                        <button type="button" onClick={() => navigate('/signup')}>Sign up</button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default LogIn;
