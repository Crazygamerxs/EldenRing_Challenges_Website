import React, { useState } from 'react';
import TopBar from '../common/TopBar';
import BottomBar from '../common/BottomBar';
import Challenge from './Challenge';
import ChallengeFilter from './ChallengeFilter';
import './Home.css';

function Home() {
    const [filters, setFilters] = useState({
        difficulties: [],
        types: []
    });

    const handleFilterChange = (newFilters) => {
        setFilters(newFilters);
    };

    return (
        <div className="home-wrapper">
            <TopBar /> 
            <div className="home-page">
                <Challenge filters={filters} />
                <ChallengeFilter onFilterChange={handleFilterChange} />
            </div>
            <BottomBar />
        </div>
    );
}

export default Home;
