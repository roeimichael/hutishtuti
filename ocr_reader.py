import os
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\roeym\Desktop\tesseract\tesseract.exe"
from PIL import Image, ImageOps
import numpy as np

CARD_LOCATIONS = {
    'card1': (880, 770, 915, 810),  # Left hand card
    'card2': (945, 770, 985, 810),   #  right hand card 2
    'flop1': (592, 320, 652, 400),   # Flop 1
    'flop2': (662, 320, 722, 400),   # Flop 2
    'flop3': (732, 320, 792, 400),   # Flop 3
    'turn':  (802, 320, 862, 400),   # Turn
    'river': (872, 320, 932, 400),   # River
}

SHAPE_COLORS = {
    "hearts": (150, 33, 24),
    "diamonds": (29, 70, 149),
    "spades": (0, 0, 0),
    "clubs": (59, 103, 24),
}

SUIT_INITIALS = {
    "hearts": "H",
    "diamonds": "D",
    "spades": "S",
    "clubs": "C",
}

CARD_REPLACEMENTS = {
    'J': 'J', 'Q': 'Q', 'K': 'K', 'A': 'A',
    '0': '10', 'O': '10', 'o': '10',
    '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9'
}

def closest_shape(color):
    min_dist = float('inf')
    shape_name = None
    for shape, ref_color in SHAPE_COLORS.items():
        dist = np.linalg.norm(np.array(color) - np.array(ref_color))
        if dist < min_dist:
            min_dist = dist
            shape_name = shape
    return shape_name

def sample_shape_color(card_img):
    region = card_img.convert("RGB")
    np_region = np.array(region)
    # Calculate Euclidean distance from white for each pixel
    diffs = np_region.astype(int) - 255
    dists = np.sqrt((diffs ** 2).sum(axis=2))
    idx = np.unravel_index(np.argmax(dists, axis=None), dists.shape)
    color = tuple(int(x) for x in np_region[idx[0], idx[1]])
    print(f"Sampled color for card: {color}")
    return color

def preprocess_card(card_img, out_size=(100, 100), pad=30):
    # Convert to grayscale
    card_img = card_img.convert("L")
    # Binarize (black and white)
    threshold = 180
    card_img = card_img.point(lambda x: 0 if x < threshold else 255, '1')
    # Pad with white background
    w, h = card_img.size
    new_w, new_h = w + 2 * pad, h + 2 * pad
    background = Image.new('1', (new_w, new_h), 1)  # 1 = white in mode '1'
    background.paste(card_img, (pad, pad))
    return background

def process_card_from_image(img, card_name, coords, crop_dir="card_crops"):
    os.makedirs(crop_dir, exist_ok=True)
    card_crop = img.crop(coords)
    capture_path = os.path.join(crop_dir, f"{card_name}_capture.png")
    card_crop.save(capture_path)
    shape_color = sample_shape_color(card_crop)
    print(f"[{card_name.upper()}] sampled color: {shape_color}")
    shape = closest_shape(shape_color)
    processed_img = preprocess_card(card_crop)
    processed_path = os.path.join(crop_dir, f"{card_name}_processed.png")
    processed_img.save(processed_path)
    print(f"[{card_name.upper()}] Saved crop: {capture_path}, processed: {processed_path}")
    text = pytesseract.image_to_string(processed_img, config='--psm 10').strip().upper()
    text = CARD_REPLACEMENTS.get(text, text)
    return {'number': text, 'shape': shape, 'capture': capture_path, 'processed': processed_path}

def detect_hand_from_image(image_path):
    img = Image.open(image_path)
    hand_cards = []
    for card_name in ['card1', 'card2']:
        card_info = process_card_from_image(img, card_name, CARD_LOCATIONS[card_name])
        hand_cards.append(card_info)
    card_strs = [f"{c['number']}-{SUIT_INITIALS.get(c['shape'], '?')}" for c in hand_cards]
    hand_str = f"({','.join(card_strs)})"
    print(f"Hand: {hand_str}")
    return hand_cards

def read_flop_from_image(image_path):
    img = Image.open(image_path)
    flop_cards = []
    for card_name in ['flop1', 'flop2', 'flop3']:
        card_info = process_card_from_image(img, card_name, CARD_LOCATIONS[card_name])
        flop_cards.append(card_info)
    card_strs = [f"{c['number']}-{SUIT_INITIALS.get(c['shape'], '?')}" for c in flop_cards]
    flop_str = f"Flop: {','.join(card_strs)}"
    print(flop_str)
    return flop_cards

def read_turn_from_image(image_path):
    img = Image.open(image_path)
    card_info = process_card_from_image(img, 'turn', CARD_LOCATIONS['turn'])
    turn_str = f"Turn: {card_info['number']}-{SUIT_INITIALS.get(card_info['shape'], '?')}"
    print(turn_str)
    return card_info

def read_river_from_image(image_path):
    img = Image.open(image_path)
    card_info = process_card_from_image(img, 'river', CARD_LOCATIONS['river'])
    river_str = f"River: {card_info['number']}-{SUIT_INITIALS.get(card_info['shape'], '?')}"
    print(river_str)
    return card_info

if __name__ == "__main__":
    try:
        print("[INFO] OCR Reader started.")
        images_dir = "images"
        for image_file in os.listdir(images_dir):
            if not image_file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
                continue
            image_path = os.path.join(images_dir, image_file)
            print(detect_hand_from_image(image_path))
            print(read_flop_from_image(image_path))
            print(read_turn_from_image(image_path))
            print(read_river_from_image(image_path))
        print("[INFO] OCR Reader finished. Press Enter to exit.")
        input()
    except Exception as e:
        import traceback
        print("[OCR ERROR]", e)
        traceback.print_exc()
        input("[ERROR] Press Enter to exit...")