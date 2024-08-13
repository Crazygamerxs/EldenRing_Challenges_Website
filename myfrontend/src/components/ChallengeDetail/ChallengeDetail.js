import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import './ChallengeDetail.css'; // Ensure this CSS file is updated as per the provided styles
import TopBar from '../common/TopBar';
import BottomBar from '../common/BottomBar';

const ChallengeDetail = () => {
    const { id } = useParams();
    const [challenge, setChallenge] = useState(null);
    const [submissions, setSubmissions] = useState([]);
    const [activeTab, setActiveTab] = useState('overview'); // Default to 'overview'

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
            <TopBar />
            <div className="challenge-detail-container">
                <div className="challenge-detail-content">
                    <h1>{challenge.name}</h1>
                    <p>{challenge.details}</p>
                    <p>Difficulty: {challenge.difficulty}</p>
                    <div className="challenge-tabs">
                        <button onClick={() => setActiveTab('overview')} className={activeTab === 'overview' ? 'active' : ''}>Overview</button>
                        <button onClick={() => setActiveTab('discussion')} className={activeTab === 'discussion' ? 'active' : ''}>Discussion</button>
                    </div>
                </div>
                <div className="challenge-detail-results">
                    {activeTab === 'overview' && (
                        <div className="submissions-list">
                            <h2>Submissions</h2>
                            <ul>
                                {submissions.map(submission => (
                                    <li key={submission.id}>
                                        <a href={submission.file_url} target="_blank" rel="noopener noreferrer">Submission by {submission.user.email}</a>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                    {/* Implement discussion tab functionality later */}
                </div>
            </div>
            <BottomBar />
        </div>
    );
};

export default ChallengeDetail;
