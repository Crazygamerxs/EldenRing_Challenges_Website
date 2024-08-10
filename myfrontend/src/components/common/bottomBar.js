import React from 'react';
import './common.css';
import images from '../../images'; 


<div class="bottom-bar">
    <div class="center-content">
    <img src={images.cat_logo} alt="cat logo" />
    <p class="text">Some Text</p>
    </div>
</div>
function BottomBar() {
    return (
        <div className="bottom-bar">
            <div className="center-content">
                <img src={images.cat_logo} alt="Logo" className="logo" />
                <p className="text">EldenRing.ca</p>
            </div>
        </div>
    );
}

export default BottomBar;