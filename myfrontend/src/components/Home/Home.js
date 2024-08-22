import React, { useState, useEffect } from 'react';
import Challenge from './Challenge';
import ChallengeFilter from './ChallengeFilter';
import Pagination from './Pagination';
import './Home.css';
import Cookies from 'js-cookie';

function Home() {
    const [filters, setFilters] = useState({
        difficulties: [],
        types: []
    });

    const [challenges, setChallenges] = useState([]);
    const [filteredChallenges, setFilteredChallenges] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const challengesPerPage = 10;

    useEffect(() => {
        const fetchChallenges = async () => {
            try {
                const response = await fetch('http://localhost:8888/api/challenge/', {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken': Cookies.get('csrftoken'),
                    },
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setChallenges(data);
            } catch (error) {
                console.error('Error fetching challenges:', error);
            }
        };
    
        fetchChallenges();
    }, []); // Ensure this effect only runs once on component mount
    

    useEffect(() => {
        const { difficulties, types } = filters;
    
        const newFilteredChallenges = challenges.filter((challenge) => {
            const isDifficultyMatch = difficulties.length === 0 || difficulties.includes(challenge.difficulty);
            const isTypeMatch = types.length === 0 || types.includes(challenge.category);
            return isDifficultyMatch && isTypeMatch;
        });
    
        setFilteredChallenges(newFilteredChallenges);
        // setCurrentPage(1); // Reset to first page when filters change
    }, [challenges, filters]); // Ensure dependencies are correct
    

    const handleFilterChange = (newFilters) => {
        setFilters(newFilters);
    };

    const indexOfLastChallenge = currentPage * challengesPerPage;
    const indexOfFirstChallenge = indexOfLastChallenge - challengesPerPage;
    const currentChallenges = filteredChallenges.slice(indexOfFirstChallenge, indexOfLastChallenge);

    const totalPages = Math.ceil(filteredChallenges.length / challengesPerPage);

    const handlePageChange = (page) => {
        if (page >= 1 && page <= totalPages) {
            setCurrentPage(page);
        }
    };

    return (
        <div className="home-wrapper">
            <div className="home-page">
                <div className='challenge-section'>
                    <Challenge challenges={currentChallenges} />
                    <Pagination
                        currentPage={currentPage}
                        totalPages={totalPages}
                        onPageChange={handlePageChange}
                    />
                </div>
                <ChallengeFilter onFilterChange={handleFilterChange} />
            </div>
        </div>
    );
}

export default Home;
