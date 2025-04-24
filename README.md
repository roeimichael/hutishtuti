# Omaha Poker Game

A Python implementation of Omaha poker with a twist. This project provides the core game logic and backend functionality for a poker game.

## Project Structure

```
src/
├── game/
│   ├── __init__.py
│   ├── game.py
│   ├── player.py
│   └── core/
│       ├── __init__.py
│       ├── card.py
│       ├── deck.py
│       └── hand_evaluator.py
```

## Features

- Full Omaha poker game logic
- Card and deck management
- Hand evaluation
- Player management
- Betting system
- Pot management

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
```

2. Activate the virtual environment:
```bash
# On Windows
.venv\Scripts\activate
# On Unix or MacOS
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```python
from game import Game, Player

# Create a game
game = Game(small_blind=5, big_blind=10)

# Add players
player1 = Player("Player1", chips=1000)
player2 = Player("Player2", chips=1000)
game.add_player(player1)
game.add_player(player2)

# Start a new hand
game.start_new_hand()

# Process player actions
game.process_player_action(player1, "call")
game.process_player_action(player2, "raise", amount=20)
```

## Development

The project is structured to make it easy to add new features and modifications. The core game logic is separated from the player management and betting system, making it simple to implement your own twist on the game.

## Testing

Run tests using pytest:
```bash
pytest
``` 