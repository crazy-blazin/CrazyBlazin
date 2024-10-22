// Callback.js
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Callback = ({ onLogin }) => {
    const navigate = useNavigate();

    useEffect(() => {
        // Simulate an async login callback (e.g., fetching from Discord API)
        const fetchUserData = async () => {
            try {
                // Replace this with your actual API call logic
                const userData = await simulateFetchUserData();

                if (userData) {
                    console.log('User data:', userData);
                    onLogin(userData);  // Set user data in parent component
                    navigate('/');  // Redirect to the home page after login
                }
            } catch (error) {
                console.error('Login failed', error);
                navigate('/');  // Redirect to home on failure
            }
        };

        fetchUserData();
    }, [onLogin, navigate]);

    const simulateFetchUserData = () => {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({ username: 'TestUser' });
            }, 500);  // Simulate a 2-second API call
        });
    };

    return <div>Loading...</div>;
};

export default Callback;
