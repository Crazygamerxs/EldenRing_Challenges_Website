import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import './ChallengeDetail.css'; 
import images from '../../images';
import SubmitRun from './SubmitRun'; // Import the SubmitRun component

// Function to convert HH:MM:SS duration to a human-readable string
const formatDuration = (duration) => {
    // Check if the duration is a valid format
    const regex = /^(\d+ )?(\d{2}):(\d{2}):(\d{2})$/;
    const match = duration.match(regex);

    if (!match) return duration;

    let days = 0;
    let hours = 0;
    let minutes = parseInt(match[3], 10);

    if (match[1]) {
        // If days are present, convert them to hours
        days = parseInt(match[1], 10);
        hours += days * 24;
    }

    hours += parseInt(match[2], 10);
    minutes += hours * 60; // Convert hours to minutes

    // Format the duration string
    let durationString = '';
    if (hours > 0) {
        durationString += `${hours} hour${hours > 1 ? 's' : ''} `;
    }
    if (minutes > 0 || hours > 0) {  // Include minutes if there are hours
        durationString += `${minutes % 60} min${minutes % 60 > 1 ? 's' : ''}`;
    }

    return durationString.trim() || '0 mins';
};


const ChallengeDetail = () => {
    const { id } = useParams();
    const [challenge, setChallenge] = useState(null);
    const [submissions, setSubmissions] = useState([]);
    const [activeTab, setActiveTab] = useState('overview');
    const [isSubmitRunOpen, setIsSubmitRunOpen] = useState(false); // State to control modal visibility


    useEffect(() => {
        const fetchChallenge = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:8888/api/challenge/${id}`);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setChallenge(data);
            } catch (error) {
                console.error('Error fetching challenge:', error);
            }
        };

        fetchChallenge();
    }, [id]);

    useEffect(() => {
        if (challenge) {
            const fetchSubmissions = async () => {
                try {
                    const response = await fetch(`http://127.0.0.1:8888/api/submissions?challenge=${id}`);
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    const data = await response.json();
                    setSubmissions(data);
                } catch (error) {
                    console.error('Error fetching submissions:', error);
                }
            };

            fetchSubmissions();
        }
    }, [challenge, id]);

    if (!challenge) {
        return <p>Loading...</p>;
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
                        <button onClick={() => setActiveTab('overview')} className={activeTab === 'overview' ? 'active' : ''}>Overview</button>
                        <button onClick={() => setActiveTab('discussion')} className={activeTab === 'discussion' ? 'active' : ''}>Discussion</button>
                    </div>
                </div>
                <div className="challenge-detail-results">
                    {activeTab === 'overview' && (
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
                    )}
                    {/* Implement discussion tab functionality later */}
                </div>
            </div>
            {isSubmitRunOpen && <SubmitRun challengeId={id} onClose={() => setIsSubmitRunOpen(false)} />}
        </div>
    );
};

export default ChallengeDetail;
