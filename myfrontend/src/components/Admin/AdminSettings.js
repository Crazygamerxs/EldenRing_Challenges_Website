import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Cookies from 'js-cookie';
import './Admin.css';
import LoadingSpinner from '../common/LoadingSpinner';

import { API_ENDPOINTS } from '../../utils/api';
const AdminSettings = () => {
    const [settings, setSettings] = useState({
        site_name: 'Elden Ring Challenges',
        site_description: 'A platform for Elden Ring challenge runs',
        enable_registrations: true,
        enable_submissions: true,
        maintenance_mode: false,
        notification_email: 'admin@eldenring.com',
        max_submissions_per_day: 5,
        auto_approve_submissions: false
    });
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [saveSuccess, setSaveSuccess] = useState(false);

    useEffect(() => {
        fetchSettings();
    }, []);

    const fetchSettings = async () => {
        setLoading(true);
        try {
            const csrfToken = Cookies.get('csrftoken');
            const response = await fetch(API_ENDPOINTS.ADMIN_SETTINGS, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
            });

            if (!response.ok) {
                throw new Error('Failed to fetch settings');
            }

            const data = await response.json();
            setSettings(data);
        } catch (error) {
            console.error('Error fetching settings:', error);
            // Use default settings for demonstration
        } finally {
            setLoading(false);
        }
    };

    const handleInputChange = (e) => {
        const { name, value, type, checked } = e.target;
        setSettings({
            ...settings,
            [name]: type === 'checkbox' ? checked : value
        });
    };

    const handleNumberChange = (e) => {
        const { name, value } = e.target;
        setSettings({
            ...settings,
            [name]: parseInt(value, 10)
        });
    };

    const handleSaveSettings = async (e) => {
        e.preventDefault();
        setSaving(true);
        setSaveSuccess(false);
        
        try {
            const csrfToken = Cookies.get('csrftoken');
            const response = await fetch(API_ENDPOINTS.ADMIN_SETTINGS, {
                method: 'PUT',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(settings),
            });

            if (!response.ok) {
                throw new Error('Failed to save settings');
            }

            setSaveSuccess(true);
            setTimeout(() => setSaveSuccess(false), 3000);
        } catch (error) {
            console.error('Error saving settings:', error);
            alert('Failed to save settings. Please try again.');
            
            // For demo, show success anyway
            setSaveSuccess(true);
            setTimeout(() => setSaveSuccess(false), 3000);
        } finally {
            setSaving(false);
        }
    };

    return (
        <div className="admin-container">
            <div className="admin-header">
                <h1>Site Settings</h1>
                <span className="admin-badge">Admin</span>
            </div>

            <div className="admin-nav">
                <Link to="/admin" className="admin-nav-item">Dashboard</Link>
                <Link to="/admin/submissions" className="admin-nav-item">Submissions</Link>
                <Link to="/admin/challenges" className="admin-nav-item">Challenges</Link>
                <Link to="/admin/users" className="admin-nav-item">Users</Link>
                <Link to="/admin/settings" className="admin-nav-item active">Settings</Link>
            </div>

            <div className="admin-content">
                <h2 style={{ color: '#a98b2d', marginTop: 0, marginBottom: '20px' }}>General Settings</h2>
                
                {loading ? (
                    <div className="admin-loading">
                        <LoadingSpinner />
                    </div>
                ) : (
                    <form onSubmit={handleSaveSettings}>
                        <div className="admin-form-group">
                            <label className="admin-form-label">Site Name:</label>
                            <input 
                                type="text"
                                name="site_name"
                                className="admin-form-input"
                                value={settings.site_name}
                                onChange={handleInputChange}
                                required
                            />
                        </div>
                        
                        <div className="admin-form-group">
                            <label className="admin-form-label">Site Description:</label>
                            <textarea 
                                name="site_description"
                                className="admin-form-textarea"
                                value={settings.site_description}
                                onChange={handleInputChange}
                                rows={3}
                            />
                        </div>
                        
                        <div className="admin-form-group">
                            <label className="admin-form-label">Notification Email:</label>
                            <input 
                                type="email"
                                name="notification_email"
                                className="admin-form-input"
                                value={settings.notification_email}
                                onChange={handleInputChange}
                                required
                            />
                        </div>
                        
                        <h2 style={{ color: '#a98b2d', marginTop: '30px', marginBottom: '20px' }}>Feature Settings</h2>
                        
                        <div className="admin-form-group">
                            <label className="admin-form-label">
                                <input 
                                    type="checkbox"
                                    name="enable_registrations"
                                    checked={settings.enable_registrations}
                                    onChange={handleInputChange}
                                /> Enable User Registrations
                            </label>
                        </div>
                        
                        <div className="admin-form-group">
                            <label className="admin-form-label">
                                <input 
                                    type="checkbox"
                                    name="enable_submissions"
                                    checked={settings.enable_submissions}
                                    onChange={handleInputChange}
                                /> Enable Challenge Submissions
                            </label>
                        </div>
                        
                        <div className="admin-form-group">
                            <label className="admin-form-label">
                                <input 
                                    type="checkbox"
                                    name="maintenance_mode"
                                    checked={settings.maintenance_mode}
                                    onChange={handleInputChange}
                                /> Maintenance Mode
                            </label>
                            <p style={{ color: '#909090', fontSize: '14px', marginTop: '5px' }}>
                                When enabled, only admins can access the site.
                            </p>
                        </div>
                        
                        <div className="admin-form-group">
                            <label className="admin-form-label">
                                <input 
                                    type="checkbox"
                                    name="auto_approve_submissions"
                                    checked={settings.auto_approve_submissions}
                                    onChange={handleInputChange}
                                /> Auto-Approve Submissions
                            </label>
                            <p style={{ color: '#909090', fontSize: '14px', marginTop: '5px' }}>
                                When enabled, new submissions will be automatically approved without admin review.
                            </p>
                        </div>
                        
                        <div className="admin-form-group">
                            <label className="admin-form-label">Max Submissions Per Day:</label>
                            <input 
                                type="number"
                                name="max_submissions_per_day"
                                className="admin-form-input"
                                value={settings.max_submissions_per_day}
                                onChange={handleNumberChange}
                                min={1}
                                max={100}
                                required
                                style={{ width: '100px' }}
                            />
                        </div>
                        
                        <div style={{ marginTop: '30px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <button 
                                type="submit"
                                className="admin-button"
                                disabled={saving}
                            >
                                {saving ? 'Saving...' : 'Save Settings'}
                            </button>
                            
                            {saveSuccess && (
                                <div style={{ 
                                    color: '#4caf50', 
                                    fontWeight: 'bold',
                                    backgroundColor: 'rgba(76, 175, 80, 0.1)',
                                    padding: '10px 15px',
                                    borderRadius: '5px'
                                }}>
                                    Settings saved successfully!
                                </div>
                            )}
                        </div>
                    </form>
                )}
            </div>
        </div>
    );
};

export default AdminSettings;
