import React, { useState, useEffect, useRef } from 'react';
import Challenge from './Challenge';
import ChallengeFilter from './ChallengeFilter';
import Pagination from './Pagination';
import './Home.css';
import Cookies from 'js-cookie';

import { API_ENDPOINTS } from '../../utils/api';
function Home() {
    const [filters, setFilters] = useState({
        difficulties: [],
        types: [],
        dlc: [],
        combination: []
    });

    const [challenges, setChallenges] = useState([]);
    const [filteredChallenges, setFilteredChallenges] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const challengesPerPage = 10;
    
    // Use ref to track if filters actually changed
    const prevFiltersRef = useRef();

    useEffect(() => {
        const fetchChallenges = async () => {
            try {
                const response = await fetch(API_ENDPOINTS.CHALLENGES, {
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
    }, []);

    useEffect(() => {
        const { difficulties, types, dlc, combination } = filters;
    
        const newFilteredChallenges = challenges.filter((challenge) => {
            // Difficulty filter
            const isDifficultyMatch = difficulties.length === 0 || difficulties.includes(challenge.difficulty);
            
            // Category/Type filter
            const isTypeMatch = types.length === 0 || types.includes(challenge.category);
            
            // DLC content filter
            let isDLCMatch = true;
            if (dlc.length > 0) {
                if (dlc.includes('base') && dlc.includes('dlc')) {
                    // Both selected, show all
                    isDLCMatch = true;
                } else if (dlc.includes('base')) {
                    // Only base game
                    isDLCMatch = !challenge.is_dlc;
                } else if (dlc.includes('dlc')) {
                    // Only DLC content
                    isDLCMatch = challenge.is_dlc;
                }
            }
            
            // Challenge combination filter
            let isCombinationMatch = true;
            if (combination.length > 0) {
                if (combination.includes('single') && combination.includes('combination')) {
                    // Both selected, show all
                    isCombinationMatch = true;
                } else if (combination.includes('single')) {
                    // Only single challenges
                    isCombinationMatch = !challenge.is_combination;
                } else if (combination.includes('combination')) {
                    // Only combination challenges
                    isCombinationMatch = challenge.is_combination;
                }
            }
            
            return isDifficultyMatch && isTypeMatch && isDLCMatch && isCombinationMatch;
        });
    
        setFilteredChallenges(newFilteredChallenges);
        
        // Only reset to page 1 if filters actually changed (not on initial load)
        const filtersChanged = prevFiltersRef.current && 
            JSON.stringify(prevFiltersRef.current) !== JSON.stringify(filters);
        
        if (filtersChanged) {
            setCurrentPage(1);
        }
        
        // Update the previous filters reference
        prevFiltersRef.current = filters;
        
    }, [challenges, filters]);

    const handleFilterChange = (newFilters) => {
        setFilters(newFilters);
    };

    const indexOfLastChallenge = currentPage * challengesPerPage;
    const indexOfFirstChallenge = indexOfLastChallenge - challengesPerPage;
    const currentChallenges = filteredChallenges.slice(indexOfFirstChallenge, indexOfLastChallenge);

    const totalPages = Math.ceil(filteredChallenges.length / challengesPerPage);

    const handlePageChange = (page) => {
        console.log('Changing to page:', page); // Debug log
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