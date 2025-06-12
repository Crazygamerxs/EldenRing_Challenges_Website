import React from 'react';
import './Home.css';
import images from '../../images';
import { categories } from '../../constants/categories';
import { Link } from 'react-router-dom';

import { API_ENDPOINTS } from '../../utils/api';
const Challenge = ({ challenges }) => {

    const getCategoryName = (id) => {
        const category = categories.find(cat => cat.id === id);
        return category ? category.name : 'Unknown Category';
    };

    const groupedChallenges = challenges.reduce((acc, challenge) => {
        const categoryName = getCategoryName(challenge.category);
        if (!acc[categoryName]) {
            acc[categoryName] = [];
        }
        acc[categoryName].push(challenge);
        return acc;
    }, {});

    return (
        <div className="challenge-container">
            {challenges.length === 0 ? (
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
                            <div 
                                key={challenge.id} 
                                className={`challenge-item ${challenge.is_dlc ? 'dlc-content' : ''} ${challenge.is_combination ? 'combination-challenge' : ''}`}
                            >
                                <div>
                                    <div className="challenge-header">
                                        <Link to={`/challenge/${challenge.id}`}>
                                            <p className="challenge-title">{challenge.name}</p>
                                        </Link>
                                        <div className="challenge-badges">
                                            {challenge.is_dlc && (
                                                <span className="challenge-badge dlc-badge" title="Requires DLC Content">
                                                    DLC
                                                </span>
                                            )}
                                            {challenge.is_combination && (
                                                <span className="challenge-badge combo-badge" title="Combination Challenge">
                                                    COMBO
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                    <p className="challenge-details">{challenge.details}</p>
                                    <div className="challenge-content">
                                        <div className="challenge-subdetails-container">
                                            <p className="challenge-subdetails">
                                                <span className={challenge.completed ? 'completion-status completed' : 'completion-status not-completed'}>
                                                    {challenge.completed ? 'Completed' : 'Not Completed'}
                                                </span> | 
                                                <span>
                                                    {challenge.difficulty}
                                                </span>
                                                {challenge.is_combination && (
                                                    <span className="combination-indicator"> | Multi-Challenge</span>
                                                )}
                                            </p>
                                        </div>
                                        <div className="challenge-actions">
                                            <Link to={`/challenge/${challenge.id}`}>
                                                <button className='challenge-btn'>View All Submissions</button>
                                            </Link>
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