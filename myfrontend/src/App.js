import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SignUp from './components/SignUp/SignUp'; // Adjust path as needed

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/SignUp" element={<SignUp />} />
        {/* Add other routes here */}
      </Routes>
    </Router>
  );
}

export default App;
