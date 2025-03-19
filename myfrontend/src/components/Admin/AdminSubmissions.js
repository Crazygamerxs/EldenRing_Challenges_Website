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
    const [showModal, setShowModal] = useState(false);
    const [rejectReason, setRejectReason] = useState('');
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
            // Use mock data for demonstration
            setSubmissions(generateMockSubmissions(statusFilter, userFilter, challengeFilter));
        } finally {
            setLoading(false);
        }
    };

    const handleApprove = async (submissionId) => {
        setActionLoading(true);
        try {
            const csrfToken = Cookies.get('csrftoken');
            const response = await fetch(`http://localhost:8888/api/admin/submissions/${submissionId}/approve/`, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Failed to approve submission');
            }

            // Update local state
            setSubmissions(prevSubmissions => 
                prevSubmissions.map(submission => 
                    submission.id === submissionId 
                        ? { ...submission, status: 'approved' } 
                        : submission
                )
            );

            // Show success message
            alert('Submission approved successfully!');
        } catch (error) {
            console.error('Error approving submission:', error);
            alert('Failed to approve submission. Please try again.');
            
            // For demo, update the UI anyway
            setSubmissions(prevSubmissions => 
                prevSubmissions.map(submission => 
                    submission.id === submissionId 
                        ? { ...submission, status: 'approved' } 
                        : submission
                )
            );
        } finally {
            setActionLoading(false);
        }
    };

    const openRejectModal = (submission) => {
        setSelectedSubmission(submission);
        setRejectReason('');
        setShowModal(true);
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
                        ? { ...submission, status: 'rejected' } 
                        : submission
                )
            );

            // Close modal and show success message
            setShowModal(false);
            alert('Submission rejected successfully!');
        } catch (error) {
            console.error('Error rejecting submission:', error);
            alert('Failed to reject submission. Please try again.');
            
            // For demo, update the UI anyway
            setSubmissions(prevSubmissions => 
                prevSubmissions.map(submission => 
                    submission.id === selectedSubmission.id 
                        ? { ...submission, status: 'rejected' } 
                        : submission
                )
            );
        } finally {
            setActionLoading(false);
            setShowModal(false);
        }
    };

    // Functions to fetch users and challenges for filtering
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

            if (!response.ok) {
                throw new Error('Failed to fetch users');
            }

            const data = await response.json();
            setUsers(data);
        } catch (error) {
            console.error('Error fetching users:', error);
            // Use mock data for demonstration
            setUsers(generateMockUsers());
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

            if (!response.ok) {
                throw new Error('Failed to fetch challenges');
            }

            const data = await response.json();
            setChallenges(data);
        } catch (error) {
            console.error('Error fetching challenges:', error);
            // Use mock data for demonstration
            setChallenges(generateMockChallenges());
        }
    };

    // Mock data generators for demonstration purposes
    const generateMockUsers = () => {
        return [
            { id: 1, username: 'TarnishedOne' },
            { id: 2, username: 'EldenLord' },
            { id: 3, username: 'MaidenlessRun' },
            { id: 4, username: 'LetMeSoloHer' },
            { id: 5, username: 'RingBearer' },
            { id: 6, username: 'BleedBuilder' },
            { id: 7, username: 'UngaBunga' }
        ];
    };

    const generateMockChallenges = () => {
        return [
            { id: 1, name: 'No Hit Run' },
            { id: 2, name: 'Level 1 Weapon Only' },
            { id: 3, name: 'No Armor Run' },
            { id: 4, name: 'Fists Only' },
            { id: 5, name: 'No Healing' },
            { id: 6, name: 'No Damage' },
            { id: 7, name: 'No Rolling' }
        ];
    };

    const generateMockSubmissions = (statusFilter, userFilter, challengeFilter) => {
        let allSubmissions = [
            {
                id: 1,
                username: 'TarnishedOne',
                challenge_name: 'No Hit Run',
                challenge_id: 1,
                file_url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                submitted_at: new Date(Date.now() - 1000 * 60 * 30).toISOString(), // 30 minutes ago
                status: 'pending',
                time_taken: '01:45:30'
            },
            {
                id: 2,
                username: 'EldenLord',
                challenge_name: 'Level 1 Weapon Only',
                challenge_id: 2,
                file_url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                submitted_at: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(), // 2 hours ago
                status: 'approved',
                time_taken: '02:15:10'
            },
            {
                id: 3,
                username: 'MaidenlessRun',
                challenge_name: 'No Armor Run',
                challenge_id: 3,
                file_url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                submitted_at: new Date(Date.now() - 1000 * 60 * 60 * 5).toISOString(), // 5 hours ago
                status: 'rejected',
                time_taken: '01:30:45',
                reject_reason: 'Video does not show the entire run'
            },
            {
                id: 4,
                username: 'LetMeSoloHer',
                challenge_name: 'Fists Only',
                challenge_id: 4,
                file_url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                submitted_at: new Date(Date.now() - 1000 * 60 * 60 * 8).toISOString(), // 8 hours ago
                status: 'pending',
                time_taken: '03:20:15'
            },
            {
                id: 5,
                username: 'RingBearer',
                challenge_name: 'No Healing',
                challenge_id: 5,
                file_url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                submitted_at: new Date(Date.now() - 1000 * 60 * 60 * 12).toISOString(), // 12 hours ago
                status: 'pending',
                time_taken: '02:45:30'
            },
            {
                id: 6,
                username: 'BleedBuilder',
                challenge_name: 'No Damage',
                challenge_id: 6,
                file_url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                submitted_at: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(), // 1 day ago
                status: 'approved',
                time_taken: '01:55:20'
            },
            {
                id: 7,
                username: 'UngaBunga',
                challenge_name: 'No Rolling',
                challenge_id: 7,
                file_url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                submitted_at: new Date(Date.now() - 1000 * 60 * 60 * 36).toISOString(), // 1.5 days ago
                status: 'rejected',
                time_taken: '02:10:45',
                reject_reason: 'Player rolled multiple times during the run'
            }
        ];

        // Apply status filter
        if (statusFilter !== 'all') {
            allSubmissions = allSubmissions.filter(submission => submission.status === statusFilter);
        }
        
        // Apply user filter
        if (userFilter) {
            const userId = parseInt(userFilter);
            allSubmissions = allSubmissions.filter(submission => {
                // For mock data, we'll match by username since we don't have user IDs in the mock data
                if (userId === 1) return submission.username === 'TarnishedOne';
                if (userId === 2) return submission.username === 'EldenLord';
                if (userId === 3) return submission.username === 'MaidenlessRun';
                if (userId === 4) return submission.username === 'LetMeSoloHer';
                if (userId === 5) return submission.username === 'RingBearer';
                if (userId === 6) return submission.username === 'BleedBuilder';
                if (userId === 7) return submission.username === 'UngaBunga';
                return false;
            });
        }
        
        // Apply challenge filter
        if (challengeFilter) {
            const challengeId = parseInt(challengeFilter);
            allSubmissions = allSubmissions.filter(submission => submission.challenge_id === challengeId);
        }
        
        return allSubmissions;
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
                                    <th>Time Taken</th>
                                    <th>Submitted</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {submissions.map(submission => (
                                    <tr key={submission.id}>
                                        <td>{submission.username}</td>
                                        <td>{submission.challenge_name}</td>
                                        <td>{submission.time_taken}</td>
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
                                                            onClick={() => handleApprove(submission.id)}
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

            {/* Reject Modal */}
            {showModal && (
                <div className="admin-modal-overlay" onClick={() => !actionLoading && setShowModal(false)}>
                    <div className="admin-modal" onClick={(e) => e.stopPropagation()}>
                        <div className="admin-modal-header">
                            <h3 className="admin-modal-title">Reject Submission</h3>
                            <button 
                                className="admin-modal-close" 
                                onClick={() => !actionLoading && setShowModal(false)}
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
                                onClick={() => !actionLoading && setShowModal(false)}
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
