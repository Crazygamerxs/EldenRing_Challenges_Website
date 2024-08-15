import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { UserContext } from '../common/UserContext';
import './Login.css';

const LogIn = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    const { login } = useContext(UserContext);
    const printCookies = () => {
        console.log('Cookies:', document.cookie);
      };
      
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://127.0.0.1:8888/api/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include', 
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (response.ok) {
                console.log('Login successful:', data);
                console.log('Logged in username:', username);
                
                printCookies(); // Print cookies to console
                // Pass user data to the login context
                login({ username });

                navigate(data.redirect || '/home');
            } else {
                alert(data.error);
            }
        } catch (error) {
            console.error('Error during login:', error);
        }
    };

    return (
        <div className='login-page'>
            <div className="login-content">
                <h2>LOGIN TO ELDENRING.CA</h2>
                <form onSubmit={handleSubmit}>
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
                        <button type="button" onClick={() => navigate('/signup')}>Don't have an account?</button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default LogIn;
