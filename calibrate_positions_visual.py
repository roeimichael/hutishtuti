"""
Visual Card Position Calibration Tool (Enhanced)

This script provides a visual interface to calibrate card positions by clicking
on the screenshot. Requires matplotlib.

If matplotlib is not available, use calibrate_positions.py instead.
"""

import os
from PIL import Image
from datetime import datetime

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("ERROR: matplotlib is required for visual calibration.")
    print("Install it with: pip install matplotlib")
    print("Or use calibrate_positions.py for manual calibration.")
    exit(1)


class VisualCalibrator:
    def __init__(self, screenshot_path):
        self.screenshot_path = screenshot_path
        self.img = Image.open(screenshot_path)
        self.current_card = None
        self.coords = {}
        self.click_points = []

        self.card_order = ['card1', 'card2', 'flop1', 'flop2', 'flop3', 'turn', 'river']
        self.current_index = 0

        self.fig, self.ax = None, None
        self.rect_patch = None

    def onclick(self, event):
        """Handle mouse click events."""
        if event.xdata is None or event.ydata is None:
            return

        x, y = int(event.xdata), int(event.ydata)
        self.click_points.append((x, y))

        print(f"Point {len(self.click_points)}: ({x}, {y})")

        if len(self.click_points) == 1:
            print("Click the bottom-right corner of the card...")
        elif len(self.click_points) == 2:
            # Two points collected, create rectangle
            p1, p2 = self.click_points
            left = min(p1[0], p2[0])
            top = min(p1[1], p2[1])
            right = max(p1[0], p2[0])
            bottom = max(p1[1], p2[1])

            coords = (left, top, right, bottom)
            self.coords[self.current_card] = coords

            # Draw rectangle on the plot
            self.draw_rectangle(coords)

            print(f"\n[OK] {self.current_card.upper()} position set: {coords}")
            print(f"  Size: {right-left}x{bottom-top} pixels")

            # Show preview
            self.show_preview(coords)

            # Ask if satisfied
            self.ask_satisfaction()

    def draw_rectangle(self, coords, color='green'):
        """Draw a rectangle on the plot."""
        left, top, right, bottom = coords
        width = right - left
        height = bottom - top

        if self.rect_patch:
            self.rect_patch.remove()

        self.rect_patch = patches.Rectangle(
            (left, top), width, height,
            linewidth=2, edgecolor=color, facecolor='none'
        )
        self.ax.add_patch(self.rect_patch)

        # Add label
        self.ax.text(left, top - 10, self.current_card.upper(),
                    color=color, fontsize=12, fontweight='bold',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        self.fig.canvas.draw()

    def show_preview(self, coords):
        """Show a preview of the cropped card."""
        crop = self.img.crop(coords)

        # Save preview
        os.makedirs("calibration_crops", exist_ok=True)
        preview_path = f"calibration_crops/{self.current_card}_preview.png"

        # Save at 4x size for easy viewing
        preview_size = (crop.width * 4, crop.height * 4)
        preview = crop.resize(preview_size, Image.NEAREST)
        preview.save(preview_path)

        print(f"  Preview saved to: {preview_path}")

    def ask_satisfaction(self):
        """Ask if user is satisfied with the position."""
        plt.pause(0.1)  # Let the plot update

        response = input("\nAre you satisfied with this position? (y/n/q to quit): ").strip().lower()

        if response == 'q':
            self.save_and_exit()
            return
        elif response == 'y':
            # Move to next card
            self.current_index += 1
            if self.current_index < len(self.card_order):
                self.start_next_card()
            else:
                # All cards done
                self.save_and_exit()
        else:
            # Redo this card
            print("\nLet's try again for this card...")
            self.click_points = []
            if self.rect_patch:
                self.rect_patch.remove()
                self.rect_patch = None
            self.fig.canvas.draw()
            print(f"\nClick the top-left corner of {self.current_card.upper()}...")

    def start_next_card(self):
        """Start calibrating the next card."""
        self.current_card = self.card_order[self.current_index]
        self.click_points = []

        print("\n" + "="*60)
        print(f"Card {self.current_index + 1}/{len(self.card_order)}: {self.current_card.upper()}")
        print("="*60)
        print("Click the top-left corner of the card...")

    def save_and_exit(self):
        """Save coordinates and exit."""
        print("\n" + "="*60)
        print("CALIBRATION COMPLETE!")
        print("="*60)

        # Create annotated screenshot with all rectangles
        self.ax.clear()
        self.ax.imshow(self.img)
        self.ax.axis('off')

        colors = {
            'card1': 'green', 'card2': 'green',
            'flop1': 'blue', 'flop2': 'blue', 'flop3': 'blue',
            'turn': 'yellow', 'river': 'red'
        }

        for card_name, coords in self.coords.items():
            left, top, right, bottom = coords
            width = right - left
            height = bottom - top
            color = colors.get(card_name, 'white')

            rect = patches.Rectangle(
                (left, top), width, height,
                linewidth=2, edgecolor=color, facecolor='none'
            )
            self.ax.add_patch(rect)
            self.ax.text(left, top - 10, card_name.upper(),
                        color=color, fontsize=10, fontweight='bold',
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        plt.title("All Card Positions", fontsize=14, fontweight='bold')
        annotated_path = "calibration_crops/annotated_screenshot.png"
        plt.savefig(annotated_path, dpi=150, bbox_inches='tight')
        print(f"\n[OK] Annotated screenshot saved to: {annotated_path}")

        # Output YAML format
        print("\nAdd these coordinates to your config.yaml file:\n")
        print("card_locations:")
        for card_name in self.card_order:
            if card_name in self.coords:
                coords = self.coords[card_name]
                print(f"  {card_name}: [{coords[0]}, {coords[1]}, {coords[2]}, {coords[3]}]")

        # Save to file
        output_file = "calibration_coords.txt"
        with open(output_file, 'w') as f:
            f.write("card_locations:\n")
            for card_name in self.card_order:
                if card_name in self.coords:
                    coords = self.coords[card_name]
                    f.write(f"  {card_name}: [{coords[0]}, {coords[1]}, {coords[2]}, {coords[3]}]\n")

        print(f"\n[OK] Coordinates also saved to: {output_file}")
        print("\nPress any key in the plot window to close...")
        plt.show()

    def run(self):
        """Run the visual calibration."""
        print("\n" + "="*60)
        print("VISUAL CARD POSITION CALIBRATION")
        print("="*60)
        print("\nInstructions:")
        print("  1. For each card, click the TOP-LEFT corner")
        print("  2. Then click the BOTTOM-RIGHT corner")
        print("  3. A preview will be saved - check if it looks good")
        print("  4. Type 'y' if satisfied, 'n' to try again, 'q' to quit")
        print("="*60)

        input("\nPress Enter to start calibration...")

        # Set up the plot
        self.fig, self.ax = plt.subplots(figsize=(16, 10))
        self.ax.imshow(self.img)
        self.ax.axis('off')
        plt.title("Click to select card positions", fontsize=14, fontweight='bold')

        # Connect click event
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)

        # Start with first card
        self.start_next_card()

        plt.show()


def take_screenshot():
    """Take a screenshot and save it."""
    if not PYAUTOGUI_AVAILABLE:
        print("\nPyAutoGUI is not installed.")
        screenshot_path = input("Please enter the path to your poker table screenshot: ").strip()
        if not os.path.exists(screenshot_path):
            print(f"Error: File not found at {screenshot_path}")
            return None
        return screenshot_path

    print("\n=== Taking Screenshot ===")
    print("Make sure your poker table is visible on screen.")
    input("Press Enter when ready to capture screenshot...")

    screenshots_dir = "calibration_screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_path = os.path.join(screenshots_dir, f'calibration_{timestamp}.png')

    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    print(f"[OK] Screenshot saved to: {screenshot_path}")

    return screenshot_path


def main():
    print("="*60)
    print("VISUAL POKER OCR CALIBRATION TOOL")
    print("="*60)

    # Take screenshot
    screenshot_path = take_screenshot()
    if not screenshot_path:
        print("Error: Could not get screenshot. Exiting.")
        return

    # Run visual calibrator
    calibrator = VisualCalibrator(screenshot_path)
    calibrator.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCalibration cancelled by user.")
    except Exception as e:
        import traceback
        print(f"\n\nError during calibration: {e}")
        traceback.print_exc()
