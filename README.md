# Hutishtuti - Poker OCR Analyzer

A Python-based Omaha Poker OCR Analyzer that uses optical character recognition (OCR) to detect and analyze poker hands from screenshots of online poker games. The system captures cards during different phases of play (preflop, flop, turn, river) and provides game state tracking.

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

- **OCR Card Detection**: Automatically detects cards from poker table screenshots
- **Multi-Phase Support**: Captures cards during preflop, flop, turn, and river
- **Visual Calibration Tool**: Easy setup for your specific poker client and screen resolution
- **Configuration Management**: Centralized config file for all settings
- **Game State Tracking**: Full Omaha poker game logic with player and table management
- **Color-Based Suit Detection**: Identifies card suits using RGB color sampling
- **Tesseract Integration**: Robust text recognition for card ranks

## Prerequisites

1. **Install Tesseract OCR**:
   - **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

2. **Python 3.7+**

## Setup

1. Clone the repository and navigate to the project directory

2. Create a virtual environment:
```bash
python -m venv .venv
```

3. Activate the virtual environment:
```bash
# On Windows
.venv\Scripts\activate
# On Unix or MacOS
source .venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Configure Tesseract path and card positions:
   - Copy `config.yaml` to `config.local.yaml`
   - Update the Tesseract path in `config.local.yaml`
   - Run calibration tool to set card positions (see below)

## Calibrating Card Positions

Before using the OCR analyzer, you need to calibrate the card positions for your poker client:

### Option 1: Visual Calibration (Recommended)

```bash
# Install matplotlib if not already installed
pip install matplotlib

# Run the visual calibration tool
python calibrate_positions_visual.py
```

Click on the screenshot to select card positions. See [CALIBRATION_GUIDE.md](CALIBRATION_GUIDE.md) for detailed instructions.

### Option 2: Manual Calibration

```bash
python calibrate_positions.py
```

Enter coordinates manually. See [CALIBRATION_GUIDE.md](CALIBRATION_GUIDE.md) for detailed instructions.

## Usage

### Running the OCR Analyzer

```bash
python run_game.py
```

The analyzer will:
1. Wait for you to press Enter at each poker phase
2. Capture a screenshot of your poker table
3. Detect cards using OCR based on the current phase:
   - **Preflop**: Your hole cards
   - **Flop**: Your hole cards + 3 flop cards
   - **Turn**: Turn card
   - **River**: River card
4. Save cropped card images to `card_crops/` for review
5. Display detected cards in the console

### Using OCR Functions Programmatically

```python
from ocr_reader import (
    detect_hand_from_image,
    read_flop_from_image,
    read_turn_from_image,
    read_river_from_image
)

# Detect hole cards
hand = detect_hand_from_image("screenshot.png")
# Returns: [{'number': 'A', 'shape': 'hearts', ...}, ...]

# Detect flop cards
flop = read_flop_from_image("screenshot.png")
# Returns: [card1, card2, card3]

# Detect turn card
turn = read_turn_from_image("screenshot.png")
# Returns: {'number': 'K', 'shape': 'spades', ...}

# Detect river card
river = read_river_from_image("screenshot.png")
# Returns: {'number': '9', 'shape': 'diamonds', ...}
```

## Configuration

All settings are in `config.yaml`. Create `config.local.yaml` to override defaults without affecting version control.

Key configuration options:
- **tesseract.path**: Path to Tesseract executable
- **card_locations**: Screen coordinates for each card position
- **suit_colors**: RGB values for suit color detection
- **ocr.threshold**: Binarization threshold for OCR preprocessing
- **ocr.padding**: Padding around card images
- **ocr.psm_mode**: Tesseract PSM mode (default: 10 for single character)

## Project Structure

```
hutishtuti/
├── config.yaml              # Default configuration
├── ocr_reader.py           # OCR card detection functions
├── run_game.py             # Main entry point
├── calibrate_positions.py  # Manual calibration tool
├── calibrate_positions_visual.py  # Visual calibration tool
├── CALIBRATION_GUIDE.md    # Detailed calibration instructions
├── src/
│   ├── config.py           # Configuration loader
│   └── game/
│       ├── game.py         # Game state management
│       ├── player.py       # Player classes
│       ├── table.py        # Table/pot management
│       └── core/
│           ├── card.py     # Card, Suit, Rank definitions
│           └── hand_evaluator.py  # Hand evaluation logic
└── requirements.txt
```

## Troubleshooting

### OCR Not Detecting Cards

1. Run the calibration tool to verify card positions
2. Check `card_crops/` folder to see what the OCR is seeing
3. Adjust coordinates in `config.yaml` if crops look wrong
4. Ensure Tesseract path is correct in config

### Wrong Card Values Detected

1. Check OCR threshold setting in config (try 170-190)
2. Verify card crops include the rank clearly
3. Make sure poker client cards are visible and not obscured

### Suit Detection Issues

1. Ensure card crops include some colored pixels
2. Adjust `suit_colors` RGB values in config for your poker client's color scheme

## Development

The project uses a modular architecture:
- **OCR Layer**: Card detection and image processing
- **Game Logic**: Poker game state and rules
- **Configuration**: Centralized settings management

## Testing

Run tests using pytest:
```bash
pytest
```

## License

This project is for educational and personal use. 