import React, { useState, useEffect } from 'react';
import Cookies from 'js-cookie';
import { useNavigate } from 'react-router-dom';
import './Leaderboard.css';
import LoadingSpinner from '../common/LoadingSpinner';
import { motion, AnimatePresence } from 'framer-motion';

const Leaderboard = () => {
    const [challengesLeaderboard, setChallengesLeaderboard] = useState([]);
    const [pointsLeaderboard, setPointsLeaderboard] = useState([]);
    const [loading, setLoading] = useState(true);
    const [currentPage, setCurrentPage] = useState(1);
    const [activeTab, setActiveTab] = useState('challenges'); // 'challenges' or 'points'
    const usersPerPage = 50;
    const navigate = useNavigate();

    useEffect(() => {
        fetchLeaderboardData();
    }, []);

    const fetchLeaderboardData = async () => {
        setLoading(true);
        try {
            const csrfToken = Cookies.get('csrftoken');
            
            // Fetch challenges leaderboard
            const challengesResponse = await fetch('http://localhost:8888/api/leaderboard/challenges', {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
            });

            // Fetch points leaderboard
            const pointsResponse = await fetch('http://localhost:8888/api/leaderboard/points', {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
            });

            if (!challengesResponse.ok || !pointsResponse.ok) {
                throw new Error('Failed to fetch leaderboard data');
            }

            const challengesData = await challengesResponse.json();
            const pointsData = await pointsResponse.json();

            setChallengesLeaderboard(challengesData);
            setPointsLeaderboard(pointsData);
        } catch (error) {
            console.error('Error fetching leaderboard data:', error);
            // If API fails, use mock data for demonstration
            setChallengesLeaderboard(generateMockChallengesData());
            setPointsLeaderboard(generateMockPointsData());
        } finally {
            setLoading(false);
        }
    };

    // Mock data generator for demonstration purposes
    const generateMockChallengesData = () => {
        const mockUsers = [];
        // Generate 100 mock users for pagination testing
        for (let i = 1; i <= 100; i++) {
            mockUsers.push({
                id: i,
                username: `Player${i}`,
                profile_image: `/static/main/images/profile_pic/pp_${(i % 3) + 1}.png`,
                challenges_completed: 100 - i + 1,
                points: Math.floor(Math.random() * 1000) + 500
            });
        }
        return mockUsers;
    };

    const generateMockPointsData = () => {
        const mockUsers = [];
        // Generate 100 mock users for pagination testing, but sort by points
        for (let i = 1; i <= 100; i++) {
            mockUsers.push({
                id: i,
                username: `Player${i}`,
                profile_image: `/static/main/images/profile_pic/pp_${(i % 3) + 1}.png`,
                challenges_completed: Math.floor(Math.random() * 50) + 10,
                points: 5000 - (i * 40) + Math.floor(Math.random() * 30)
            });
        }
        return mockUsers;
    };

    // Get current leaderboard data based on active tab
    const currentLeaderboard = activeTab === 'challenges' ? challengesLeaderboard : pointsLeaderboard;

    // Get current users for pagination
    const indexOfLastUser = currentPage * usersPerPage;
    const indexOfFirstUser = indexOfLastUser - usersPerPage;
    const currentUsers = currentLeaderboard.slice(indexOfFirstUser, indexOfLastUser);
    const totalPages = Math.ceil(currentLeaderboard.length / usersPerPage);

    // Change page
    const paginate = (pageNumber) => setCurrentPage(pageNumber);

    // Change tab
    const handleTabChange = (tab) => {
        setActiveTab(tab);
        setCurrentPage(1); // Reset to first page when changing tabs
    };

    const renderRankCell = (index) => {
        // Calculate the actual rank based on pagination
        const actualRank = indexOfFirstUser + index + 1;
        
        if (actualRank <= 3) {
            return (
                <div className={`top-rank rank-${actualRank}`}>
                    {actualRank}
                </div>
            );
        }
        return actualRank;
    };

    return (
        <div className="leaderboard-container">
            <div className="leaderboard-header">
                <h1>Global Leaderboard</h1>
            </div>

            <div className="leaderboard-tabs">
                <motion.button 
                    className={`leaderboard-tab ${activeTab === 'challenges' ? 'active' : ''}`}
                    onClick={() => handleTabChange('challenges')}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                >
                    Most Completed Challenges
                </motion.button>
                <motion.button 
                    className={`leaderboard-tab ${activeTab === 'points' ? 'active' : ''}`}
                    onClick={() => handleTabChange('points')}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                >
                    Highest Points
                </motion.button>
            </div>

            <div className="leaderboard-content">
                {loading ? (
                    <div className="loading-container">
                        <LoadingSpinner />
                    </div>
                ) : (
                    <AnimatePresence mode="wait">
                        <motion.div 
                            key={activeTab}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            transition={{ duration: 0.3 }}
                            className="leaderboard-table-container"
                        >
                            <table className="leaderboard-table">
                                <thead>
                                    <tr>
                                        <th>Rank</th>
                                        <th>Player</th>
                                        <th>
                                            {activeTab === 'challenges' ? 'Challenges Completed' : 'Points'}
                                        </th>
                                        <th>
                                            {activeTab === 'challenges' ? 'Points' : 'Challenges Completed'}
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {currentUsers.map((player, index) => (
                                        <motion.tr 
                                            key={player.id}
                                            initial={{ opacity: 0, y: 10 }}
                                            animate={{ opacity: 1, y: 0 }}
                                            transition={{ duration: 0.2, delay: index * 0.03 }}
                                        >
                                            <td className="rank-cell">
                                                {renderRankCell(index)}
                                            </td>
                                            <td>
                                                <div className="player-cell">
                                                <span className="player-name">
                                                    {player.username}
                                                </span>
                                                </div>
                                            </td>
                                            <td className="value-cell">
                                                {activeTab === 'challenges' 
                                                    ? player.challenges_completed 
                                                    : <span className="points">{player.points}</span>
                                                }
                                            </td>
                                            <td className="value-cell">
                                                {activeTab === 'challenges' 
                                                    ? <span className="points">{player.points}</span>
                                                    : player.challenges_completed
                                                }
                                            </td>
                                        </motion.tr>
                                    ))}
                                </tbody>
                            </table>
                        </motion.div>
                    </AnimatePresence>
                )}
                
                {!loading && totalPages > 1 && (
                    <div className="pagination">
                        <button 
                            className="pagination-button"
                            onClick={() => paginate(1)}
                            disabled={currentPage === 1}
                        >
                            First
                        </button>
                        <button 
                            className="pagination-button"
                            onClick={() => paginate(currentPage - 1)}
                            disabled={currentPage === 1}
                        >
                            Prev
                        </button>
                        
                        {/* Show page numbers */}
                        {[...Array(totalPages)].map((_, i) => {
                            // Only show a few pages around the current page
                            if (
                                i === 0 || // First page
                                i === totalPages - 1 || // Last page
                                (i >= currentPage - 2 && i <= currentPage + 2) // Pages around current
                            ) {
                                return (
                                    <button
                                        key={i}
                                        className={`pagination-button ${currentPage === i + 1 ? 'active' : ''}`}
                                        onClick={() => paginate(i + 1)}
                                    >
                                        {i + 1}
                                    </button>
                                );
                            } else if (
                                i === currentPage - 3 || 
                                i === currentPage + 3
                            ) {
                                // Show ellipsis for skipped pages
                                return <span key={i} className="pagination-ellipsis">...</span>;
                            }
                            return null;
                        })}
                        
                        <button 
                            className="pagination-button"
                            onClick={() => paginate(currentPage + 1)}
                            disabled={currentPage === totalPages}
                        >
                            Next
                        </button>
                        <button 
                            className="pagination-button"
                            onClick={() => paginate(totalPages)}
                            disabled={currentPage === totalPages}
                        >
                            Last
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Leaderboard;
