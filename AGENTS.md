# 52 Card Pick - Development Guide

## Running the Game

```bash
# Activate virtual environment
source .venv/bin/activate

# Run game
python 52_card_pick.py
```

## Project Structure

- `52_card_pick.py` - Single-file Tkinter game (no external dependencies)
- `.venv/` - Python virtual environment

## Notes

- Uses built-in `tkinter` - no pip packages required
- Game state: cards start face-up randomly, click to move to deck pile (top-left)
- Score: +10 points per card collected
- Menu: New Game, Score view, Quit
