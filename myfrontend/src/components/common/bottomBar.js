import React from 'react';
import './common.css';
import images from '../../images';

function BottomBar() {
    return (
        <div className="bottom-bar">
            <div className="center-content">
                <img src={images.cat_logo} alt="Logo" className="logo" />
                <div className="bottom-text">
                    <p className="site-name">EldenRing Challenge</p>
                    <p className="disclaimer">
                        This is a fan-made website and is not officially affiliated with or endorsed by FromSoftware Inc. or Bandai Namco Entertainment. 
                        Elden Ring is a trademark of FromSoftware Inc. Donations help cover server and maintenance costs.
                    </p>
                </div>
            </div>
        </div>
    );
}

export default BottomBar;
