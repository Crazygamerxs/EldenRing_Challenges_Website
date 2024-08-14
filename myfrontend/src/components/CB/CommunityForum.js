import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './CB.css';

const CommunityForum = () => {
    const { forumId } = useParams(); // Get forum ID from URL params
    const [threads, setThreads] = useState([]);
    const [categoryName, setCategoryName] = useState('');

    useEffect(() => {
        fetch(`/api/threads/?category_id=${forumId}`)
            .then(response => {
                if (!response.ok) {
                    return response.text().then(text => {
                        throw new Error(`HTTP error! Status: ${response.status}, Response: ${text}`);
                    });
                }
                return response.json();
            })
            .then(data => {
                console.log('Fetched threads:', data); // Log the fetched data
                setThreads(data);
    
                if (data.length > 0 && data[0].category) {
                    setCategoryName(data[0].category.name);
                } else {
                    setCategoryName('No Category');
                }
            })
            .catch(error => console.error('Error fetching threads:', error));
    }, [forumId]);
    
    return (
        <div className='community-page'>
            <div className="community-board">
                <h2>Forums / {categoryName}</h2>
                <div className="forum-table">
                    <div className="forum-header">
                        <div className="forum-column-1st">Thread</div>
                        <div className="forum-column">Replies</div>
                        <div className="forum-column">Created</div>
                    </div>
                    {threads.length > 0 ? (
                        threads.map((thread) => (
                            <div className="forum-row" key={thread.id}>
                                <div className="forum-column-1st">
                                    <strong>{thread.title}</strong>
                                    <span>by {thread.username}</span>
                                </div>
                                <div className="forum-column">0</div> {/* Placeholder for replies */}
                                <div className="forum-column">
                                    <span>{new Date(thread.created_at).toLocaleString()}</span>
                                </div>
                            </div>
                        ))
                    ) : (
                        <div className="forum-row">
                            <div className="forum-column-1st">No threads available</div>
                            <div className="forum-column">-</div>
                            <div className="forum-column">-</div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default CommunityForum;
