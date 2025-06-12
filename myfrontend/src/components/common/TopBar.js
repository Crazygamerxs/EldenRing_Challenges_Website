import React, { useContext, useState, useEffect, useCallback } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './common.css'; 
import images from '../../images';
import { UserContext } from '../common/UserContext';
import { API_ENDPOINTS } from '../../utils/api';
import Cookies from 'js-cookie';

const TopBar = () => {
    const { user, loading, logout } = useContext(UserContext);
    const navigate = useNavigate();
    const [unreadCount, setUnreadCount] = useState(0);

    // Memoized function to fetch unread count
    const fetchUnreadNotificationsCount = useCallback(async () => {
        try {
            const csrfToken = Cookies.get('csrftoken');
            const response = await fetch(API_ENDPOINTS.NOTIFICATIONS_UNREAD_COUNT, {
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
    }, []);

    useEffect(() => {
        if (user) {
            fetchUnreadNotificationsCount();
            
            // Set up interval to refresh count every 30 seconds
            const interval = setInterval(fetchUnreadNotificationsCount, 30000);
            
            return () => clearInterval(interval);
        }
    }, [user, fetchUnreadNotificationsCount]);

    // Listen for custom events to update notification count
    useEffect(() => {
        const handleNotificationUpdate = () => {
            fetchUnreadNotificationsCount();
        };

        // Listen for custom events
        window.addEventListener('notificationMarkedRead', handleNotificationUpdate);
        window.addEventListener('notificationAllMarkedRead', handleNotificationUpdate);
        
        return () => {
            window.removeEventListener('notificationMarkedRead', handleNotificationUpdate);
            window.removeEventListener('notificationAllMarkedRead', handleNotificationUpdate);
        };
    }, [fetchUnreadNotificationsCount]);

    const handleLogout = async () => {
        await logout();
        navigate('/login'); // Redirect to login page after logout
    };

    // Buy Me a Coffee click handler
    const handleBuyMeCoffeeClick = () => {
        // Replace 'yourusername' with your actual Buy Me a Coffee username
        window.open('https://buymeacoffee.com/Soda', '_blank', 'noopener,noreferrer');
    };

    // Cycling button text and icon messages on reload
    const [buttonIndex] = useState(() => {
        // Cycle through messages based on page reload
        return Math.floor(Date.now() / 10000) % 3; // Changes every 10 seconds of real time
    });
    
    const buttonMessages = [
        {
            text: "Support the Tarnished's Rune addiction",
            icon: "⚔️",
            theme: "tarnished"
        },
        {
            text: "Fund Ranni's research project (not a cult)",
            icon: "🌙",
            theme: "ranni"
        },
        {
            text: "Aid a Tarnished lost between grace and ruin",
            icon: "🔥",
            theme: "weary"
        }
    ];

    const buttonContent = buttonMessages[buttonIndex];

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
            </div>
            <div className="right-section">
                {user ? (
                    <>
                        {/* Elden Ring themed donation button */}
                        <button 
                            onClick={handleBuyMeCoffeeClick}
                            className={`elden-coffee-btn hover-effect ${buttonContent.theme}`}
                        >
                            <span className="elden-icon">{buttonContent.icon}</span>
                            <span className="elden-text">{buttonContent.text}</span>
                        </button>
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
                        {/* Show donation button for non-logged in users too */}
                        <button 
                            onClick={handleBuyMeCoffeeClick}
                            className={`elden-coffee-btn hover-effect ${buttonContent.theme}`}
                        >
                            <span className="elden-icon">{buttonContent.icon}</span>
                            <span className="elden-text">{buttonContent.text}</span>
                        </button>
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
