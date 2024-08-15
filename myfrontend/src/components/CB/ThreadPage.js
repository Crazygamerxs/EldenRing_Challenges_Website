import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import './CB.css'; // Import the CSS file
import images from '../../images'; // Import the images

const ThreadPage = () => {
    const { threadId } = useParams(); // Get thread ID from URL params
    const [thread, setThread] = useState(null);
    const [comments, setComments] = useState([]);
    const [categoryName, setCategoryName] = useState('');

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:8888/api/threads/${threadId}/`);
                const data = response.data;

                setThread(data.thread);
                setComments(data.comments);
                setCategoryName(data.categoryName); // Assuming your API returns categoryName
            } catch (error) {
                console.error('Error fetching thread data:', error);
            }
        };

        fetchData();
    }, [threadId]);

    return (
        <div className="thread-page">
            {thread && (
                <div className="thread-header">
                    <div className="header-content">
                        <div className='pin-icon'>
                            <img src={images.pin} alt="pin icon" />
                        </div>
                        <h1>{thread.title}</h1>
                    </div>
                    <p>By {thread.username} on {new Date(thread.created_at).toLocaleDateString()}</p>
                    <div>{thread.body}</div>
                </div>
            )}

            <div className="breadcrumb">
                <Link to="/CB" className="forum-link">Forums</Link>
                <span className="divider">/</span>
                <span className="category-link" onClick={() => window.history.back()}>{categoryName}</span>
            </div>

            <div className="thread-content">
                {comments.map(comment => (
                    <div key={comment.id} className="comment">
                        <p><strong>{comment.username}</strong></p>
                        <p className="comment-date">on {new Date(comment.created_at).toLocaleDateString()}</p>
                        <p>{comment.body}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ThreadPage;
