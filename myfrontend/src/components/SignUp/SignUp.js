import React from 'react';
import TopBar from '../common/TopBar'; 
import BottomBar from '../common/BottomBar';
import './SignUp.css';
import images from '../../images'; 

const SignUp = () => {
  return (
    <div>
      <TopBar />
      <div className='signup-page'>
        <div className="sign-up-content">
          <h2>SIGN UP FOR ELDENRING.CA</h2>
          <form>
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input type="text" id="username" name="username" required />
            </div>
            <div className="form-group">
              <label htmlFor="email">Email Address</label>
              <input type="email" id="email" name="email" required />
            </div>
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input type="password" id="password" name="password" required />
            </div>
            <div className="form-actions">
              <button type="submit">Sign Up</button>
              <button type="button">Already have an account?</button>
            </div>
          </form>
          <div className="google-signup-bar">
            <img src={images.google} alt="Google Logo" />
            <span>Log in with Google</span>
          </div>
        </div>
      </div>
      <BottomBar />
    </div>
  );
};

export default SignUp;
