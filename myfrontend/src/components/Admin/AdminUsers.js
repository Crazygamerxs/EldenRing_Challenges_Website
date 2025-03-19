import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Cookies from 'js-cookie';
import './Admin.css';
import LoadingSpinner from '../common/LoadingSpinner';

const AdminUsers = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [showEditModal, setShowEditModal] = useState(false);
    const [selectedUser, setSelectedUser] = useState(null);
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        is_active: true,
        is_staff: false
    });
    const [actionLoading, setActionLoading] = useState(false);

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        setLoading(true);
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
        } finally {
            setLoading(false);
        }
    };

    const handleEditUser = async () => {
        if (!formData.username || !formData.email) {
            alert('Please fill in all required fields');
            return;
        }

        setActionLoading(true);
        try {
            const csrfToken = Cookies.get('csrftoken');
            const response = await fetch(`http://localhost:8888/api/admin/users/${selectedUser.id}/`, {
                method: 'PUT',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                throw new Error('Failed to update user');
            }

            const updatedUser = await response.json();
            setUsers(prevUsers => 
                prevUsers.map(user => 
                    user.id === selectedUser.id ? updatedUser : user
                )
            );
            setShowEditModal(false);
            alert('User updated successfully!');
        } catch (error) {
            console.error('Error updating user:', error);
            alert('Failed to update user. Please try again.');
            
            // For demo, update the user anyway
            setUsers(prevUsers => 
                prevUsers.map(user => 
                    user.id === selectedUser.id 
                        ? {
                            ...user,
                            username: formData.username,
                            email: formData.email,
                            is_active: formData.is_active,
                            is_staff: formData.is_staff
                        } 
                        : user
                )
            );
            setShowEditModal(false);
        } finally {
            setActionLoading(false);
        }
    };

    const handleDeactivateUser = async (userId, currentStatus) => {
        const newStatus = !currentStatus;
        const confirmMessage = newStatus 
            ? 'Are you sure you want to activate this user?' 
            : 'Are you sure you want to deactivate this user?';
        
        if (!window.confirm(confirmMessage)) {
            return;
        }

        setActionLoading(true);
        try {
            const csrfToken = Cookies.get('csrftoken');
            const response = await fetch(`http://localhost:8888/api/admin/users/${userId}/status/`, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ is_active: newStatus }),
            });

            if (!response.ok) {
                throw new Error('Failed to update user status');
            }

            setUsers(prevUsers => 
                prevUsers.map(user => 
                    user.id === userId 
                        ? { ...user, is_active: newStatus } 
                        : user
                )
            );
            
            alert(`User ${newStatus ? 'activated' : 'deactivated'} successfully!`);
        } catch (error) {
            console.error('Error updating user status:', error);
            alert('Failed to update user status. Please try again.');
            
            // For demo, update the user status anyway
            setUsers(prevUsers => 
                prevUsers.map(user => 
                    user.id === userId 
                        ? { ...user, is_active: newStatus } 
                        : user
                )
            );
        } finally {
            setActionLoading(false);
        }
    };

    const openEditModal = (user) => {
        setSelectedUser(user);
        setFormData({
            username: user.username,
            email: user.email,
            is_active: user.is_active,
            is_staff: user.is_staff
        });
        setShowEditModal(true);
    };

    // Mock data generator for demonstration purposes
    const generateMockUsers = () => {
        return [
            {
                id: 1,
                username: 'admin',
                email: 'admin@eldenring.com',
                profile_image: '/static/main/images/profile_pic/pp_1.png',
                date_joined: new Date(Date.now() - 1000 * 60 * 60 * 24 * 30).toISOString(), // 30 days ago
                is_active: true,
                is_staff: true,
                completed_challenges: 15
            },
            {
                id: 2,
                username: 'TarnishedOne',
                email: 'tarnished@example.com',
                profile_image: '/static/main/images/profile_pic/pp_2.png',
                date_joined: new Date(Date.now() - 1000 * 60 * 60 * 24 * 25).toISOString(), // 25 days ago
                is_active: true,
                is_staff: false,
                completed_challenges: 12
            },
            {
                id: 3,
                username: 'EldenLord',
                email: 'eldenlord@example.com',
                profile_image: '/static/main/images/profile_pic/pp_3.png',
                date_joined: new Date(Date.now() - 1000 * 60 * 60 * 24 * 20).toISOString(), // 20 days ago
                is_active: true,
                is_staff: false,
                completed_challenges: 8
            },
            {
                id: 4,
                username: 'MaidenlessRun',
                email: 'maidenless@example.com',
                profile_image: '/static/main/images/profile_pic/pp_1.png',
                date_joined: new Date(Date.now() - 1000 * 60 * 60 * 24 * 15).toISOString(), // 15 days ago
                is_active: false,
                is_staff: false,
                completed_challenges: 5
            },
            {
                id: 5,
                username: 'LetMeSoloHer',
                email: 'letmesolo@example.com',
                profile_image: '/static/main/images/profile_pic/pp_2.png',
                date_joined: new Date(Date.now() - 1000 * 60 * 60 * 24 * 10).toISOString(), // 10 days ago
                is_active: true,
                is_staff: false,
                completed_challenges: 10
            }
        ];
    };

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    };

    // Filter users based on search term
    const filteredUsers = users.filter(user => 
        user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.email.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="admin-container">
            <div className="admin-header">
                <h1>User Management</h1>
                <span className="admin-badge">Admin</span>
            </div>

            <div className="admin-nav">
                <Link to="/admin" className="admin-nav-item">Dashboard</Link>
                <Link to="/admin/submissions" className="admin-nav-item">Submissions</Link>
                <Link to="/admin/challenges" className="admin-nav-item">Challenges</Link>
                <Link to="/admin/users" className="admin-nav-item active">Users</Link>
                <Link to="/admin/settings" className="admin-nav-item">Settings</Link>
            </div>

            <div className="admin-content">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                    <h2 style={{ color: '#a98b2d', margin: 0 }}>User List</h2>
                    
                    <div>
                        <input 
                            type="text"
                            placeholder="Search users..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="admin-form-input"
                            style={{ width: '300px' }}
                        />
                    </div>
                </div>
                
                {loading ? (
                    <div className="admin-loading">
                        <LoadingSpinner />
                    </div>
                ) : filteredUsers.length === 0 ? (
                    <div style={{ textAlign: 'center', padding: '50px 0', color: '#909090' }}>
                        <h3 style={{ color: '#a98b2d' }}>No Users Found</h3>
                        <p>There are no users matching your search criteria.</p>
                    </div>
                ) : (
                    <div className="admin-table-container">
                        <table className="admin-table">
                            <thead>
                                <tr>
                                    <th>Username</th>
                                    <th>Email</th>
                                    <th>Joined</th>
                                    <th>Challenges</th>
                                    <th>Status</th>
                                    <th>Role</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredUsers.map(user => (
                                    <tr key={user.id}>
                                        <td>
                                            <div className="player-cell">
                                                <img 
                                                    src={user.profile_image} 
                                                    alt={user.username} 
                                                    className="player-avatar"
                                                    onError={(e) => {
                                                        e.target.onerror = null;
                                                        e.target.src = '/static/main/images/profile_pic/pp_1.png';
                                                    }}
                                                />
                                                <span className="player-name">{user.username}</span>
                                            </div>
                                        </td>
                                        <td>{user.email}</td>
                                        <td>{formatDate(user.date_joined)}</td>
                                        <td>{user.completed_challenges}</td>
                                        <td>
                                            <span className={`admin-status ${user.is_active ? 'approved' : 'rejected'}`}>
                                                {user.is_active ? 'Active' : 'Inactive'}
                                            </span>
                                        </td>
                                        <td>
                                            <span className={`admin-status ${user.is_staff ? 'pending' : ''}`}>
                                                {user.is_staff ? 'Admin' : 'User'}
                                            </span>
                                        </td>
                                        <td>
                                            <div className="admin-action-buttons">
                                                <button 
                                                    onClick={() => openEditModal(user)}
                                                    className="admin-action-button view"
                                                    disabled={actionLoading}
                                                >
                                                    Edit
                                                </button>
                                                <button 
                                                    onClick={() => handleDeactivateUser(user.id, user.is_active)}
                                                    className={`admin-action-button ${user.is_active ? 'reject' : 'approve'}`}
                                                    disabled={actionLoading}
                                                >
                                                    {user.is_active ? 'Deactivate' : 'Activate'}
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>

            {/* Edit User Modal */}
            {showEditModal && (
                <div className="admin-modal-overlay" onClick={() => !actionLoading && setShowEditModal(false)}>
                    <div className="admin-modal" onClick={(e) => e.stopPropagation()}>
                        <div className="admin-modal-header">
                            <h3 className="admin-modal-title">Edit User</h3>
                            <button 
                                className="admin-modal-close" 
                                onClick={() => !actionLoading && setShowEditModal(false)}
                                disabled={actionLoading}
                            >
                                ×
                            </button>
                        </div>
                        <div className="admin-modal-body">
                            <div className="admin-form-group">
                                <label className="admin-form-label">Username:</label>
                                <input 
                                    type="text"
                                    className="admin-form-input"
                                    value={formData.username}
                                    onChange={(e) => setFormData({...formData, username: e.target.value})}
                                    placeholder="Enter username"
                                    required
                                    disabled={actionLoading}
                                />
                            </div>
                            
                            <div className="admin-form-group">
                                <label className="admin-form-label">Email:</label>
                                <input 
                                    type="email"
                                    className="admin-form-input"
                                    value={formData.email}
                                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                                    placeholder="Enter email"
                                    required
                                    disabled={actionLoading}
                                />
                            </div>
                            
                            <div className="admin-form-group">
                                <label className="admin-form-label">Status:</label>
                                <div>
                                    <label style={{ marginRight: '20px' }}>
                                        <input 
                                            type="radio"
                                            name="is_active"
                                            checked={formData.is_active}
                                            onChange={() => setFormData({...formData, is_active: true})}
                                            disabled={actionLoading}
                                        /> Active
                                    </label>
                                    <label>
                                        <input 
                                            type="radio"
                                            name="is_active"
                                            checked={!formData.is_active}
                                            onChange={() => setFormData({...formData, is_active: false})}
                                            disabled={actionLoading}
                                        /> Inactive
                                    </label>
                                </div>
                            </div>
                            
                            <div className="admin-form-group">
                                <label className="admin-form-label">Role:</label>
                                <div>
                                    <label style={{ marginRight: '20px' }}>
                                        <input 
                                            type="radio"
                                            name="is_staff"
                                            checked={formData.is_staff}
                                            onChange={() => setFormData({...formData, is_staff: true})}
                                            disabled={actionLoading}
                                        /> Admin
                                    </label>
                                    <label>
                                        <input 
                                            type="radio"
                                            name="is_staff"
                                            checked={!formData.is_staff}
                                            onChange={() => setFormData({...formData, is_staff: false})}
                                            disabled={actionLoading}
                                        /> User
                                    </label>
                                </div>
                            </div>
                        </div>
                        <div className="admin-modal-footer">
                            <button 
                                className="admin-button secondary"
                                onClick={() => !actionLoading && setShowEditModal(false)}
                                disabled={actionLoading}
                            >
                                Cancel
                            </button>
                            <button 
                                className="admin-button"
                                onClick={handleEditUser}
                                disabled={actionLoading}
                            >
                                {actionLoading ? 'Saving...' : 'Save Changes'}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default AdminUsers;
