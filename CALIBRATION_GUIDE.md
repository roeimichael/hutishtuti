# Card Position Calibration Guide

This guide explains how to calibrate the card positions for your specific poker client and screen resolution.

## Why Calibrate?

The OCR system needs to know exactly where cards appear on your screen. Different poker clients, screen resolutions, and window sizes mean the coordinates will be different for each setup.

## Two Calibration Methods

### Method 1: Visual Calibration (Recommended)

**Requirements:** `matplotlib` library

**Advantages:**
- Click directly on the screenshot to select positions
- Visual feedback in real-time
- Easier and faster

**How to use:**

1. Install matplotlib (if not already installed):
   ```bash
   pip install matplotlib
   ```

2. Run the visual calibration tool:
   ```bash
   python calibrate_positions_visual.py
   ```

3. Follow the on-screen instructions:
   - The tool will take a screenshot of your poker table
   - For each card position, click TWO points:
     - First: Top-left corner of the card rank area
     - Second: Bottom-right corner of the card rank area
   - A preview will be saved automatically
   - Type 'y' if the crop looks good, 'n' to try again

4. When finished, copy the coordinates from the output to your `config.yaml`

### Method 2: Manual Calibration

**Requirements:** None (basic Python only)

**Advantages:**
- Works without additional dependencies
- More control over exact pixel coordinates

**How to use:**

1. Run the manual calibration tool:
   ```bash
   python calibrate_positions.py
   ```

2. The tool will take a screenshot and save it

3. Open the screenshot in an image editor (Paint, GIMP, Preview, etc.)

4. For each card position:
   - Find the pixel coordinates of the top-left corner
   - Find the pixel coordinates of the bottom-right corner
   - Enter them when prompted: `left, top, right, bottom`
   - A preview will be saved to `calibration_crops/`
   - Check the preview and confirm or retry

5. Copy the final coordinates to your `config.yaml`

## What to Calibrate

You need to calibrate 7 card positions:

1. **card1** - Your left hole card
2. **card2** - Your right hole card
3. **flop1** - First flop card
4. **flop2** - Second flop card
5. **flop3** - Third flop card
6. **turn** - Turn card
7. **river** - River card

## Tips for Best Results

### 1. Card Crop Area

The crop should include:
- The card **rank** (number or face: A, K, Q, J, 10, 9, etc.)
- Enough of the card to sample the **suit color**

The crop should NOT include:
- The entire card (too much white space)
- Other UI elements
- Parts of adjacent cards

### 2. Optimal Crop Size

A good crop is usually:
- **Width:** 30-60 pixels
- **Height:** 40-80 pixels

Too small = OCR might miss the rank
Too large = OCR gets confused by extra details

### 3. Consistent Setup

For best results:
- Use the same poker client window size every time
- Don't move or resize the poker client window
- Keep the same screen resolution

### 4. Testing Your Calibration

After calibrating:

1. Check the preview images in `calibration_crops/`:
   - `card_name_preview.png` - Actual size crop
   - `card_name_preview_large.png` - 4x enlarged for easier viewing
   - `annotated_screenshot.png` - Shows all positions on the original screenshot

2. The rank (A, K, Q, J, 10, 2, 3, etc.) should be clearly visible
3. There should be visible colored pixels for suit detection

### 5. Troubleshooting

**OCR reads wrong values:**
- Crop might be too small or too large
- Adjust the coordinates to include just the rank area

**Suit detection wrong:**
- Make sure the crop includes some colored pixels
- The suit color sampling looks for the darkest (non-white) pixel

**No cards detected:**
- Coordinates might be completely wrong
- Run calibration again and double-check the preview images

## After Calibration

1. Open `config.yaml` (or `config.local.yaml` if you created one)

2. Update the `card_locations` section with your new coordinates:

```yaml
card_locations:
  card1: [880, 770, 915, 810]
  card2: [945, 770, 985, 810]
  flop1: [592, 320, 652, 400]
  flop2: [662, 320, 722, 400]
  flop3: [732, 320, 792, 400]
  turn:  [802, 320, 862, 400]
  river: [872, 320, 932, 400]
```

3. Test your setup:
   ```bash
   python run_game.py
   ```

4. If detection is still not accurate, re-run calibration and fine-tune the coordinates

## Output Files

After calibration, you'll find:

- `calibration_screenshots/` - Original screenshots taken
- `calibration_crops/` - Preview crops of each card position
- `calibration_coords.txt` - Final coordinates in YAML format
- `annotated_screenshot.png` - Visual reference showing all positions

Keep these files for reference when troubleshooting!
