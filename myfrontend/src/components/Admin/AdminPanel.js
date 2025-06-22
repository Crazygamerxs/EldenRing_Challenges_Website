import React, { useState, useEffect, useContext } from 'react';
import { Link } from 'react-router-dom';
import Cookies from 'js-cookie';
import './Admin.css';
import { UserContext } from '../common/UserContext';
import LoadingSpinner from '../common/LoadingSpinner';

import { API_ENDPOINTS } from '../../utils/api';
const AdminPanel = () => {
    const [stats, setStats] = useState({
        totalUsers: 0,
        totalChallenges: 0,
        pendingSubmissions: 0,
        approvedSubmissions: 0,
        rejectedSubmissions: 0
    });
    const [recentSubmissions, setRecentSubmissions] = useState([]);
    const [loading, setLoading] = useState(true);
    const { user } = useContext(UserContext);

    useEffect(() => {
        fetchAdminData();
    }, []);

    const fetchAdminData = async () => {
        setLoading(true);
        try {
            // Fetch admin dashboard stats
            const statsResponse = await fetch(API_ENDPOINTS.ADMIN_STATS, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            // Fetch recent submissions
            const submissionsResponse = await fetch(API_ENDPOINTS.ADMIN_RECENT_SUBMISSIONS, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!statsResponse.ok || !submissionsResponse.ok) {
                console.error('API Response Status:', {
                    stats: statsResponse.status,
                    submissions: submissionsResponse.status
                });
                throw new Error(`Failed to fetch admin data: Stats ${statsResponse.status}, Submissions ${submissionsResponse.status}`);
            }

            const statsData = await statsResponse.json();
            const submissionsData = await submissionsResponse.json();

            console.log('Admin data fetched successfully:', { statsData, submissionsData });
            setStats(statsData);
            setRecentSubmissions(submissionsData);
        } catch (error) {
            console.error('Error fetching admin data:', error);
            // Show error state instead of mock data
            setStats({
                totalUsers: 0,
                totalChallenges: 0,
                pendingSubmissions: 0,
                approvedSubmissions: 0,
                rejectedSubmissions: 0,
                error: 'Failed to load admin statistics'
            });
            setRecentSubmissions([]);
        } finally {
            setLoading(false);
        }
    };

    // Mock data generator for demonstration purposes
    const generateMockSubmissions = () => {
        return [
            {
                id: 1,
                username: 'TarnishedOne',
                challenge_name: 'No Hit Run',
                submitted_at: new Date(Date.now() - 1000 * 60 * 30).toISOString(), // 30 minutes ago
                status: 'pending'
            },
            {
                id: 2,
                username: 'EldenLord',
                challenge_name: 'Level 1 Weapon Only',
                submitted_at: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(), // 2 hours ago
                status: 'approved'
            },
            {
                id: 3,
                username: 'MaidenlessRun',
                challenge_name: 'No Armor Run',
                submitted_at: new Date(Date.now() - 1000 * 60 * 60 * 5).toISOString(), // 5 hours ago
                status: 'rejected'
            },
            {
                id: 4,
                username: 'LetMeSoloHer',
                challenge_name: 'Fists Only',
                submitted_at: new Date(Date.now() - 1000 * 60 * 60 * 8).toISOString(), // 8 hours ago
                status: 'pending'
            },
            {
                id: 5,
                username: 'RingBearer',
                challenge_name: 'No Healing',
                submitted_at: new Date(Date.now() - 1000 * 60 * 60 * 12).toISOString(), // 12 hours ago
                status: 'pending'
            }
        ];
    };

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    const getStatusBadge = (status) => {
        return <span className={`admin-status ${status}`}>{status.charAt(0).toUpperCase() + status.slice(1)}</span>;
    };

    if (loading) {
        return (
            <div className="admin-container">
                <div className="admin-loading">
                    <LoadingSpinner />
                </div>
            </div>
        );
    }

    return (
        <div className="admin-container">
            <div className="admin-header">
                <h1>Admin Dashboard</h1>
                <span className="admin-badge">Admin</span>
            </div>

            <div className="admin-nav">
                <Link to="/admin" className="admin-nav-item active">Dashboard</Link>
                <Link to="/admin/submissions" className="admin-nav-item">Submissions</Link>
                <Link to="/admin/challenges" className="admin-nav-item">Challenges</Link>
                <Link to="/admin/users" className="admin-nav-item">Users</Link>
                <Link to="/admin/settings" className="admin-nav-item">Settings</Link>
            </div>

            <div className="admin-content">
                <h2 style={{ color: '#a98b2d', marginTop: 0, marginBottom: '20px' }}>Overview</h2>
                
                <div className="admin-grid">
                    <div className="admin-card">
                        <h3>Users</h3>
                        <div className="admin-stat">
                            <span className="admin-stat-value">{stats.totalUsers}</span>
                            <span className="admin-stat-label">Total Users</span>
                        </div>
                    </div>
                    
                    <div className="admin-card">
                        <h3>Challenges</h3>
                        <div className="admin-stat">
                            <span className="admin-stat-value">{stats.totalChallenges}</span>
                            <span className="admin-stat-label">Total Challenges</span>
                        </div>
                    </div>
                    
                    <div className="admin-card">
                        <h3>Submissions</h3>
                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                            <div className="admin-stat">
                                <span className="admin-stat-value" style={{ color: '#ff9800' }}>{stats.pendingSubmissions}</span>
                                <span className="admin-stat-label">Pending</span>
                            </div>
                            <div className="admin-stat">
                                <span className="admin-stat-value" style={{ color: '#4caf50' }}>{stats.approvedSubmissions}</span>
                                <span className="admin-stat-label">Approved</span>
                            </div>
                            <div className="admin-stat">
                                <span className="admin-stat-value" style={{ color: '#f44336' }}>{stats.rejectedSubmissions}</span>
                                <span className="admin-stat-label">Rejected</span>
                            </div>
                        </div>
                    </div>
                </div>

                <h2 style={{ color: '#a98b2d', marginBottom: '20px' }}>Recent Submissions</h2>
                
                <div className="admin-table-container">
                    <table className="admin-table">
                        <thead>
                            <tr>
                                <th>User</th>
                                <th>Challenge</th>
                                <th>Submitted</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {recentSubmissions.map(submission => (
                                <tr key={submission.id}>
                                    <td>{submission.username}</td>
                                    <td>{submission.challenge_name}</td>
                                    <td>{formatDate(submission.submitted_at)}</td>
                                    <td>{getStatusBadge(submission.status)}</td>
                                    <td>
                                        <div className="admin-action-buttons">
                                            <Link 
                                                to={`/admin/submissions/${submission.id}`} 
                                                className="admin-action-button view"
                                            >
                                                View
                                            </Link>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <div style={{ textAlign: 'center', marginTop: '20px' }}>
                    <Link to="/admin/submissions" className="admin-button">
                        View All Submissions
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default AdminPanel;
