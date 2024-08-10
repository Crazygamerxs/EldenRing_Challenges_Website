import React from 'react';
import './common.css'; 
import images from '../../images'; 

const TopBar = () => {
  return (
    <div className="top-bar">
      <div className="left-section">
        <div className='menu-icon'>
            <img src={images.cat_logo} alt="cat logo" />
        </div>
        <h1 className="heading">EldenRing.ca</h1>
      </div>
      <div className='middle-section'>
        <a href="Home" className="nav-link">Challenge</a>
        <a href="#community" className="nav-link">Community Board</a>
      </div>
      <div className="right-section">
        <a href="login" className="nav-link">Login</a>
        <button className="signup-btn">
          <a href="signup" className="signup-link">Sign up</a>
        </button>
      </div>
    </div>
  );
};

export default TopBar;
