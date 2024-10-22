import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import SlotMachine from './SlotMachine';
import LoginWithDiscord from './LoginWithDiscord';
import Callback from './Callback';

const App = () => {
    const [user, setUser] = useState(null);

    const handleLogin = (userData) => {
        setUser(userData);
    };

    return (
        <Router>
            <Routes>
                <Route path="/callback" element={<Callback onLogin={handleLogin} />} />
                <Route
                    path="/"
                    element={
                        user ? (
                            <div>
                                <h2>Welcome, {user.username}!</h2>
                                <SlotMachine />
                            </div>
                        ) : (
                            <LoginWithDiscord />
                        )
                    }
                />
                <Route path="*" element={<Navigate to="/" />} />
            </Routes>
        </Router>
    );
};

export default App;
