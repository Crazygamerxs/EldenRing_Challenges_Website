import React from 'react';
import TopBar from '../common/TopBar'; 
import BottomBar from '../common/BottomBar';
import './Login.css';
import images from '../../images'; 

const LogIn = () => {
  return (
    <div>
      <TopBar />
      <div className='login-page'>
        <div className="login-content">
          <h2>LOGIN TO ELDENRING.CA</h2>
          <form>
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input type="text" id="username" name="username" required />
            </div>
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input type="password" id="password" name="password" required />
            </div>
            <div className="form-actions">
              <button type="login">Log In</button>
              <button type="button">Already have an account?</button>
            </div>
          </form>
          <div className="google-login-bar">
            <img src={images.google} alt="Google Logo" />
            <span>Log in with Google</span>
          </div>
        </div>
      </div>
      <BottomBar />
    </div>
  );
};

export default LogIn;
