import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import TopBar from '../common/TopBar';
import BottomBar from '../common/BottomBar';
import './SignUp.css'; // Make sure this CSS file is updated with the new styles

const SignUp = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://127.0.0.1:8888/api/signup/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, email, password }),
            });

            if (response.ok) {
                navigate('/home');
            } else {
                const errorData = await response.json();
                alert(errorData.error);
            }
        } catch (error) {
            console.error('Error during signup:', error);
        }
    };

    return (
        <div>
            <TopBar />
            <div className='signup-page'>
                <div className="sign-up-content">
                    <h2>SIGN UP FOR ELDENRING.CA</h2>
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
                            <label htmlFor="email">Email Address</label>
                            <input
                                type="email"
                                id="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
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
                            <button type="submit">Sign Up</button>
                            <button type="button" onClick={() => navigate('/login')}>Already have an account?</button>
                        </div>
                    </form>
                </div>
            </div>
            <BottomBar />
        </div>
    );
};

export default SignUp;
