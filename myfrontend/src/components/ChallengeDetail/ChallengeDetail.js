import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Cookies from 'js-cookie';
import './ChallengeDetail.css';
import images from '../../images';
import SubmitRun from './SubmitRun';
import MultipleRunSubmit from './MultipleRunSubmit'; // Import the MultipleRunSubmit component
import LoadingSpinner from '../common/LoadingSpinner'; // Import the LoadingSpinner component

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
    const [isMultiSubmitOpen, setIsMultiSubmitOpen] = useState(false); // State to control the multi-submit modal
    const [loadingChallenge, setLoadingChallenge] = useState(true);
    const [loadingSubmissions, setLoadingSubmissions] = useState(true);

    useEffect(() => {
        const fetchChallenge = async () => {
            try {
                const csrfToken = Cookies.get('csrftoken');
                const response = await fetch(`http://localhost:8888/api/challenge/${id}`, {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken': csrfToken,
                    },
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setChallenge(data);
                setLoadingChallenge(false);
            } catch (error) {
                console.error('Error fetching challenge:', error);
                setLoadingChallenge(false);
            }
        };

        fetchChallenge();
    }, [id]);

    // Function to fetch submissions - moved outside useEffect so it can be called from onClose
    const fetchSubmissions = async () => {
        if (!challenge) return;
        
        setLoadingSubmissions(true);
        try {
            const csrfToken = Cookies.get('csrftoken');
            const response = await fetch(`http://localhost:8888/api/submissions?challenge=${id}`, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            setSubmissions(data);
            setLoadingSubmissions(false);
        } catch (error) {
            console.error('Error fetching submissions:', error);
            setLoadingSubmissions(false);
        }
    };

    useEffect(() => {
        if (challenge) {
            fetchSubmissions();
        }
    }, [challenge, id]);

    return (
        <div>
            <div className="challenge-detail-container">
                <div className="challenge-detail-content">
                    {loadingChallenge ? (
                        <LoadingSpinner />
                    ) : (
                        <>
                            <div className="submit-run-btn-container">
                                <h1>{challenge.name}</h1>
                                <button className="submit-run-btn" onClick={() => setIsSubmitRunOpen(true)}>
                                    Submit Run
                                    <img src={images.plus_icon} alt="plus icon" className="submit-run-icon" />
                                </button>
                            </div>
                            <p>{challenge.details}</p>
                            <p>Difficulty: {challenge.difficulty}</p>
                            {/* Keep only the Overview tab for now */}
                            <div className="challenge-tabs">
                                <button onClick={() => setActiveTab('overview')} className={activeTab === 'overview' ? 'active' : ''}>Overview</button>
                                {/* Discussion tab hidden for future implementation 
                                <button onClick={() => setActiveTab('discussion')} className={activeTab === 'discussion' ? 'active' : ''}>Discussion</button>
                                */}
                            </div>
                        </>
                    )}
                </div>
                <div className="challenge-detail-results">
                    {loadingSubmissions ? (
                        <LoadingSpinner />
                    ) : (
                        activeTab === 'overview' && (
                            <div className="leaderboard">
                                <div className="leaderboard-header">
                                    <h2>Challenge Leaderboard</h2>
                                </div>
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
                                        {submissions.map((submission, index) => (
                                            <tr key={submission.id}>
                                                <td>{index + 1}</td>
                                                <td>{submission.username}</td>
                                                <td>{formatDuration(submission.time_taken)}</td>
                                                <td>{new Date(submission.submitted_at).toLocaleDateString()}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )
                    )}
                    {/* Implement discussion tab functionality later */}
                </div>
            </div>
            {isSubmitRunOpen && (
                <SubmitRun
                    challengeId={id}
                    onClose={() => {
                        setIsSubmitRunOpen(false);
                        fetchSubmissions(); // Trigger a refresh of submissions
                    }}
                    onOpenMultiSubmit={() => {
                        setIsSubmitRunOpen(false);
                        setIsMultiSubmitOpen(true);
                    }}
                />
            )}
            {isMultiSubmitOpen && (
                <MultipleRunSubmit
                    challenges={[challenge]} // Replace with a list of challenges you want to allow for multi-submit
                    onClose={() => setIsMultiSubmitOpen(false)}
                />
            )}
        </div>
    );
};

export default ChallengeDetail;
