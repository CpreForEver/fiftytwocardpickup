# 52 Card Pick

A fast-paced card collection game built with Python and Tkinter!

## How to Play

1. **Objective**: Collect all 52 cards by clicking on them
2. **Scoring**: +10 points per card collected
3. **Win Condition**: Collect all cards within the time limit
4. **Card Pile**: Cards stack in a pile at the top-left. When the pile exceeds 5 cards, it resets to the starting position

## Controls

- **Click** on any face-up card to collect it (+10 points)
- **File Menu**: Access game options (New Game, Score, Quit)

## Gameplay

- Cards are randomly placed across the green felt table
- Each card shows its rank and suit (red for Hearts/Diamonds, black for Clubs/Spades)
- Click cards to move them into the deck pile at top-left
- Watch your score increase as you collect cards!

## Game Screenshot

![52 Card Pick](resources/game_screenshot.png)

## Requirements

- Python 3.x
- Tkinter (included with Python)

## How to Run

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the game
python 52_card_pick.py
```

## Features

- 🎮 Single-file implementation (no external dependencies)
- ⏱️ Time-based gameplay challenge
- 🃏 Realistic card styling with suit colors
- 📊 Score tracking and menu system
- 🏆 Win screen with replay option

---

**Created for 52 Card Pick Challenge**
