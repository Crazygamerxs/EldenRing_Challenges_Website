import React from 'react';
import TopBar from '../common/TopBar'; 
import BottomBar from '../common/BottomBar';
import Challenge from './Challenge';
import './Home.css';

function Home() {
    return (
        <div className="home-wrapper">
            <TopBar />
            <div className="home-page">
                <Challenge />
            </div>
            <BottomBar />
        </div>
    );
}

export default Home;
