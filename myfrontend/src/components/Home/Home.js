import React, { useState } from 'react';
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
            <div className="home-page">
                <Challenge filters={filters} />
                <ChallengeFilter onFilterChange={handleFilterChange} />
            </div>
        </div>
    );
}

export default Home;
