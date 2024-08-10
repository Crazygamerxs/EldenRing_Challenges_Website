import React from 'react';
import TopBar from '../common/TopBar'; 
import BottomBar from '../common/BottomBar';
import './Home.css';
import images from '../../images'; 

function Home() {
    return (
        <div>
        <TopBar />
        <div className='home-page'>
            <h1>Welcome to the Elden Ring Challenges Website!</h1>
            <p>Start exploring the challenges and embark on your journey.</p>
        </div>
        <BottomBar />
        </div>
    );
}

export default Home;