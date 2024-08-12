import React, { useEffect, useState } from 'react';
import './Home.css';
import images from '../../images';

const Challenge = () => {
    const [challenges, setChallenges] = useState([]);

    useEffect(() => {
        const fetchChallenges = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8888/api/challenge/');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                console.log('Fetched Challenges:', data); 
                setChallenges(data);
            } catch (error) {
                console.error('Error fetching challenges:', error);
            }
        };

        fetchChallenges();
    }, []);

    return (
        <div className="challenge-container">
            <h2 className="challenge-heading">Challenges</h2>
            {challenges.map((challenge, index) => (
                <div key={index} className="challenge-item">
                    <div>
                        <p className="challenge-title">{challenge.name}</p>
                        <p className="challenge-details">{challenge.details}</p>
                        <div className="challenge-content">
                            <div className="challenge-subdetails-container">
                                <p className="challenge-subdetails">
                                    {challenge.completed ? 'Completed' : 'Not Completed'} | {challenge.difficulty}
                                </p>
                            </div>
                            <div className="challenge-actions">
                                <button className='challenge-btn'>View All Submissions</button>
                                <button className='challenge-btn'>
                                    <div className='discussion-icon'>
                                        <img src={images.chat} alt="chat icon" />
                                    </div>
                                    Discussion
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default Challenge;