import React, { useEffect, useState } from 'react';
import './Home.css';
import images from '../../images';
import { categories } from '../../constants/categories';

const Challenge = ({ filters }) => {
    const [challenges, setChallenges] = useState([]);
    const [filteredChallenges, setFilteredChallenges] = useState([]);

    useEffect(() => {
        const fetchChallenges = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8888/api/challenge/');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setChallenges(data);
            } catch (error) {
                error('Error fetching challenges:', error);
            }
        };

        fetchChallenges();
    }, []); // Empty dependency array

    useEffect(() => {
        const { difficulties, types } = filters;

        const newFilteredChallenges = challenges.filter((challenge) => {
            const isDifficultyMatch = difficulties.length === 0 || difficulties.includes(challenge.difficulty);
            const isTypeMatch = types.length === 0 || types.includes(challenge.category);
            return isDifficultyMatch && isTypeMatch;
        });

        setFilteredChallenges(newFilteredChallenges);
    }, [challenges, filters]); // Dependencies are correct

    const getCategoryName = (id) => {
        const category = categories.find(cat => cat.id === id);
        return category ? category.name : 'Unknown Category';
    };

    const groupedChallenges = filteredChallenges.reduce((acc, challenge) => {
        const categoryName = getCategoryName(challenge.category);
        if (!acc[categoryName]) {
            acc[categoryName] = [];
        }
        acc[categoryName].push(challenge);
        return acc;
    }, {});

    return (
        <div className="challenge-container">
            {filteredChallenges.length === 0 ? (
                <div className="no-data">
                    <img src={images.nodata} alt="No Data" className="no-data-icon" />
                    <p className="no-data-message">
                        We couldn't find what you searched for. Try changing the filters.
                    </p>
                </div>
            ) : (
                Object.keys(groupedChallenges).map((categoryName, index) => (
                    <div key={index}>
                        <h2 className="challenge-heading">{categoryName}</h2>
                        {groupedChallenges[categoryName].map((challenge) => (
                            <div key={challenge.id} className="challenge-item">
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
                ))
            )}
        </div>
    );
};

export default Challenge;
