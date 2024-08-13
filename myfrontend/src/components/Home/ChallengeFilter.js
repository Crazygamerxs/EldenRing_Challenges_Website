import React, { useState, useEffect } from 'react';
import './Home.css';

const ChallengeFilter = ({ onFilterChange }) => {
    const [selectedDifficulties, setSelectedDifficulties] = useState([]);
    const [selectedTypes, setSelectedTypes] = useState([]);

    const handleDifficultyChange = (e) => {
        const value = e.target.value;
        setSelectedDifficulties((prev) =>
            prev.includes(value) ? prev.filter((v) => v !== value) : [...prev, value]
        );
    };

    const handleTypeChange = (e) => {
        const value = parseInt(e.target.value, 10); // Convert to integer
        setSelectedTypes((prev) =>
            prev.includes(value) ? prev.filter((v) => v !== value) : [...prev, value]
        );
    };

    useEffect(() => {
        if (typeof onFilterChange === 'function') {
            // Debounce the filter change to avoid rapid updates
            const timer = setTimeout(() => {
                onFilterChange({
                    difficulties: selectedDifficulties,
                    types: selectedTypes
                });
            }, 300); // Adjust delay as needed

            return () => clearTimeout(timer); // Cleanup timer on component unmount or filter change
        }
    }, [selectedDifficulties, selectedTypes, onFilterChange]);

    return (
        <div className="challenge-filter">
            <h3>Filter</h3>
            <div className="filter-category">
                <h4>DIFFICULTY</h4>
                <label>
                    <input type="checkbox" value="Easy" onChange={handleDifficultyChange} />
                    Easy
                </label>
                <label>
                    <input type="checkbox" value="Medium" onChange={handleDifficultyChange} />
                    Medium
                </label>
                <label>
                    <input type="checkbox" value="Hard" onChange={handleDifficultyChange} />
                    Hard
                </label>
                <label>
                    <input type="checkbox" value="Extreme" onChange={handleDifficultyChange} />
                    Extreme
                </label>
            </div>
            <div className="filter-category">
                <h4>Type's</h4>
                <label>
                    <input type="checkbox" value="1" onChange={handleTypeChange} />
                    General Challenges
                </label>
                <label>
                    <input type="checkbox" value="2" onChange={handleTypeChange} />
                    Basic Weaponry Challenges
                </label>
                <label>
                    <input type="checkbox" value="3" onChange={handleTypeChange} />
                    Advanced Weaponry Challenges
                </label>
                <label>
                    <input type="checkbox" value="4" onChange={handleTypeChange} />
                    Advance Spell Challenges
                </label>
                <label>
                    <input type="checkbox" value="5" onChange={handleTypeChange} />
                    Extreme Weaponry/Spell Challenges
                </label>
                <label>
                    <input type="checkbox" value="6" onChange={handleTypeChange} />
                    Status Challenges
                </label>
                <label>
                    <input type="checkbox" value="7" onChange={handleTypeChange} />
                    Crafting and Item Challenges
                </label>
                <label>
                    <input type="checkbox" value="8" onChange={handleTypeChange} />
                    Healing and FP Recovery Challenges
                </label>
                <label>
                    <input type="checkbox" value="9" onChange={handleTypeChange} />
                    Level/Stat Challenges
                </label>
                <label>
                    <input type="checkbox" value="10" onChange={handleTypeChange} />
                    Challenges for the Brave or Insane
                </label>
            </div>
        </div>
    );
};

export default ChallengeFilter;
