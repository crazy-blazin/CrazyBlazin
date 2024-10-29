import random
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config.config import SLOT_PAYOUTS, SLOT_WEIGHTS


# Function to simulate a slot machine spin with a 3x3 grid
def spin_slot_machine(bet: int) -> int:
    symbols = list(SLOT_PAYOUTS.keys())
    weights = list(SLOT_WEIGHTS.values())

    # Simulate a 3x3 grid spin
    grid = [
        random.choices(symbols, weights, k=3),
        random.choices(symbols, weights, k=3),
        random.choices(symbols, weights, k=3)
    ]

    # Initialize payout
    payout = 0

    # Check rows
    for row in grid:
        if row.count(row[0]) == 3:
            payout += SLOT_PAYOUTS[row[0]] * bet

    # Check columns
    for col in range(3):
        if grid[0][col] == grid[1][col] == grid[2][col]:
            payout += SLOT_PAYOUTS[grid[0][col]] * bet

    # Check diagonals
    if grid[0][0] == grid[1][1] == grid[2][2]:
        payout += SLOT_PAYOUTS[grid[0][0]] * bet
    if grid[0][2] == grid[1][1] == grid[2][0]:
        payout += SLOT_PAYOUTS[grid[0][2]] * bet

    return payout

# Function to simulate multiple spins
def simulate_slot_machine(bet: int, spins: int):
    ax, fig = plt.subplots(1,2, figsize=(12, 6))
    for _ in range(0,15):
        history = []
        wins = 0
        for _ in range(spins):
            payout = spin_slot_machine(bet)
            history.append(payout - bet)
            if payout > 0:
                wins += 1
            history_cumulative = np.cumsum(history)
        
        # Print the results
        print(f"Total wins: {wins}")

        # Plot the results
        fig[0].plot(history)
        fig[0].set_title(f'Slot Machine Simulation (Bet: {bet})')
        fig[0].set_xlabel('Spins')
        fig[0].set_ylabel('Payout')
        fig[0].grid(True)

        fig[1].plot(history_cumulative)
        fig[1].set_title(f'Slot Machine Simulation (Bet: {bet})')
        fig[1].set_xlabel('Spins')
        fig[1].set_ylabel('Cumulative Payout')
        fig[1].grid(True)

    plt.show()

# Example of simulating with different betting values
simulate_slot_machine(bet=100, spins=250)  # You can adjust the bet and spins here
