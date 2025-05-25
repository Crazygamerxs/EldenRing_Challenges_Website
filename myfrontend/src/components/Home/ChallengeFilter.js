import React, { useState, useEffect } from 'react';
import './Home.css';

const ChallengeFilter = ({ onFilterChange }) => {
    const [selectedDifficulties, setSelectedDifficulties] = useState([]);
    const [selectedTypes, setSelectedTypes] = useState([]);
    const [selectedDLC, setSelectedDLC] = useState([]);
    const [selectedCombination, setSelectedCombination] = useState([]);

    const handleDifficultyChange = (e) => {
        const value = e.target.value;
        setSelectedDifficulties((prev) =>
            prev.includes(value) ? prev.filter((v) => v !== value) : [...prev, value]
        );
    };

    const handleTypeChange = (e) => {
        const value = parseInt(e.target.value, 10);
        setSelectedTypes((prev) =>
            prev.includes(value) ? prev.filter((v) => v !== value) : [...prev, value]
        );
    };

    const handleDLCChange = (e) => {
        const value = e.target.value;
        setSelectedDLC((prev) =>
            prev.includes(value) ? prev.filter((v) => v !== value) : [...prev, value]
        );
    };

    const handleCombinationChange = (e) => {
        const value = e.target.value;
        setSelectedCombination((prev) =>
            prev.includes(value) ? prev.filter((v) => v !== value) : [...prev, value]
        );
    };

    // Clear all filters function
    const clearAllFilters = () => {
        setSelectedDifficulties([]);
        setSelectedTypes([]);
        setSelectedDLC([]);
        setSelectedCombination([]);
    };

    useEffect(() => {
        if (typeof onFilterChange === 'function') {
            const timer = setTimeout(() => {
                onFilterChange({
                    difficulties: selectedDifficulties,
                    types: selectedTypes,
                    dlc: selectedDLC,
                    combination: selectedCombination
                });
            }, 300);

            return () => clearTimeout(timer);
        }
    }, [selectedDifficulties, selectedTypes, selectedDLC, selectedCombination, onFilterChange]);

    return (
        <div className="challenge-filter">
            <div className="filter-header">
                <h3>Filter</h3>
                <button className="clear-filters-btn" onClick={clearAllFilters}>
                    Clear All
                </button>
            </div>
            
            <div className="filter-category">
                <h4>DIFFICULTY</h4>
                <label>
                    <input type="checkbox" value="Easy" onChange={handleDifficultyChange} 
                           checked={selectedDifficulties.includes("Easy")} />
                    Easy
                </label>
                <label>
                    <input type="checkbox" value="Medium" onChange={handleDifficultyChange} 
                           checked={selectedDifficulties.includes("Medium")} />
                    Medium
                </label>
                <label>
                    <input type="checkbox" value="Hard" onChange={handleDifficultyChange} 
                           checked={selectedDifficulties.includes("Hard")} />
                    Hard
                </label>
                <label>
                    <input type="checkbox" value="Extreme" onChange={handleDifficultyChange} 
                           checked={selectedDifficulties.includes("Extreme")} />
                    Extreme
                </label>
            </div>

            {/* <div className="filter-category">
                <h4>CONTENT TYPE</h4>
                <label>
                    <input type="checkbox" value="base" onChange={handleDLCChange} 
                           checked={selectedDLC.includes("base")} />
                    Base Game Only
                </label>
                <label>
                    <input type="checkbox" value="dlc" onChange={handleDLCChange} 
                           checked={selectedDLC.includes("dlc")} />
                    DLC Content
                </label>
            </div> */}

            {/* <div className="filter-category">
                <h4>CHALLENGE TYPE</h4>
                <label>
                    <input type="checkbox" value="single" onChange={handleCombinationChange} 
                           checked={selectedCombination.includes("single")} />
                    Single Challenges
                </label>
                <label>
                    <input type="checkbox" value="combination" onChange={handleCombinationChange} 
                           checked={selectedCombination.includes("combination")} />
                    Challenge Combinations
                </label>
            </div> */}
            
            <div className="filter-category">
                <h4>CATEGORIES</h4>
                <label>
                    <input type="checkbox" value="1" onChange={handleTypeChange} 
                           checked={selectedTypes.includes(1)} />
                    General Challenges
                </label>
                <label>
                    <input type="checkbox" value="2" onChange={handleTypeChange} 
                           checked={selectedTypes.includes(2)} />
                    Basic Weaponry Challenges
                </label>
                <label>
                    <input type="checkbox" value="3" onChange={handleTypeChange} 
                           checked={selectedTypes.includes(3)} />
                    Advanced Weaponry Challenges
                </label>
                <label>
                    <input type="checkbox" value="4" onChange={handleTypeChange} 
                           checked={selectedTypes.includes(4)} />
                    Advanced Spell Challenges
                </label>
                <label>
                    <input type="checkbox" value="5" onChange={handleTypeChange} 
                           checked={selectedTypes.includes(5)} />
                    Extreme Weaponry/Spell Challenges
                </label>
                <label>
                    <input type="checkbox" value="6" onChange={handleTypeChange} 
                           checked={selectedTypes.includes(6)} />
                    Status Challenges
                </label>
                <label>
                    <input type="checkbox" value="7" onChange={handleTypeChange} 
                           checked={selectedTypes.includes(7)} />
                    Crafting and Item Challenges
                </label>
                <label>
                    <input type="checkbox" value="8" onChange={handleTypeChange} 
                           checked={selectedTypes.includes(8)} />
                    Healing and FP Recovery Challenges
                </label>
                <label>
                    <input type="checkbox" value="9" onChange={handleTypeChange} 
                           checked={selectedTypes.includes(9)} />
                    Level/Stats Challenges
                </label>
                <label>
                    <input type="checkbox" value="10" onChange={handleTypeChange} 
                           checked={selectedTypes.includes(10)} />
                    Challenges for the Brave or Insane
                </label>
                <label>
                    <input type="checkbox" value="11" onChange={handleTypeChange} 
                           checked={selectedTypes.includes(11)} />
                    Challenge Combinations
                </label>
            </div>
        </div>
    );
};

export default ChallengeFilter;