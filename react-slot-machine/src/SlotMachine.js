import React, { useState } from 'react';
import './SlotMachine.css';

// Define the slot machine's symbol probabilities
const SLOT_WEIGHTS = {
    "7️⃣": 0.01,
    "⭐": 0.05,
    "🔔": 0.05,
    "🍇": 0.10,
    "🍉": 0.10,
    "🍊": 0.20,
    "🍋": 0.20,
    "🍒": 0.29
};

const symbols = Object.keys(SLOT_WEIGHTS);

const getRandomSymbol = (weights) => {
    let totalWeight = 0;
    let random = Math.random();

    for (let symbol of symbols) {
        totalWeight += weights[symbol];
        if (random <= totalWeight) {
            return symbol;
        }
    }
    return "🍒"; // Default if no match
};

const SlotMachine = () => {
    const [reels, setReels] = useState([
        ["🍒", "🍒", "🍒"],
        ["🍒", "🍒", "🍒"],
        ["🍒", "🍒", "🍒"]
    ]);

    const [isSpinning, setIsSpinning] = useState(false);
    const [message, setMessage] = useState("");

    // Load the sounds
    const spinSound = new Audio("/spin.wav");
    const winSound = new Audio("/win.wav");

    const spinReels = () => {
        setIsSpinning(true);
        setMessage("");

        // Play spin sound when spinning starts
        spinSound.play();

        let spinDuration = 4000; // Total spin duration of 4 seconds
        let currentSpinTime = 0;
        let interval = 100; // Initial speed of symbol change

        const slowDownSpin = () => {
            if (currentSpinTime < spinDuration) {
                setReels([
                    [getRandomSymbol(SLOT_WEIGHTS), getRandomSymbol(SLOT_WEIGHTS), getRandomSymbol(SLOT_WEIGHTS)],
                    [getRandomSymbol(SLOT_WEIGHTS), getRandomSymbol(SLOT_WEIGHTS), getRandomSymbol(SLOT_WEIGHTS)],
                    [getRandomSymbol(SLOT_WEIGHTS), getRandomSymbol(SLOT_WEIGHTS), getRandomSymbol(SLOT_WEIGHTS)]
                ]);

                interval += 20; // Increase delay (slows down)
                currentSpinTime += interval;

                setTimeout(slowDownSpin, interval);
            } else {
                setIsSpinning(false);
                calculateResult();
            }
        };

        slowDownSpin();
    };

    const calculateResult = () => {
        const finalReels = [
            [getRandomSymbol(SLOT_WEIGHTS), getRandomSymbol(SLOT_WEIGHTS), getRandomSymbol(SLOT_WEIGHTS)],
            [getRandomSymbol(SLOT_WEIGHTS), getRandomSymbol(SLOT_WEIGHTS), getRandomSymbol(SLOT_WEIGHTS)],
            [getRandomSymbol(SLOT_WEIGHTS), getRandomSymbol(SLOT_WEIGHTS), getRandomSymbol(SLOT_WEIGHTS)]
        ];
        setReels(finalReels);

        if (
            (finalReels[0][0] === finalReels[0][1] && finalReels[0][1] === finalReels[0][2]) ||
            (finalReels[1][0] === finalReels[1][1] && finalReels[1][1] === finalReels[1][2]) ||
            (finalReels[2][0] === finalReels[2][1] && finalReels[2][1] === finalReels[2][2])
        ) {
            setMessage("🎉 You won! 🎉");

            // Play win sound if the user wins
            winSound.play();
        } else {
            setMessage("Try again!");
        }
    };

    return (
        <div className="slot-machine-container">
            <h1 className="slot-title">Slot Machine</h1>

            <div className="reels-grid">
                {reels.flat().map((symbol, index) => (
                    <div key={index} className="reel">
                        {symbol}
                    </div>
                ))}
            </div>

            <button
                className="spin-button"
                onClick={spinReels}
                disabled={isSpinning}
            >
                {isSpinning ? "Spinning..." : "Spin"}
            </button>

            <p className="result-message">{message}</p>
        </div>
    );
};

export default SlotMachine;
