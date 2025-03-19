import React, { useContext, useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './common.css'; 
import images from '../../images';
import { UserContext } from '../common/UserContext';
import Cookies from 'js-cookie';

const TopBar = () => {
    const { user, loading, logout } = useContext(UserContext);
    const navigate = useNavigate();
    const [unreadCount, setUnreadCount] = useState(0);

    useEffect(() => {
        if (user) {
            fetchUnreadNotificationsCount();
        }
    }, [user]);

    const fetchUnreadNotificationsCount = async () => {
        try {
            const csrfToken = Cookies.get('csrftoken');
            const response = await fetch('http://localhost:8888/api/notifications/unread-count/', {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
            });

            if (!response.ok) {
                throw new Error('Failed to fetch unread notifications count');
            }

            const data = await response.json();
            setUnreadCount(data.count);
        } catch (error) {
            console.error('Error fetching unread notifications count:', error);
            // For demo, set a random count
            setUnreadCount(Math.floor(Math.random() * 5));
        }
    };

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
                <Link to ='/leaderboard' className="nav-link hover-effect">Leaderboard</Link>
                {/* Community Board hidden for future implementation 
                <Link to="/CB" className="nav-link hover-effect">Community Board</Link>
                */}
                {/* Notifications moved to right section */}
            </div>
            <div className="right-section">
                {user ? (
                    <>
                        {/* Notification icon with unread count */}
                        <Link to="/notifications" className="notification-icon-link hover-effect">
                            <div className="notification-icon-container">
                                <i className="fas fa-bell"></i>
                                {unreadCount > 0 && (
                                    <span className="notification-badge">{unreadCount > 9 ? '9+' : unreadCount}</span>
                                )}
                            </div>
                        </Link>
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
