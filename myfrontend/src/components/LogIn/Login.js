import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import TopBar from '../common/TopBar';
import BottomBar from '../common/BottomBar';
import './Login.css';

const LogIn = () => {
    const [username, setusername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://127.0.0.1:8888/api/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            if (response.ok) {
                navigate('/home');
            } else {
                const errorData = await response.json();
                alert(errorData.error);
            }
        } catch (error) {
            console.error('Error during login:', error);
        }
    };

    return (
        <div>
            <TopBar />
            <div className='login-page'>
                <div className="login-content">
                    <h2>LOGIN TO ELDENRING.CA</h2>
                    <form onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label htmlFor="username">username</label>
                            <input
                                type="username"
                                id="username"
                                value={username}
                                onChange={(e) => setusername(e.target.value)}
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
            <BottomBar />
        </div>
    );
};

export default LogIn;
