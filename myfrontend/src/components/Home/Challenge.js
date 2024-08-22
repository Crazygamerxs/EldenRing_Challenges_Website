import React from 'react';
import './Home.css';
import images from '../../images';
import { categories } from '../../constants/categories';
import { Link } from 'react-router-dom';

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
                            <div key={challenge.id} className="challenge-item">
                                <div>
                                    <Link to={`/challenge/${challenge.id}`}>
                                        <p className="challenge-title">{challenge.name}</p>
                                    </Link>
                                    <p className="challenge-details">{challenge.details}</p>
                                    <div className="challenge-content">
                                        <div className="challenge-subdetails-container">
                                            <p className="challenge-subdetails">
                                                {challenge.completed ? 'Completed' : 'Not Completed'} | {challenge.difficulty}
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
