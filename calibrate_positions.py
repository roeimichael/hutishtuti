import os
from PIL import Image, ImageDraw
from datetime import datetime

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("WARNING: pyautogui not installed. You'll need to provide a screenshot manually.")

def take_screenshot():
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
    print(f"Screenshot saved to: {screenshot_path}")
    return screenshot_path

def get_coordinates(card_name, default_coords=None):
    print(f"\n--- {card_name.upper()} ---")
    if default_coords:
        print(f"Default coordinates: {default_coords}")
        use_default = input("Use default? (y/n): ").strip().lower()
        if use_default == 'y':
            return default_coords
    print("Enter coordinates for the card region (left, top, right, bottom)")
    print("Example: 880, 770, 915, 810")
    while True:
        try:
            coords_input = input(f"{card_name} coordinates: ").strip()
            coords = [int(x.strip()) for x in coords_input.split(',')]
            if len(coords) != 4:
                print("Error: Please enter exactly 4 values (left, top, right, bottom)")
                continue
            left, top, right, bottom = coords
            if left >= right or top >= bottom:
                print("Error: Invalid coordinates. Ensure left < right and top < bottom")
                continue
            return tuple(coords)
        except ValueError:
            print("Error: Please enter valid numbers separated by commas")

def preview_crop(image_path, card_name, coords, crop_dir="calibration_crops"):
    os.makedirs(crop_dir, exist_ok=True)
    img = Image.open(image_path)
    crop = img.crop(coords)
    crop_path = os.path.join(crop_dir, f"{card_name}_preview.png")
    crop.save(crop_path)
    preview_size = (crop.width * 4, crop.height * 4)
    preview = crop.resize(preview_size, Image.NEAREST)
    preview_path = os.path.join(crop_dir, f"{card_name}_preview_large.png")
    preview.save(preview_path)
    print(f"\n[OK] Preview saved to: {crop_path}")
    print(f"[OK] Large preview saved to: {preview_path}")
    print(f"  Crop size: {crop.width}x{crop.height} pixels")
    print(f"  Coordinates: {coords}")
    return crop_path

def create_annotated_screenshot(image_path, all_coords, output_path="calibration_crops/annotated_screenshot.png"):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    colors = {
        'card1': 'green', 'card2': 'green',
        'flop1': 'blue', 'flop2': 'blue', 'flop3': 'blue',
        'turn': 'yellow', 'river': 'red'
    }
    for card_name, coords in all_coords.items():
        color = colors.get(card_name, 'white')
        draw.rectangle(coords, outline=color, width=3)
        draw.text((coords[0], coords[1] - 20), card_name.upper(), fill=color)
    img.save(output_path)
    print(f"\n[OK] Annotated screenshot saved to: {output_path}")
    print("  This shows all card positions marked on the original screenshot.")

def calibrate_card_position(image_path, card_name, default_coords=None):
    coords = get_coordinates(card_name, default_coords)
    while True:
        preview_crop(image_path, card_name, coords)
        print(f"\nOpen the preview images to check if the crop looks correct.")
        satisfied = input("Are you satisfied with this position? (y/n): ").strip().lower()
        if satisfied == 'y':
            return coords
        print("Let's adjust the coordinates...")
        coords = get_coordinates(card_name, coords)

def format_yaml_output(all_coords):
    print("\n" + "="*60)
    print("CALIBRATION COMPLETE!")
    print("="*60)
    print("\nAdd these coordinates to your config.yaml file:\n")
    print("card_locations:")
    for card_name, coords in all_coords.items():
        print(f"  {card_name}: [{coords[0]}, {coords[1]}, {coords[2]}, {coords[3]}]")
    print("\n" + "="*60)

def main():
    print("="*60)
    print("POKER OCR CARD POSITION CALIBRATION TOOL")
    print("="*60)
    screenshot_path = take_screenshot()
    if not screenshot_path:
        print("Error: Could not get screenshot. Exiting.")
        return
    default_coords = {
        'card1': (880, 770, 915, 810),
        'card2': (945, 770, 985, 810),
        'flop1': (592, 320, 652, 400),
        'flop2': (662, 320, 722, 400),
        'flop3': (732, 320, 792, 400),
        'turn':  (802, 320, 862, 400),
        'river': (872, 320, 932, 400),
    }
    print("\n" + "="*60)
    print("CALIBRATION INSTRUCTIONS")
    print("="*60)
    print("For each card position, you'll need to enter 4 coordinates:")
    print("  left, top, right, bottom")
    print("\nHow to find coordinates:")
    print("  1. Open the screenshot in an image editor (Paint, Preview, etc.)")
    print("  2. Hover over the card to see pixel coordinates")
    print("  3. Note the top-left corner (left, top)")
    print("  4. Note the bottom-right corner (right, bottom)")
    print("\nTip: The crop should include just the card rank (number/face)")
    print("     and enough of the suit color to detect it.")
    print("="*60)
    card_order = ['card1', 'card2', 'flop1', 'flop2', 'flop3', 'turn', 'river']
    all_coords = {}
    for card_name in card_order:
        default = default_coords.get(card_name)
        all_coords[card_name] = calibrate_card_position(screenshot_path, card_name, default)
    create_annotated_screenshot(screenshot_path, all_coords)
    format_yaml_output(all_coords)
    output_file = "calibration_coords.txt"
    with open(output_file, 'w') as f:
        f.write("card_locations:\n")
        for card_name, coords in all_coords.items():
            f.write(f"  {card_name}: [{coords[0]}, {coords[1]}, {coords[2]}, {coords[3]}]\n")
    print(f"\nCoordinates also saved to: {output_file}")
    print("\nNext steps:")
    print("  1. Review the annotated screenshot and preview crops")
    print("  2. Copy the coordinates above to your config.yaml")
    print("  3. Run your poker OCR analyzer to test!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCalibration cancelled by user.")
    except Exception as e:
        import traceback
        print(f"\n\nError during calibration: {e}")
        traceback.print_exc()
        input("\nPress Enter to exit...")
