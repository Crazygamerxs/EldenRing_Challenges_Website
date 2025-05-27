import React, { useState, useEffect, useContext } from 'react';
import { Link } from 'react-router-dom';
import Cookies from 'js-cookie';
import './Notifications.css';
import { UserContext } from '../common/UserContext';
import LoadingSpinner from '../common/LoadingSpinner';
import images from '../../images';

const Notifications = () => {
    const [notifications, setNotifications] = useState([]);
    const [loading, setLoading] = useState(true);
    const { user } = useContext(UserContext);

    useEffect(() => {
        if (user) {
            fetchNotifications();
        }
    }, [user]);

    const fetchNotifications = async () => {
        setLoading(true);
        try {
            const csrfToken = Cookies.get('csrftoken');
            const response = await fetch('http://localhost:8888/api/notifications/', {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
            });

            if (!response.ok) {
                throw new Error('Failed to fetch notifications');
            }

            const data = await response.json();
            setNotifications(data);
        } catch (error) {
            console.error('Error fetching notifications:', error);
            // If API fails, use mock data for demonstration
            setNotifications(generateMockNotifications());
        } finally {
            setLoading(false);
        }
    };

    const markAsRead = async (notificationId) => {
        try {
            const csrfToken = Cookies.get('csrftoken');
            const response = await fetch(`http://localhost:8888/api/notifications/${notificationId}/read/`, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Failed to mark notification as read');
            }

            // Update local state
            setNotifications(prevNotifications => 
                prevNotifications.map(notification => 
                    notification.id === notificationId 
                        ? { ...notification, read: true } 
                        : notification
                )
            );

            // Dispatch custom event to update TopBar notification count
            window.dispatchEvent(new CustomEvent('notificationMarkedRead'));
        } catch (error) {
            console.error('Error marking notification as read:', error);
            // For demo, update the UI anyway
            setNotifications(prevNotifications => 
                prevNotifications.map(notification => 
                    notification.id === notificationId 
                        ? { ...notification, read: true } 
                        : notification
                )
            );
            // Still dispatch event for demo
            window.dispatchEvent(new CustomEvent('notificationMarkedRead'));
        }
    };

    const markAllAsRead = async () => {
        try {
            const csrfToken = Cookies.get('csrftoken');
            const response = await fetch('http://localhost:8888/api/notifications/mark-all-read/', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Failed to mark all notifications as read');
            }

            // Update local state
            setNotifications(prevNotifications => 
                prevNotifications.map(notification => ({ ...notification, read: true }))
            );

            // Dispatch custom event to update TopBar notification count
            window.dispatchEvent(new CustomEvent('notificationAllMarkedRead'));
        } catch (error) {
            console.error('Error marking all notifications as read:', error);
            // For demo, update the UI anyway
            setNotifications(prevNotifications => 
                prevNotifications.map(notification => ({ ...notification, read: true }))
            );
            // Still dispatch event for demo
            window.dispatchEvent(new CustomEvent('notificationAllMarkedRead'));
        }
    };

    // Mock data generator for demonstration purposes
    const generateMockNotifications = () => {
        return [
            {
                id: 1,
                title: 'Run Submission Approved',
                content: 'Your submission for "No Hit Run" has been approved and added to the leaderboard!',
                created_at: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(), // 2 hours ago
                read: false,
                type: 'success',
                challenge_id: 1,
                challenge_name: 'No Hit Run',
                status: 'approved'
            },
            {
                id: 2,
                title: 'Run Submission Rejected',
                content: 'Your submission for "Level 1 Weapon Only" has been rejected. Reason: Video does not show the entire run.',
                created_at: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(), // 1 day ago
                read: true,
                type: 'error',
                challenge_id: 2,
                challenge_name: 'Level 1 Weapon Only',
                status: 'rejected'
            },
            {
                id: 3,
                title: 'Run Submission Received',
                content: 'Your submission for "No Armor Run" has been received and is pending review.',
                created_at: new Date(Date.now() - 1000 * 60 * 30).toISOString(), // 30 minutes ago
                read: false,
                type: 'info',
                challenge_id: 3,
                challenge_name: 'No Armor Run',
                status: 'pending'
            }
        ];
    };

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now - date;
        const diffSec = Math.floor(diffMs / 1000);
        const diffMin = Math.floor(diffSec / 60);
        const diffHour = Math.floor(diffMin / 60);
        const diffDay = Math.floor(diffHour / 24);

        if (diffDay > 0) {
            return diffDay === 1 ? '1 day ago' : `${diffDay} days ago`;
        } else if (diffHour > 0) {
            return diffHour === 1 ? '1 hour ago' : `${diffHour} hours ago`;
        } else if (diffMin > 0) {
            return diffMin === 1 ? '1 minute ago' : `${diffMin} minutes ago`;
        } else {
            return 'Just now';
        }
    };

    const getStatusBadge = (status) => {
        switch (status) {
            case 'approved':
                return <span className="notification-badge badge-approved">Approved</span>;
            case 'rejected':
                return <span className="notification-badge badge-rejected">Rejected</span>;
            case 'pending':
                return <span className="notification-badge badge-pending">Pending</span>;
            default:
                return null;
        }
    };

    return (
        <div className="notifications-container">
            <div className="notifications-header">
                <h1>Notifications</h1>
                <div className="notifications-actions">
                    {notifications.length > 0 && notifications.some(n => !n.read) && (
                        <button 
                            onClick={markAllAsRead}
                            className="notification-mark-all-read"
                        >
                            Mark All as Read
                        </button>
                    )}
                </div>
            </div>

            {loading ? (
                <div className="loading-container">
                    <LoadingSpinner />
                </div>
            ) : notifications.length === 0 ? (
                <div className="notification-empty">
                    <h3>No Notifications</h3>
                    <p>You don't have any notifications yet. When you submit runs or receive updates, they will appear here.</p>
                </div>
            ) : (
                <div className="notifications-list">
                    {notifications.map(notification => (
                        <div 
                            key={notification.id} 
                            className={`notification-item ${!notification.read ? 'unread' : ''} ${notification.type}`}
                        >
                            <div className="notification-header">
                                <h3 className="notification-title">
                                    {notification.title}
                                    {getStatusBadge(notification.status)}
                                </h3>
                                <span className="notification-date">{formatDate(notification.created_at)}</span>
                            </div>
                            <p className="notification-content">{notification.content}</p>
                            <div className="notification-actions">
                                <Link to={`/challenge/${notification.challenge_id}`} className="notification-challenge">
                                    <img src={images.pin} alt="Challenge" style={{ width: '16px', height: '16px' }} />
                                    View Challenge: {notification.challenge_name}
                                </Link>
                                {!notification.read && (
                                    <button 
                                        onClick={() => markAsRead(notification.id)}
                                        className="notification-mark-read"
                                    >
                                        Mark as Read
                                    </button>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default Notifications;