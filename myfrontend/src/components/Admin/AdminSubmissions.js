import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Cookies from 'js-cookie';
import './Admin.css';
import LoadingSpinner from '../common/LoadingSpinner';

const AdminSubmissions = () => {
    const [submissions, setSubmissions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [statusFilter, setStatusFilter] = useState('all');
    const [userFilter, setUserFilter] = useState('');
    const [challengeFilter, setChallengeFilter] = useState('');
    const [users, setUsers] = useState([]);
    const [challenges, setChallenges] = useState([]);
    const [selectedSubmission, setSelectedSubmission] = useState(null);
    const [showRejectModal, setShowRejectModal] = useState(false);
    const [showApproveModal, setShowApproveModal] = useState(false);
    const [rejectReason, setRejectReason] = useState('');
    const [adminVerifiedTime, setAdminVerifiedTime] = useState('');
    const [actionLoading, setActionLoading] = useState(false);

    useEffect(() => {
        fetchSubmissions();
        fetchUsers();
        fetchChallenges();
    }, []);

    useEffect(() => {
        fetchSubmissions();
    }, [statusFilter, userFilter, challengeFilter]);

    const fetchSubmissions = async () => {
        setLoading(true);
        try {
            const csrfToken = Cookies.get('csrftoken');
            let endpoint = `http://localhost:8888/api/admin/submissions/?status=${statusFilter}`;
            
            if (userFilter) {
                endpoint += `&user=${userFilter}`;
            }
            
            if (challengeFilter) {
                endpoint += `&challenge=${challengeFilter}`;
            }
            
            const response = await fetch(endpoint, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
            });

            if (!response.ok) {
                throw new Error('Failed to fetch submissions');
            }

            const data = await response.json();
            setSubmissions(data);
        } catch (error) {
            console.error('Error fetching submissions:', error);
            alert('Failed to load submissions. Please refresh the page.');
        } finally {
            setLoading(false);
        }
    };

    // Replace your handleApprove method with this fixed version:

const handleApprove = async (submissionId, adminTime = '') => {
    setActionLoading(true);
    try {
        const csrfToken = Cookies.get('csrftoken');
        const requestBody = {};
        
        if (adminTime) {
            requestBody.admin_verified_time = adminTime;
        }
        
        const response = await fetch(`http://localhost:8888/api/admin/submissions/${submissionId}/approve/`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
            throw new Error('Failed to approve submission');
        }

        const result = await response.json();
        
        // Update local state
        setSubmissions(prevSubmissions => 
            prevSubmissions.map(submission => 
                submission.id === submissionId 
                    ? { 
                        ...submission, 
                        status: 'approved',
                        points_awarded: result.pointsAwarded,
                        admin_verified_time: result.adminVerifiedTime || adminTime || null
                    } 
                    : submission
            )
        );

        alert(`Submission approved successfully! ${result.pointsAwarded} points awarded.`);
        setShowApproveModal(false);
        setAdminVerifiedTime('');
    } catch (error) {
        console.error('Error approving submission:', error);
        alert('Failed to approve submission. Please try again.');
    } finally {
        setActionLoading(false);
    }
};

    const openApproveModal = (submission) => {
        setSelectedSubmission(submission);
        setAdminVerifiedTime('');
        setShowApproveModal(true);
    };

    const openRejectModal = (submission) => {
        setSelectedSubmission(submission);
        setRejectReason('');
        setShowRejectModal(true);
    };

    const handleReject = async () => {
        if (!selectedSubmission) return;
        
        if (!rejectReason.trim()) {
            alert('Please provide a reason for rejection');
            return;
        }

        setActionLoading(true);
        try {
            const csrfToken = Cookies.get('csrftoken');
            const response = await fetch(`http://localhost:8888/api/admin/submissions/${selectedSubmission.id}/reject/`, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ reason: rejectReason }),
            });

            if (!response.ok) {
                throw new Error('Failed to reject submission');
            }

            // Update local state
            setSubmissions(prevSubmissions => 
                prevSubmissions.map(submission => 
                    submission.id === selectedSubmission.id 
                        ? { ...submission, status: 'rejected', reject_reason: rejectReason } 
                        : submission
                )
            );

            setShowRejectModal(false);
            alert('Submission rejected successfully!');
        } catch (error) {
            console.error('Error rejecting submission:', error);
            alert('Failed to reject submission. Please try again.');
        } finally {
            setActionLoading(false);
            setShowRejectModal(false);
        }
    };

    const fetchUsers = async () => {
        try {
            const csrfToken = Cookies.get('csrftoken');
            const response = await fetch('http://localhost:8888/api/admin/users/', {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
            });

            if (response.ok) {
                const data = await response.json();
                setUsers(data);
            }
        } catch (error) {
            console.error('Error fetching users:', error);
        }
    };

    const fetchChallenges = async () => {
        try {
            const csrfToken = Cookies.get('csrftoken');
            const response = await fetch('http://localhost:8888/api/admin/challenges/', {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
            });

            if (response.ok) {
                const data = await response.json();
                setChallenges(data);
            }
        } catch (error) {
            console.error('Error fetching challenges:', error);
        }
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

    const validateTimeFormat = (timeString) => {
        const timePattern = /^\d{2}:\d{2}:\d{2}$/;
        return timePattern.test(timeString);
    };

    return (
        <div className="admin-container">
            <div className="admin-header">
                <h1>Submission Management</h1>
                <span className="admin-badge">Admin</span>
            </div>

            <div className="admin-nav">
                <Link to="/admin" className="admin-nav-item">Dashboard</Link>
                <Link to="/admin/submissions" className="admin-nav-item active">Submissions</Link>
                <Link to="/admin/challenges" className="admin-nav-item">Challenges</Link>
                <Link to="/admin/users" className="admin-nav-item">Users</Link>
                <Link to="/admin/settings" className="admin-nav-item">Settings</Link>
            </div>

            <div className="admin-content">
                <div style={{ marginBottom: '20px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
                        <h2 style={{ color: '#a98b2d', margin: 0 }}>Challenge Submissions</h2>
                    </div>
                    
                    <div className="admin-filters">
                        <div className="admin-filter-group">
                            <label>Status:</label>
                            <select 
                                value={statusFilter}
                                onChange={(e) => setStatusFilter(e.target.value)}
                                className="admin-form-select"
                            >
                                <option value="all">All Submissions</option>
                                <option value="pending">Pending</option>
                                <option value="approved">Approved</option>
                                <option value="rejected">Rejected</option>
                            </select>
                        </div>
                        
                        <div className="admin-filter-group">
                            <label>User:</label>
                            <select 
                                value={userFilter}
                                onChange={(e) => setUserFilter(e.target.value)}
                                className="admin-form-select"
                            >
                                <option value="">All Users</option>
                                {users.map(user => (
                                    <option key={user.id} value={user.id}>{user.username}</option>
                                ))}
                            </select>
                        </div>
                        
                        <div className="admin-filter-group">
                            <label>Challenge:</label>
                            <select 
                                value={challengeFilter}
                                onChange={(e) => setChallengeFilter(e.target.value)}
                                className="admin-form-select"
                            >
                                <option value="">All Challenges</option>
                                {challenges.map(challenge => (
                                    <option key={challenge.id} value={challenge.id}>{challenge.name}</option>
                                ))}
                            </select>
                        </div>
                        
                        {(statusFilter !== 'all' || userFilter || challengeFilter) && (
                            <button 
                                className="admin-button secondary"
                                onClick={() => {
                                    setStatusFilter('all');
                                    setUserFilter('');
                                    setChallengeFilter('');
                                }}
                                style={{ marginLeft: '10px' }}
                            >
                                Clear Filters
                            </button>
                        )}
                    </div>
                </div>
                
                {loading ? (
                    <div className="admin-loading">
                        <LoadingSpinner />
                    </div>
                ) : submissions.length === 0 ? (
                    <div style={{ textAlign: 'center', padding: '50px 0', color: '#909090' }}>
                        <h3 style={{ color: '#a98b2d' }}>No Submissions Found</h3>
                        <p>There are no submissions matching the selected filter.</p>
                    </div>
                ) : (
                    <div className="admin-table-container">
                        <table className="admin-table">
                            <thead>
                                <tr>
                                    <th>User</th>
                                    <th>Challenge</th>
                                    <th>User Time</th>
                                    <th>Admin Time</th>
                                    <th>Points</th>
                                    <th>Submitted</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {submissions.map(submission => (
                                    <tr key={submission.id}>
                                        <td>
                                            <span className="username-display">{submission.username}</span>
                                        </td>
                                        <td>
                                            <div>
                                                <span className="challenge-name">{submission.challenge_name}</span>
                                                <span className={`difficulty-badge ${submission.challenge_difficulty.toLowerCase()}`}>
                                                    {submission.challenge_difficulty}
                                                </span>
                                            </div>
                                        </td>
                                        <td>
                                            <span className="time-display user-time">
                                                {submission.user_time}
                                            </span>
                                        </td>
                                        <td>
                                            <span className="time-display admin-time">
                                                {submission.admin_verified_time || '-'}
                                            </span>
                                        </td>
                                        <td>
                                            <span className="points-display">
                                                {submission.status === 'approved' ? submission.points_awarded : submission.challenge_points}
                                                {submission.status !== 'approved' && <small> (potential)</small>}
                                            </span>
                                        </td>
                                        <td>{formatDate(submission.submitted_at)}</td>
                                        <td>{getStatusBadge(submission.status)}</td>
                                        <td>
                                            <div className="admin-action-buttons">
                                                <a 
                                                    href={submission.file_url} 
                                                    target="_blank" 
                                                    rel="noopener noreferrer"
                                                    className="admin-action-button view"
                                                >
                                                    View Run
                                                </a>
                                                
                                                {submission.status === 'pending' && (
                                                    <>
                                                        <button 
                                                            onClick={() => openApproveModal(submission)}
                                                            className="admin-action-button approve"
                                                            disabled={actionLoading}
                                                        >
                                                            Approve
                                                        </button>
                                                        <button 
                                                            onClick={() => openRejectModal(submission)}
                                                            className="admin-action-button reject"
                                                            disabled={actionLoading}
                                                        >
                                                            Reject
                                                        </button>
                                                    </>
                                                )}
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>

            {/* Approve Modal with Time Override */}
            {showApproveModal && (
                <div className="admin-modal-overlay" onClick={() => !actionLoading && setShowApproveModal(false)}>
                    <div className="admin-modal" onClick={(e) => e.stopPropagation()}>
                        <div className="admin-modal-header">
                            <h3 className="admin-modal-title">Approve Submission</h3>
                            <button 
                                className="admin-modal-close" 
                                onClick={() => !actionLoading && setShowApproveModal(false)}
                                disabled={actionLoading}
                            >
                                ×
                            </button>
                        </div>
                        <div className="admin-modal-body">
                            <p>You are about to approve the following submission:</p>
                            <p><strong>User:</strong> {selectedSubmission?.username}</p>
                            <p><strong>Challenge:</strong> {selectedSubmission?.challenge_name}</p>
                            <p><strong>User's Time:</strong> {selectedSubmission?.user_time}</p>
                            <p><strong>Points to Award:</strong> {selectedSubmission?.challenge_points}</p>
                            
                            <div className="admin-form-group">
                                <label className="admin-form-label">
                                    Admin Verified Time (Optional):
                                    <small style={{ display: 'block', color: '#909090', fontWeight: 'normal' }}>
                                        Override the user's time if needed (format: HH:MM:SS)
                                    </small>
                                </label>
                                <input 
                                    type="text"
                                    className="admin-form-input"
                                    value={adminVerifiedTime}
                                    onChange={(e) => setAdminVerifiedTime(e.target.value)}
                                    placeholder="HH:MM:SS (e.g., 01:30:45)"
                                    disabled={actionLoading}
                                />
                                {adminVerifiedTime && !validateTimeFormat(adminVerifiedTime) && (
                                    <small style={{ color: '#f44336', marginTop: '5px', display: 'block' }}>
                                        Invalid time format. Use HH:MM:SS
                                    </small>
                                )}
                            </div>
                        </div>
                        <div className="admin-modal-footer">
                            <button 
                                className="admin-button secondary"
                                onClick={() => !actionLoading && setShowApproveModal(false)}
                                disabled={actionLoading}
                            >
                                Cancel
                            </button>
                            <button 
                                className="admin-button"
                                onClick={() => handleApprove(selectedSubmission?.id, adminVerifiedTime)}
                                disabled={actionLoading || (adminVerifiedTime && !validateTimeFormat(adminVerifiedTime))}
                            >
                                {actionLoading ? 'Approving...' : 'Approve Submission'}
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Reject Modal */}
            {showRejectModal && (
                <div className="admin-modal-overlay" onClick={() => !actionLoading && setShowRejectModal(false)}>
                    <div className="admin-modal" onClick={(e) => e.stopPropagation()}>
                        <div className="admin-modal-header">
                            <h3 className="admin-modal-title">Reject Submission</h3>
                            <button 
                                className="admin-modal-close" 
                                onClick={() => !actionLoading && setShowRejectModal(false)}
                                disabled={actionLoading}
                            >
                                ×
                            </button>
                        </div>
                        <div className="admin-modal-body">
                            <p>You are about to reject the following submission:</p>
                            <p><strong>User:</strong> {selectedSubmission?.username}</p>
                            <p><strong>Challenge:</strong> {selectedSubmission?.challenge_name}</p>
                            
                            <div className="admin-form-group">
                                <label className="admin-form-label">Reason for Rejection:</label>
                                <textarea 
                                    className="admin-form-textarea"
                                    value={rejectReason}
                                    onChange={(e) => setRejectReason(e.target.value)}
                                    placeholder="Provide a reason for rejecting this submission..."
                                    required
                                    disabled={actionLoading}
                                />
                            </div>
                        </div>
                        <div className="admin-modal-footer">
                            <button 
                                className="admin-button secondary"
                                onClick={() => !actionLoading && setShowRejectModal(false)}
                                disabled={actionLoading}
                            >
                                Cancel
                            </button>
                            <button 
                                className="admin-button danger"
                                onClick={handleReject}
                                disabled={actionLoading}
                            >
                                {actionLoading ? 'Rejecting...' : 'Reject Submission'}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default AdminSubmissions;