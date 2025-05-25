import React, { useState, useEffect } from 'react';
import Cookies from 'js-cookie';
import './Leaderboard.css';
import LoadingSpinner from '../common/LoadingSpinner';

const Leaderboard = () => {
    const [activeTab, setActiveTab] = useState('challenges');
    const [leaderboardData, setLeaderboardData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);
    const usersPerPage = 10;

    useEffect(() => {
        fetchLeaderboardData();
    }, [activeTab]);

    const fetchLeaderboardData = async () => {
        setLoading(true);
        setError(null);
        
        try {
            const csrfToken = Cookies.get('csrftoken');
            const endpoint = activeTab === 'challenges' 
                ? 'http://localhost:8888/api/leaderboard/challenges/'
                : 'http://localhost:8888/api/leaderboard/points/';
            
            const response = await fetch(endpoint, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
            });

            if (!response.ok) {
                throw new Error('Failed to fetch leaderboard data');
            }

            const data = await response.json();
            setLeaderboardData(data);
            setCurrentPage(1); // Reset to first page when switching tabs
        } catch (err) {
            console.error('Error fetching leaderboard:', err);
            setError(err.message);
            // Generate mock data for demonstration
            generateMockLeaderboardData();
        } finally {
            setLoading(false);
        }
    };

    const generateMockLeaderboardData = () => {
        const mockData = [];
        for (let i = 1; i <= 25; i++) { // Generate 25 mock users for pagination demo
            mockData.push({
                id: i,
                username: `Player${i}`,
                challenges_completed: Math.max(1, 20 - i + Math.floor(Math.random() * 5)),
                points: Math.max(100, 2000 - (i * 50) + Math.floor(Math.random() * 200))
            });
        }
        setLeaderboardData(mockData);
        setCurrentPage(1);
    };

    const handleTabChange = (tab) => {
        setActiveTab(tab);
    };

    const getRankDisplay = (globalIndex) => {
        const rank = globalIndex + 1;
        if (rank === 1) return '🥇';
        if (rank === 2) return '🥈';
        if (rank === 3) return '🥉';
        return `#${rank}`;
    };

    // Pagination logic
    const indexOfLastUser = currentPage * usersPerPage;
    const indexOfFirstUser = indexOfLastUser - usersPerPage;
    const currentUsers = leaderboardData.slice(indexOfFirstUser, indexOfLastUser);
    const totalPages = Math.ceil(leaderboardData.length / usersPerPage);

    const handlePageChange = (page) => {
        if (page >= 1 && page <= totalPages) {
            setCurrentPage(page);
            // Scroll to top of leaderboard content
            const leaderboardContent = document.querySelector('.leaderboard-content');
            if (leaderboardContent) {
                leaderboardContent.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
    };

    // Pagination component
    const Pagination = () => {
        const getPageNumbers = () => {
            const pageNumbers = [];
            const maxPagesToShow = 5;
            const half = Math.floor(maxPagesToShow / 2);
            
            let start = Math.max(1, currentPage - half);
            let end = Math.min(totalPages, currentPage + half);
            
            if (currentPage - half <= 1) {
                end = Math.min(maxPagesToShow, totalPages);
            } else if (currentPage + half >= totalPages) {
                start = Math.max(totalPages - maxPagesToShow + 1, 1);
            }

            if (start > 1) {
                pageNumbers.push(1);
                if (start > 2) pageNumbers.push('...');
            }
            
            for (let i = start; i <= end; i++) {
                pageNumbers.push(i);
            }
            
            if (end < totalPages) {
                if (end < totalPages - 1) pageNumbers.push('...');
                pageNumbers.push(totalPages);
            }
            
            return pageNumbers;
        };

        if (totalPages <= 1) return null;

        return (
            <div className="leaderboard-pagination">
                <button
                    className="pagination-btn"
                    onClick={() => handlePageChange(currentPage - 1)}
                    disabled={currentPage === 1}
                >
                    &lt;
                </button>
                {getPageNumbers().map((page, index) => (
                    <button
                        key={index}
                        className={`pagination-btn ${page === currentPage ? 'active' : ''} ${page === '...' ? 'ellipsis' : ''}`}
                        onClick={() => typeof page === 'number' && handlePageChange(page)}
                        disabled={page === '...'}
                    >
                        {page}
                    </button>
                ))}
                <button
                    className="pagination-btn"
                    onClick={() => handlePageChange(currentPage + 1)}
                    disabled={currentPage === totalPages}
                >
                    &gt;
                </button>
            </div>
        );
    };

    return (
        <div className="leaderboard-container">
            <div className="leaderboard-header">
                <h1>Leaderboard</h1>
            </div>

            <div className="leaderboard-tabs">
                <button 
                    className={activeTab === 'challenges' ? 'active' : ''}
                    onClick={() => handleTabChange('challenges')}
                >
                    By Challenges
                </button>
                <button 
                    className={activeTab === 'points' ? 'active' : ''}
                    onClick={() => handleTabChange('points')}
                >
                    By Points
                </button>
            </div>

            <div className="leaderboard-content">
                {loading ? (
                    <div className="leaderboard-loading">
                        <LoadingSpinner />
                    </div>
                ) : error ? (
                    <div className="leaderboard-error">
                        <p>Failed to load leaderboard data</p>
                        <button onClick={fetchLeaderboardData} className="retry-btn">
                            Try Again
                        </button>
                    </div>
                ) : (
                    <>
                        <div className="leaderboard-table-container">
                            <table className="leaderboard-table">
                                <thead>
                                    <tr>
                                        <th>Rank</th>
                                        <th>Player</th>
                                        <th>Challenges</th>
                                        <th>Points</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {currentUsers.map((player, index) => {
                                        const globalIndex = indexOfFirstUser + index;
                                        return (
                                            <tr key={player.id} className="leaderboard-row">
                                                <td className="rank-cell">
                                                    <span className="rank-display">
                                                        {getRankDisplay(globalIndex)}
                                                    </span>
                                                </td>
                                                <td className="player-cell">
                                                    <span className="player-name">{player.username}</span>
                                                </td>
                                                <td className="challenges-cell">
                                                    <span className="challenges-completed">
                                                        {player.challenges_completed}
                                                    </span>
                                                </td>
                                                <td className="points-cell">
                                                    <span className="points-earned">
                                                        {player.points || 0}
                                                    </span>
                                                </td>
                                            </tr>
                                        );
                                    })}
                                </tbody>
                            </table>
                        </div>
                        
                        <Pagination />
                        
                        {leaderboardData.length === 0 && (
                            <div className="no-data-message">
                                <p>No leaderboard data available yet.</p>
                                <p>Complete some challenges to appear on the leaderboard!</p>
                            </div>
                        )}
                    </>
                )}
            </div>
        </div>
    );
};

export default Leaderboard;