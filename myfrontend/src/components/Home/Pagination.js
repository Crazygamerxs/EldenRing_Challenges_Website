import React from 'react';
import './Home.css';

import { API_ENDPOINTS } from '../../utils/api';
const Pagination = ({ currentPage, totalPages, onPageChange }) => {
    // Scroll to top function
    const scrollToTop = () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const handlePrevious = () => {
        if (currentPage > 1) {
            onPageChange(currentPage - 1);
            scrollToTop();
        }
    };

    const handleNext = () => {
        if (currentPage < totalPages) {
            onPageChange(currentPage + 1);
            scrollToTop();
        }
    };

    // Handle page number click - FIXED VERSION
    const handlePageClick = (page) => {
        if (typeof page === 'number') {
            onPageChange(page);
            scrollToTop(); // Always scroll to top, regardless of current page
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

    // Don't render pagination if there's only one page or no pages
    if (totalPages <= 1) {
        return null;
    }

    return (
        <div className="pagination-container">
            <button
                className="pagination-button"
                onClick={handlePrevious}
                disabled={currentPage === 1}
                title="Previous page"
            >
                &lt;
            </button>
            {getPageNumbers().map((page, index) => (
                <button
                    key={index}
                    className={`pagination-button ${page === currentPage ? 'active' : ''} ${page === '...' ? 'ellipsis' : ''}`}
                    onClick={() => handlePageClick(page)}
                    disabled={page === '...'}
                    title={typeof page === 'number' ? `Go to page ${page}` : ''}
                >
                    {page}
                </button>
            ))}
            <button
                className="pagination-button"
                onClick={handleNext}
                disabled={currentPage === totalPages}
                title="Next page"
            >
                &gt;
            </button>
        </div>
    );
};

export default Pagination;