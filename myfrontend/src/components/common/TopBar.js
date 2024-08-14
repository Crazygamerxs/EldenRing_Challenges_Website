import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import './common.css'; 
import images from '../../images';
import { UserContext } from '../common/UserContext'; 

const TopBar = () => {
  const { user, logout } = useContext(UserContext);
  return (
    <div className="top-bar">
      <div className="left-section">
        <div className='menu-icon'>
            <img src={images.cat_logo} alt="cat logo" />
        </div>
        <Link to="/home" className="nav-link">
          <h1 className="heading">EldenRing.ca</h1>
        </Link>
      </div>
      <div className='middle-section'>
        <Link to="/home" className="nav-link">Challenge</Link>
        <Link to="/CB" className="nav-link">Community Board</Link>
      </div>
      <div className="right-section">
        {user ? (
          <>
            <span className="nav-link">Hey, {user.username}</span>
            <button onClick={logout} className="logout-btn">Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" className="nav-link">Login</Link>
            <button className="signup-btn">
              <Link to="/signup" className="signup-link">Sign up</Link>
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default TopBar;
