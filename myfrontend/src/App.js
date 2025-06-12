import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SignUp from './components/SignUp/SignUp';
import Login from './components/Login/Login';
import PasswordResetConfirm from './components/Login/PasswordResetConfirm';
import PasswordResetRequest from './components/Login/PasswordResetRequest';
import Home from './components/Home/Home';
import ChallengeDetail from './components/ChallengeDetail/ChallengeDetail';
import Leaderboard from './components/Leaderboard/Leaderboard';
// UserProfile removed
import Notifications from './components/Notifications/Notifications';
import CommunityBoard from './components/CB/CB';
import CommunityForum from './components/CB/CommunityForum';
import ThreadPage from './components/CB/ThreadPage';
import AdminPanel from './components/Admin/AdminPanel';
import AdminSubmissions from './components/Admin/AdminSubmissions';
import AdminChallenges from './components/Admin/AdminChallenges';
import AdminUsers from './components/Admin/AdminUsers';
import AdminSettings from './components/Admin/AdminSettings';
import LoadingIndicator from './components/common/LoadingIndicator';
import TopBar from './components/common/TopBar';
import BottomBar from './components/common/bottomBar';
import { UserProvider } from './components/common/UserContext';
import { NotificationProvider } from './components/common/NotificationContext';
import RouteLoader from './components/common/RouteLoader';
import PrivateRoute from './components/common/PrivateRoute';
import AdminRoute from './components/common/AdminRoute';
import CSRFTOKEN from "./components/common/CSRFToken";
import ErrorBoundary from './components/common/ErrorBoundary';
import { initializeSecurity } from './utils/security';

const App = () => {
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        initializeSecurity();
    }, []);

    return (
        <ErrorBoundary showDetails={process.env.NODE_ENV === 'development'}>
            <UserProvider>
                <NotificationProvider>
                    <Router>
                        <TopBar />
                        <CSRFTOKEN />
                        <LoadingIndicator isVisible={isLoading} />
                        <Routes>
                            <Route path="/" element={<Home />} />
                            <Route path="/home" element={<Home />} />
                            <Route path="/signup" element={<SignUp />} />
                            <Route path="/login" element={<Login />} />
                            <Route path="/password-reset" element={<PasswordResetRequest />} />
                            <Route path="/password-reset-confirm/:uidb64/:token" element={<PasswordResetConfirm />} />
                            <Route path="/challenge/:id" element={<ChallengeDetail />} />
                            <Route path="/leaderboard" element={<Leaderboard />} />
            {/* UserProfile route removed */}
                            <Route path="/notifications" element={<PrivateRoute element={<Notifications />} />} />
                            
                            {/* Admin Routes - Protected with AdminRoute */}
                            <Route path="/admin" element={<AdminRoute element={<AdminPanel />} />} />
                            <Route path="/admin/submissions" element={<AdminRoute element={<AdminSubmissions />} />} />
                            <Route path="/admin/challenges" element={<AdminRoute element={<AdminChallenges />} />} />
                            <Route path="/admin/users" element={<AdminRoute element={<AdminUsers />} />} />
                            <Route path="/admin/settings" element={<AdminRoute element={<AdminSettings />} />} />
                            
                            {/* Community Board Routes - Hidden but kept for future use */}
                            <Route path="/CB" element={<CommunityBoard />} />
                            <Route path="/forum/:forumId" element={<PrivateRoute element={<CommunityForum />} />} />
                            <Route path="/thread/:threadId" element={<PrivateRoute element={<ThreadPage />} />} />
                        </Routes>
                        <BottomBar />
                        <RouteLoader setIsLoading={setIsLoading} />
                    </Router>
                </NotificationProvider>
            </UserProvider>
        </ErrorBoundary>
    );
};

export default App;
