// server.js (Node.js backend)
const express = require('express');
const axios = require('axios');
const app = express();
const port = 3001;

const CLIENT_ID = '831465297394401291';
const REDIRECT_URI = 'http://localhost:3000/callback';
const DISCORD_AUTH_URL = `https://discord.com/oauth2/authorize?client_id=831465297394401291&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fcallback&scope=identify`;

app.get('/login', (req, res) => {
    const redirectUrl = `https://discord.com/oauth2/authorize?client_id=${CLIENT_ID}&redirect_uri=${encodeURIComponent(REDIRECT_URI)}&response_type=code&scope=identify`;
    res.redirect(redirectUrl);
});

app.get('/callback', async (req, res) => {
    const code = req.query.code;

    try {
        const tokenResponse = await axios.post(
            'https://discord.com/api/oauth2/token',
            new URLSearchParams({
                client_id: CLIENT_ID,
                client_secret: CLIENT_SECRET,
                grant_type: 'authorization_code',
                code: code,
                redirect_uri: REDIRECT_URI,
            }),
            { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
        );

        const accessToken = tokenResponse.data.access_token;

        const userResponse = await axios.get('https://discord.com/api/users/@me', {
            headers: { Authorization: `Bearer ${accessToken}` },
        });

        const user = userResponse.data;
        res.redirect(`http://localhost:3000?username=${user.username}`);
    } catch (error) {
        console.error(error);
        res.send('Error during Discord OAuth');
    }
});

app.listen(port, () => {
    console.log(`Backend listening at http://localhost:${port}`);
});
