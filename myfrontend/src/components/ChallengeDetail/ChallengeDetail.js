import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Cookies from 'js-cookie';
import './ChallengeDetail.css';
import images from '../../images';
import SubmitRun from './SubmitRun';
import MultipleRunSubmit from './MultipleRunSubmit';
import LoadingSpinner from '../common/LoadingSpinner';
import { API_ENDPOINTS } from '../../utils/api';

// Function to convert HH:MM:SS duration to a human-readable string
const formatDuration = (duration) => {
    const regex = /^(\d+ )?(\d{2}):(\d{2}):(\d{2})$/;
    const match = duration.match(regex);

    if (!match) return duration;

    let days = 0;
    let hours = 0;
    let minutes = parseInt(match[3], 10);

    if (match[1]) {
        days = parseInt(match[1], 10);
        hours += days * 24;
    }

    hours += parseInt(match[2], 10);
    minutes += hours * 60;

    let durationString = '';
    if (hours > 0) {
        durationString += `${hours} hour${hours > 1 ? 's' : ''} `;
    }
    if (minutes > 0 || hours > 0) {
        durationString += `${minutes % 60} min${minutes % 60 > 1 ? 's' : ''}`;
    }

    return durationString.trim() || '0 mins';
};

const ChallengeDetail = () => {
    const { id } = useParams();
    const [challenge, setChallenge] = useState(null);
    const [submissions, setSubmissions] = useState([]);
    const [activeTab, setActiveTab] = useState('overview');
    const [isSubmitRunOpen, setIsSubmitRunOpen] = useState(false);
    const [isMultiSubmitOpen, setIsMultiSubmitOpen] = useState(false);
    const [loadingChallenge, setLoadingChallenge] = useState(true);
    const [loadingSubmissions, setLoadingSubmissions] = useState(true);
    const [challengeError, setChallengeError] = useState(null);
    const [submissionsError, setSubmissionsError] = useState(null);

    useEffect(() => {
        // Reset state when ID changes
        setChallenge(null);
        setSubmissions([]);
        setChallengeError(null);
        setSubmissionsError(null);
        setLoadingChallenge(true);
        setLoadingSubmissions(true);
        
        if (id) {
            fetchChallenge();
            fetchSubmissions();
        }
    }, [id]);

    const fetchChallenge = async () => {
        try {
            const csrfToken = Cookies.get('csrftoken');
            const response = await fetch(API_ENDPOINTS.CHALLENGE_DETAIL(id), {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
            });
            
            if (!response.ok) {
                throw new Error(`Failed to fetch challenge: ${response.status}`);
            }
            
            const data = await response.json();
            setChallenge(data);
            setChallengeError(null);
        } catch (error) {
            console.error('Error fetching challenge:', error);
            setChallengeError('Failed to load challenge details. Please try again.');
        } finally {
            setLoadingChallenge(false);
        }
    };

    const fetchSubmissions = async () => {
        try {
            const csrfToken = Cookies.get('csrftoken');
            const response = await fetch(`${API_ENDPOINTS.SUBMISSIONS}?challenge=${id}`, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
            });
            
            if (!response.ok) {
                throw new Error(`Failed to fetch submissions: ${response.status}`);
            }
            
            const data = await response.json();
            setSubmissions(Array.isArray(data) ? data : []);
            setSubmissionsError(null);
        } catch (error) {
            console.error('Error fetching submissions:', error);
            setSubmissionsError('Failed to load submissions. Please try again.');
            setSubmissions([]); // Set empty array on error
        } finally {
            setLoadingSubmissions(false);
        }
    };

    // Show error state for challenge
    if (challengeError) {
        return (
            <div className="challenge-detail-container">
                <div className="challenge-detail-content">
                    <div style={{ textAlign: 'center', padding: '50px 0', color: '#f44336' }}>
                        <h3>Error Loading Challenge</h3>
                        <p>{challengeError}</p>
                        <button 
                            onClick={fetchChallenge}
                            style={{
                                background: '#a98b2d',
                                color: 'white',
                                border: 'none',
                                padding: '10px 20px',
                                borderRadius: '5px',
                                cursor: 'pointer'
                            }}
                        >
                            Try Again
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    // Show loading spinner while challenge is being fetched
    if (loadingChallenge || !challenge) {
        return (
            <div className="challenge-detail-container">
                <div className="challenge-detail-content">
                    <LoadingSpinner text="Loading challenge..." />
                </div>
            </div>
        );
    }

    return (
        <div>
            <div className="challenge-detail-container">
                <div className="challenge-detail-content">
                    <div className="submit-run-btn-container">
                        <h1>{challenge.name}</h1>
                        <button className="submit-run-btn" onClick={() => setIsSubmitRunOpen(true)}>
                            Submit Run
                            <img src={images.plus_icon} alt="plus icon" className="submit-run-icon" />
                        </button>
                    </div>
                    <p>{challenge.details}</p>
                    <p>Difficulty: {challenge.difficulty}</p>
                    
                    <div className="challenge-tabs">
                        <button 
                            onClick={() => setActiveTab('overview')} 
                            className={activeTab === 'overview' ? 'active' : ''}
                        >
                            Overview
                        </button>
                    </div>
                </div>
                
                <div className="challenge-detail-results">
                    {activeTab === 'overview' && (
                        <div className="leaderboard">
                            <div className="leaderboard-header">
                                <h2>Challenge Leaderboard</h2>
                            </div>
                            
                            {loadingSubmissions ? (
                                <div style={{ textAlign: 'center', padding: '50px 0' }}>
                                    <LoadingSpinner text="Loading submissions..." />
                                </div>
                            ) : submissionsError ? (
                                <div style={{ textAlign: 'center', padding: '50px 0', color: '#f44336' }}>
                                    <p>{submissionsError}</p>
                                    <button 
                                        onClick={fetchSubmissions}
                                        style={{
                                            background: '#a98b2d',
                                            color: 'white',
                                            border: 'none',
                                            padding: '8px 16px',
                                            borderRadius: '4px',
                                            cursor: 'pointer',
                                            marginTop: '10px'
                                        }}
                                    >
                                        Retry
                                    </button>
                                </div>
                            ) : (
                                <table>
                                    <thead>
                                        <tr>
                                            <th>#</th>
                                            <th>Player</th>
                                            <th>Time</th>
                                            <th>Date</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {submissions.length === 0 ? (
                                            <tr>
                                                <td colSpan="4" style={{ textAlign: 'center', padding: '30px', color: '#909090' }}>
                                                    No submissions yet. Be the first to complete this challenge!
                                                </td>
                                            </tr>
                                        ) : (
                                            submissions.map((submission, index) => (
                                                <tr key={submission.id || index}>
                                                    <td>{index + 1}</td>
                                                    <td>{submission.username || 'Unknown'}</td>
                                                    <td>{submission.time_taken ? formatDuration(submission.time_taken) : 'N/A'}</td>
                                                    <td>
                                                        {submission.submitted_at 
                                                            ? new Date(submission.submitted_at).toLocaleDateString()
                                                            : 'N/A'
                                                        }
                                                    </td>
                                                </tr>
                                            ))
                                        )}
                                    </tbody>
                                </table>
                            )}
                        </div>
                    )}
                </div>
            </div>
            
            {isSubmitRunOpen && (
                <SubmitRun
                    challengeId={id}
                    onClose={() => {
                        setIsSubmitRunOpen(false);
                        fetchSubmissions(); // Refresh submissions after closing
                    }}
                    onOpenMultiSubmit={() => {
                        setIsSubmitRunOpen(false);
                        setIsMultiSubmitOpen(true);
                    }}
                />
            )}
            
            {isMultiSubmitOpen && (
                <MultipleRunSubmit
                    challenges={[challenge]}
                    onClose={() => setIsMultiSubmitOpen(false)}
                />
            )}
        </div>
    );
};

export default ChallengeDetail;
