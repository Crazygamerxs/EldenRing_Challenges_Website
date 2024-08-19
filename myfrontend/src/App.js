import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SignUp from './components/SignUp/SignUp';
import Login from './components/Login/Login';
import Home from './components/Home/Home';
import ChallengeDetail from './components/ChallengeDetail/ChallengeDetail';
import CommunityBoard from './components/CB/CB';
import CommunityForum from './components/CB/CommunityForum';
import ThreadPage from './components/CB/ThreadPage';
import LoadingIndicator from './components/common/LoadingIndicator';
import TopBar from './components/common/TopBar';
import BottomBar from './components/common/BottomBar';
import { UserProvider } from './components/common/UserContext';
import RouteLoader from './components/common/RouteLoader';
import PrivateRoute from './components/common/PrivateRoute'; // Import PrivateRoute

const App = () => {
    const [isLoading, setIsLoading] = useState(false);

    return (
        <UserProvider>
            <Router>
                <TopBar />
                <LoadingIndicator isVisible={isLoading} />
                <Routes>
                    <Route path="/home" element={<Home />} />
                    <Route path="/signup" element={<SignUp />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/challenge/:id" element={<ChallengeDetail />} />
                    <Route path="/CB" element={<CommunityBoard />} />
                    <Route path="/forum/:forumId" element={<PrivateRoute element={<CommunityForum />} />} />
                    <Route path="/thread/:threadId" element={<PrivateRoute element={<ThreadPage />} />} />
                </Routes>
                <BottomBar />
                <RouteLoader setIsLoading={setIsLoading} />
            </Router>
        </UserProvider>
    );
};

export default App;
