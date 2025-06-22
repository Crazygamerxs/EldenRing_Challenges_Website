import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Cookies from 'js-cookie';
import './Admin.css';
import LoadingSpinner from '../common/LoadingSpinner';

import { API_ENDPOINTS } from '../../utils/api';
const AdminChallenges = () => {
    const [challenges, setChallenges] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('all');
    const [searchTerm, setSearchTerm] = useState('');
    const [showAddModal, setShowAddModal] = useState(false);
    const [showEditModal, setShowEditModal] = useState(false);
    const [selectedChallenge, setSelectedChallenge] = useState(null);
    const [formData, setFormData] = useState({
        name: '',
        details: '',
        difficulty: 'Easy',
        category: ''
    });
    const [categories, setCategories] = useState([]);
    const [actionLoading, setActionLoading] = useState(false);

    useEffect(() => {
        fetchChallenges();
        fetchCategories();
    }, [filter]);

    const fetchChallenges = async () => {
        setLoading(true);
        try {
            const endpoint = filter !== 'all' ? `${API_ENDPOINTS.ADMIN_CHALLENGES}?category=${filter}` : API_ENDPOINTS.ADMIN_CHALLENGES;
            
            const response = await fetch(endpoint, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                console.error('Failed to fetch challenges:', response.status);
                throw new Error(`Failed to fetch challenges: ${response.status}`);
            }

            const data = await response.json();
            console.log('Challenges fetched successfully:', data);
            setChallenges(data);
        } catch (error) {
            console.error('Error fetching challenges:', error);
            // Show error state instead of mock data
            setChallenges([]);
        } finally {
            setLoading(false);
        }
    };

    const fetchCategories = async () => {
        try {
            const response = await fetch(API_ENDPOINTS.ADMIN_CATEGORIES, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                console.error('Failed to fetch categories:', response.status);
                throw new Error(`Failed to fetch categories: ${response.status}`);
            }

            const data = await response.json();
            console.log('Categories fetched successfully:', data);
            setCategories(data);
        } catch (error) {
            console.error('Error fetching categories:', error);
            // Show error state instead of mock data
            setCategories([]);
        }
    };

    const handleAddChallenge = async () => {
        if (!formData.name || !formData.details || !formData.category) {
            alert('Please fill in all required fields');
            return;
        }

        setActionLoading(true);
        try {
            const csrfToken = Cookies.get('csrftoken');
            const response = await fetch(API_ENDPOINTS.ADMIN_CHALLENGES, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                throw new Error('Failed to add challenge');
            }

            const newChallenge = await response.json();
            setChallenges(prevChallenges => [...prevChallenges, newChallenge]);
            setShowAddModal(false);
            resetForm();
            alert('Challenge added successfully!');
        } catch (error) {
            console.error('Error adding challenge:', error);
            alert('Failed to add challenge. Please try again.');
            
            // For demo, add a mock challenge anyway
            const mockChallenge = {
                id: Math.max(...challenges.map(c => c.id)) + 1,
                name: formData.name,
                details: formData.details,
                difficulty: formData.difficulty,
                category: categories.find(c => c.id === parseInt(formData.category))?.name || 'Unknown Category'
            };
            setChallenges(prevChallenges => [...prevChallenges, mockChallenge]);
            setShowAddModal(false);
            resetForm();
        } finally {
            setActionLoading(false);
        }
    };

    const handleEditChallenge = async () => {
        if (!formData.name || !formData.details || !formData.category) {
            alert('Please fill in all required fields');
            return;
        }

        setActionLoading(true);
        try {
            const csrfToken = Cookies.get('csrftoken');
            const response = await fetch(`API_ENDPOINTS.ADMIN_CHALLENGE_DETAIL(selectedChallenge.id)`, {
                method: 'PUT',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                throw new Error('Failed to update challenge');
            }

            const updatedChallenge = await response.json();
            setChallenges(prevChallenges => 
                prevChallenges.map(challenge => 
                    challenge.id === selectedChallenge.id ? updatedChallenge : challenge
                )
            );
            setShowEditModal(false);
            resetForm();
            alert('Challenge updated successfully!');
        } catch (error) {
            console.error('Error updating challenge:', error);
            alert('Failed to update challenge. Please try again.');
            
            // For demo, update the challenge anyway
            setChallenges(prevChallenges => 
                prevChallenges.map(challenge => 
                    challenge.id === selectedChallenge.id 
                        ? {
                            ...challenge,
                            name: formData.name,
                            details: formData.details,
                            difficulty: formData.difficulty,
                            category: categories.find(c => c.id === parseInt(formData.category))?.name || 'Unknown Category'
                        } 
                        : challenge
                )
            );
            setShowEditModal(false);
            resetForm();
        } finally {
            setActionLoading(false);
        }
    };

    const handleDeleteChallenge = async (challengeId) => {
        if (!window.confirm('Are you sure you want to delete this challenge?')) {
            return;
        }

        setActionLoading(true);
        try {
            const csrfToken = Cookies.get('csrftoken');
            const response = await fetch(`API_ENDPOINTS.ADMIN_CHALLENGE_DETAIL(challengeId)`, {
                method: 'DELETE',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
            });

            if (!response.ok) {
                throw new Error('Failed to delete challenge');
            }

            setChallenges(prevChallenges => 
                prevChallenges.filter(challenge => challenge.id !== challengeId)
            );
            alert('Challenge deleted successfully!');
        } catch (error) {
            console.error('Error deleting challenge:', error);
            alert('Failed to delete challenge. Please try again.');
            
            // For demo, remove the challenge anyway
            setChallenges(prevChallenges => 
                prevChallenges.filter(challenge => challenge.id !== challengeId)
            );
        } finally {
            setActionLoading(false);
        }
    };

    const openEditModal = (challenge) => {
        setSelectedChallenge(challenge);
        setFormData({
            name: challenge.name,
            details: challenge.details,
            difficulty: challenge.difficulty,
            category: categories.find(c => c.name === challenge.category)?.id.toString() || ''
        });
        setShowEditModal(true);
    };

    const resetForm = () => {
        setFormData({
            name: '',
            details: '',
            difficulty: 'Easy',
            category: ''
        });
        setSelectedChallenge(null);
    };

    // Mock data generator for demonstration purposes
    const generateMockChallenges = (filterCategory) => {
        const allChallenges = [
            {
                id: 1,
                name: 'No Hit Run',
                details: 'Complete the game without taking any damage.',
                difficulty: 'Hard',
                category: 'Challenges for the Brave or Insane'
            },
            {
                id: 2,
                name: 'Level 1 Weapon Only',
                details: 'Complete the game using only unupgraded weapons.',
                difficulty: 'Medium',
                category: 'Basic Weaponry Challenges'
            },
            {
                id: 3,
                name: 'No Armor Run',
                details: 'Complete the game without wearing any armor.',
                difficulty: 'Easy',
                category: 'General Challenges'
            },
            {
                id: 4,
                name: 'Fists Only',
                details: 'Complete the game using only your fists.',
                difficulty: 'Hard',
                category: 'Basic Weaponry Challenges'
            },
            {
                id: 5,
                name: 'No Healing',
                details: 'Complete the game without using any healing items or spells.',
                difficulty: 'Hard',
                category: 'Healing and FP Recovery Challenges'
            },
            {
                id: 6,
                name: 'No Damage',
                details: 'Complete the game without taking any damage.',
                difficulty: 'Hard',
                category: 'Challenges for the Brave or Insane'
            },
            {
                id: 7,
                name: 'No Rolling',
                details: 'Complete the game without using the roll or dodge mechanic.',
                difficulty: 'Medium',
                category: 'General Challenges'
            }
        ];

        if (filterCategory === 'all') {
            return allChallenges;
        }
        
        return allChallenges.filter(challenge => challenge.category === filterCategory);
    };

    // Filter challenges based on search term
    const filteredChallenges = challenges.filter(challenge => 
        challenge.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        challenge.details.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="admin-container">
            <div className="admin-header">
                <h1>Challenge Management</h1>
                <span className="admin-badge">Admin</span>
            </div>

            <div className="admin-nav">
                <Link to="/admin" className="admin-nav-item">Dashboard</Link>
                <Link to="/admin/submissions" className="admin-nav-item">Submissions</Link>
                <Link to="/admin/challenges" className="admin-nav-item active">Challenges</Link>
                <Link to="/admin/users" className="admin-nav-item">Users</Link>
                <Link to="/admin/settings" className="admin-nav-item">Settings</Link>
            </div>

            <div className="admin-content">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                    <h2 style={{ color: '#a98b2d', margin: 0 }}>Challenge List</h2>
                    
                    <div>
                        <button 
                            className="admin-button"
                            onClick={() => {
                                resetForm();
                                setShowAddModal(true);
                            }}
                        >
                            Add New Challenge
                        </button>
                    </div>
                </div>
                
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                    <div style={{ display: 'flex', alignItems: 'center' }}>
                        <input 
                            type="text"
                            placeholder="Search challenges..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="admin-form-input"
                            style={{ width: '300px', marginRight: '10px' }}
                        />
                    </div>
                    
                    <div>
                        <select 
                            value={filter}
                            onChange={(e) => setFilter(e.target.value)}
                            className="admin-form-select"
                            style={{ width: 'auto', marginLeft: '10px' }}
                        >
                            <option value="all">All Categories</option>
                            {categories.map(category => (
                                <option key={category.id} value={category.name}>
                                    {category.name}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>
                
                {loading ? (
                    <div className="admin-loading">
                        <LoadingSpinner />
                    </div>
                ) : filteredChallenges.length === 0 ? (
                    <div style={{ textAlign: 'center', padding: '50px 0', color: '#909090' }}>
                        <h3 style={{ color: '#a98b2d' }}>No Challenges Found</h3>
                        <p>There are no challenges matching your search criteria.</p>
                    </div>
                ) : (
                    <div className="admin-table-container">
                        <table className="admin-table">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Category</th>
                                    <th>Difficulty</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredChallenges.map(challenge => (
                                    <tr key={challenge.id}>
                                        <td>{challenge.name}</td>
                                        <td>{challenge.category}</td>
                                        <td>{challenge.difficulty}</td>
                                        <td>
                                            <div className="admin-action-buttons">
                                                <button 
                                                    onClick={() => openEditModal(challenge)}
                                                    className="admin-action-button view"
                                                    disabled={actionLoading}
                                                >
                                                    Edit
                                                </button>
                                                <button 
                                                    onClick={() => handleDeleteChallenge(challenge.id)}
                                                    className="admin-action-button reject"
                                                    disabled={actionLoading}
                                                >
                                                    Delete
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

            {/* Add Challenge Modal */}
            {showAddModal && (
                <div className="admin-modal-overlay" onClick={() => !actionLoading && setShowAddModal(false)}>
                    <div className="admin-modal" onClick={(e) => e.stopPropagation()}>
                        <div className="admin-modal-header">
                            <h3 className="admin-modal-title">Add New Challenge</h3>
                            <button 
                                className="admin-modal-close" 
                                onClick={() => !actionLoading && setShowAddModal(false)}
                                disabled={actionLoading}
                            >
                                ×
                            </button>
                        </div>
                        <div className="admin-modal-body">
                            <div className="admin-form-group">
                                <label className="admin-form-label">Challenge Name:</label>
                                <input 
                                    type="text"
                                    className="admin-form-input"
                                    value={formData.name}
                                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                                    placeholder="Enter challenge name"
                                    required
                                    disabled={actionLoading}
                                />
                            </div>
                            
                            <div className="admin-form-group">
                                <label className="admin-form-label">Description:</label>
                                <textarea 
                                    className="admin-form-textarea"
                                    value={formData.details}
                                    onChange={(e) => setFormData({...formData, details: e.target.value})}
                                    placeholder="Enter challenge description"
                                    required
                                    disabled={actionLoading}
                                />
                            </div>
                            
                            <div className="admin-form-group">
                                <label className="admin-form-label">Difficulty:</label>
                                <select 
                                    className="admin-form-select"
                                    value={formData.difficulty}
                                    onChange={(e) => setFormData({...formData, difficulty: e.target.value})}
                                    required
                                    disabled={actionLoading}
                                >
                                    <option value="Easy">Easy</option>
                                    <option value="Medium">Medium</option>
                                    <option value="Hard">Hard</option>
                                </select>
                            </div>
                            
                            <div className="admin-form-group">
                                <label className="admin-form-label">Category:</label>
                                <select 
                                    className="admin-form-select"
                                    value={formData.category}
                                    onChange={(e) => setFormData({...formData, category: e.target.value})}
                                    required
                                    disabled={actionLoading}
                                >
                                    <option value="">Select a category</option>
                                    {categories.map(category => (
                                        <option key={category.id} value={category.id}>
                                            {category.name}
                                        </option>
                                    ))}
                                </select>
                            </div>
                        </div>
                        <div className="admin-modal-footer">
                            <button 
                                className="admin-button secondary"
                                onClick={() => !actionLoading && setShowAddModal(false)}
                                disabled={actionLoading}
                            >
                                Cancel
                            </button>
                            <button 
                                className="admin-button"
                                onClick={handleAddChallenge}
                                disabled={actionLoading}
                            >
                                {actionLoading ? 'Adding...' : 'Add Challenge'}
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Edit Challenge Modal */}
            {showEditModal && (
                <div className="admin-modal-overlay" onClick={() => !actionLoading && setShowEditModal(false)}>
                    <div className="admin-modal" onClick={(e) => e.stopPropagation()}>
                        <div className="admin-modal-header">
                            <h3 className="admin-modal-title">Edit Challenge</h3>
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
                                <label className="admin-form-label">Challenge Name:</label>
                                <input 
                                    type="text"
                                    className="admin-form-input"
                                    value={formData.name}
                                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                                    placeholder="Enter challenge name"
                                    required
                                    disabled={actionLoading}
                                />
                            </div>
                            
                            <div className="admin-form-group">
                                <label className="admin-form-label">Description:</label>
                                <textarea 
                                    className="admin-form-textarea"
                                    value={formData.details}
                                    onChange={(e) => setFormData({...formData, details: e.target.value})}
                                    placeholder="Enter challenge description"
                                    required
                                    disabled={actionLoading}
                                />
                            </div>
                            
                            <div className="admin-form-group">
                                <label className="admin-form-label">Difficulty:</label>
                                <select 
                                    className="admin-form-select"
                                    value={formData.difficulty}
                                    onChange={(e) => setFormData({...formData, difficulty: e.target.value})}
                                    required
                                    disabled={actionLoading}
                                >
                                    <option value="Easy">Easy</option>
                                    <option value="Medium">Medium</option>
                                    <option value="Hard">Hard</option>
                                </select>
                            </div>
                            
                            <div className="admin-form-group">
                                <label className="admin-form-label">Category:</label>
                                <select 
                                    className="admin-form-select"
                                    value={formData.category}
                                    onChange={(e) => setFormData({...formData, category: e.target.value})}
                                    required
                                    disabled={actionLoading}
                                >
                                    <option value="">Select a category</option>
                                    {categories.map(category => (
                                        <option key={category.id} value={category.id}>
                                            {category.name}
                                        </option>
                                    ))}
                                </select>
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
                                onClick={handleEditChallenge}
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

export default AdminChallenges;
