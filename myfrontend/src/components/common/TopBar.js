import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom'; // Import useNavigate
import './common.css'; 
import images from '../../images';
import { UserContext } from '../common/UserContext'; 

const TopBar = () => {
    const { user, loading, logout } = useContext(UserContext);
    const navigate = useNavigate(); // Use useNavigate for redirection

    const handleLogout = async () => {
        await logout();
        navigate('/login'); // Redirect to login page after logout
    };

    if (loading) {
        return (
            <div className="top-bar">
                <div className="left-section">
                    <div className='menu-icon'>
                        <img src={images.cat_logo} alt="cat logo" />
                    </div>
                    <h1 className="heading">EldenRing.ca</h1>
                </div>
                <div className='middle-section'>
                    <span className="nav-link">Loading...</span>
                </div>
                <div className="right-section">
                    <span className="nav-link">Loading...</span>
                </div>
            </div>
        );
    }

    return (
        <div className="top-bar">
            <div className="left-section">
                <div className='menu-icon'>
                    <img src={images.cat_logo} alt="cat logo" />
                </div>
                <Link to="/home" className="nav-link">
                    <h1 className="heading">EldenRing.ca</h1>
                </Link>
            </div>
            <div className='middle-section'>
                <Link to="/home" className="nav-link hover-effect">Challenge</Link>
                <Link to="/CB" className="nav-link hover-effect">Community Board</Link>
            </div>
            <div className="right-section">
                {user ? (
                    <>
                        <span className="nav-link hover-effect">Hey, {user.username}</span>
                        <button onClick={handleLogout} className="logout-btn">Logout</button>
                    </>
                ) : (
                    <>
                        <Link to="/login" className="nav-link">Login</Link>
                        <button className="signup-btn">
                            <Link to="/signup" className="signup-link">Sign up</Link>
                        </button>
                    </>
                )}
            </div>
        </div>
    );
};

export default TopBar;
