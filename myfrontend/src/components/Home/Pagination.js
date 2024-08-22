import React from 'react';
import './Home.css';

const Pagination = ({ currentPage, totalPages, onPageChange }) => {
    const handlePrevious = () => {
        if (currentPage > 1) {
            onPageChange(currentPage - 1);
            window.scrollTo({ top: 0, behavior: 'smooth' }); // Scroll to top
        }
    };

    const handleNext = () => {
        if (currentPage < totalPages) {
            onPageChange(currentPage + 1);
            window.scrollTo({ top: 0, behavior: 'smooth' }); // Scroll to top
        }
    };

    const getPageNumbers = () => {
        const pageNumbers = [];
        const maxPagesToShow = 6;
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

    return (
        <div className="pagination-container">
            <button
                className="pagination-button"
                onClick={handlePrevious}
                disabled={currentPage === 1}
            >
                &lt;
            </button>
            {getPageNumbers().map((page, index) => (
                <button
                    key={index}
                    className={`pagination-button ${page === currentPage ? 'active' : ''}`}
                    onClick={() => typeof page === 'number' && onPageChange(page)}
                >
                    {page}
                </button>
            ))}
            <button
                className="pagination-button"
                onClick={handleNext}
                disabled={currentPage === totalPages}
            >
                &gt;
            </button>
        </div>
    );
};

export default Pagination;
