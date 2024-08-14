import React from 'react';
import { Link } from 'react-router-dom'; // Import Link
import images from '../../images';
import './CB.css';

const CommunityBoard = () => {
    const forums = [
        { id: 1, name: 'Introduction', description: 'New to the Community? Introduce yourself here.', posts: '11,336', lastPostUser: 'Soda', lastPostAvatar: images.pp_1 },
        { id: 2, name: 'Challenges', description: 'For general discussion of challenges.', posts: '1,336', lastPostUser: 'Salty', lastPostAvatar: images.pp_2 },
        { id: 3, name: 'Talk', description: 'Off-topic discussion, unrelated to challenges.', posts: '336', lastPostUser: 'Crazygamer', lastPostAvatar: images.pp_3 },
        { id: 4, name: 'The Site', description: 'Site help / suggestions / feedback.', posts: '51,061', lastPostUser: 'Rockett', lastPostAvatar: images.pp_1 },
    ];

    return (
        <div className='community-page'>
            <div className="community-board">
                <h2>Elden Ring Community Forums</h2>
                <div className="forum-table">
                    <div className="forum-header">
                        <div className="forum-column-1st">Forums</div>
                        <div className="forum-column">Posts</div>
                        <div className="forum-column">Last Post</div>
                    </div>
                    {forums.map((forum) => (
                        <Link to={`/forum/${forum.id}`} key={forum.id} className="forum-row">
                            <div className="forum-column-1st">
                                <strong>{forum.name}</strong>
                                <span>{forum.description}</span>
                            </div>
                            <div className="forum-column">{forum.posts}</div>
                            <div className="forum-column">
                                <img src={forum.lastPostAvatar} alt={`${forum.lastPostUser} avatar`} className="avatar" />
                                <span>{forum.lastPostUser}</span>
                            </div>
                        </Link>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default CommunityBoard;
