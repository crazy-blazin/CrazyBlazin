import React from 'react';

const CLIENT_ID = '831465297394401291';
const REDIRECT_URI = 'http://localhost:3000/callback';
const DISCORD_AUTH_URL = `https://discord.com/oauth2/authorize?client_id=831465297394401291&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fcallback&scope=identify`;

const LoginWithDiscord = () => {
    const handleLogin = () => {
        window.location.href = DISCORD_AUTH_URL;
    };

    return (
        <div className="login-container">
            <h2>Welcome to the Slot Machine</h2>
            <button onClick={handleLogin} className="login-button">
                Login with Discord
            </button>
        </div>
    );
};

export default LoginWithDiscord;
