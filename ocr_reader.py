import os
import pytesseract
from PIL import Image, ImageOps
import numpy as np
from src.config import get_config

# Load configuration
config = get_config()

# Set Tesseract path from config
pytesseract.pytesseract.tesseract_cmd = config.tesseract_path

# Load all configuration values
CARD_LOCATIONS = config.card_locations
SHAPE_COLORS = config.suit_colors
SUIT_INITIALS = config.suit_initials
CARD_REPLACEMENTS = config.card_replacements

def closest_shape(color):
    min_dist = float('inf')
    shape_name = None
    for shape, ref_color in SHAPE_COLORS.items():
        dist = np.linalg.norm(np.array(color) - np.array(ref_color))
        if dist < min_dist:
            min_dist = dist
            shape_name = shape
    return shape_name

def sample_shape_color(card_img, verbose=False):
    region = card_img.convert("RGB")
    np_region = np.array(region)
    # Calculate Euclidean distance from white for each pixel
    diffs = np_region.astype(int) - 255
    dists = np.sqrt((diffs ** 2).sum(axis=2))
    idx = np.unravel_index(np.argmax(dists, axis=None), dists.shape)
    color = tuple(int(x) for x in np_region[idx[0], idx[1]])
    if verbose:
        print(f"Sampled color for card: {color}")
    return color

def preprocess_card(card_img, out_size=None, pad=None):
    # Use config defaults if not provided
    if out_size is None:
        out_size = config.ocr_output_size
    if pad is None:
        pad = config.ocr_padding

    # Convert to grayscale
    card_img = card_img.convert("L")
    # Binarize (black and white)
    threshold = config.ocr_threshold
    card_img = card_img.point(lambda x: 0 if x < threshold else 255, '1')
    # Pad with white background
    w, h = card_img.size
    new_w, new_h = w + 2 * pad, h + 2 * pad
    background = Image.new('1', (new_w, new_h), 1)  # 1 = white in mode '1'
    background.paste(card_img, (pad, pad))
    return background

def process_card_from_image(img, card_name, coords, crop_dir=None, verbose=False):
    # Use config default if not provided
    if crop_dir is None:
        crop_dir = config.crop_directory

    os.makedirs(crop_dir, exist_ok=True)
    card_crop = img.crop(coords)
    capture_path = os.path.join(crop_dir, f"{card_name}_capture.png")
    card_crop.save(capture_path)
    shape_color = sample_shape_color(card_crop, verbose=verbose)

    if verbose:
        print(f"[{card_name.upper()}] sampled color: {shape_color}")

    shape = closest_shape(shape_color)
    processed_img = preprocess_card(card_crop)
    processed_path = os.path.join(crop_dir, f"{card_name}_processed.png")
    processed_img.save(processed_path)

    if verbose:
        print(f"[{card_name.upper()}] Saved crop: {capture_path}, processed: {processed_path}")

    # Use PSM mode from config
    psm_config = f'--psm {config.ocr_psm_mode}'
    text = pytesseract.image_to_string(processed_img, config=psm_config).strip().upper()
    text = CARD_REPLACEMENTS.get(text, text)
    return {'number': text, 'shape': shape, 'capture': capture_path, 'processed': processed_path}

def detect_hand_from_image(image_path, verbose=False):
    img = Image.open(image_path)
    hand_cards = []
    for card_name in ['card1', 'card2']:
        card_info = process_card_from_image(img, card_name, CARD_LOCATIONS[card_name], verbose=verbose)
        hand_cards.append(card_info)
    card_strs = [f"{c['number']}{SUIT_INITIALS.get(c['shape'], '?')}" for c in hand_cards]
    hand_str = f"{card_strs[0]} {card_strs[1]}"
    return hand_cards, hand_str

def read_flop_from_image(image_path, verbose=False):
    img = Image.open(image_path)
    flop_cards = []
    for card_name in ['flop1', 'flop2', 'flop3']:
        card_info = process_card_from_image(img, card_name, CARD_LOCATIONS[card_name], verbose=verbose)
        flop_cards.append(card_info)
    card_strs = [f"{c['number']}{SUIT_INITIALS.get(c['shape'], '?')}" for c in flop_cards]
    flop_str = f"{card_strs[0]} {card_strs[1]} {card_strs[2]}"
    return flop_cards, flop_str

def read_turn_from_image(image_path, verbose=False):
    img = Image.open(image_path)
    card_info = process_card_from_image(img, 'turn', CARD_LOCATIONS['turn'], verbose=verbose)
    turn_str = f"{card_info['number']}{SUIT_INITIALS.get(card_info['shape'], '?')}"
    return card_info, turn_str

def read_river_from_image(image_path, verbose=False):
    img = Image.open(image_path)
    card_info = process_card_from_image(img, 'river', CARD_LOCATIONS['river'], verbose=verbose)
    river_str = f"{card_info['number']}{SUIT_INITIALS.get(card_info['shape'], '?')}"
    return card_info, river_str

if __name__ == "__main__":
    try:
        print("[INFO] OCR Reader started.")
        images_dir = "images"
        for image_file in os.listdir(images_dir):
            if not image_file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
                continue
            image_path = os.path.join(images_dir, image_file)
            print(f"\nProcessing: {image_file}")

            hand, hand_str = detect_hand_from_image(image_path, verbose=True)
            print(f"Hand: {hand_str}")

            flop, flop_str = read_flop_from_image(image_path, verbose=True)
            print(f"Flop: {flop_str}")

            turn, turn_str = read_turn_from_image(image_path, verbose=True)
            print(f"Turn: {turn_str}")

            river, river_str = read_river_from_image(image_path, verbose=True)
            print(f"River: {river_str}")

        print("\n[INFO] OCR Reader finished. Press Enter to exit.")
        input()
    except Exception as e:
        import traceback
        print("[OCR ERROR]", e)
        traceback.print_exc()
        input("[ERROR] Press Enter to exit...")