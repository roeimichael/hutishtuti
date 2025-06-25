import os
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\roeym\Desktop\tesseract\tesseract.exe"
from PIL import Image, ImageOps
import numpy as np

IMAGES_DIR = 'images'

CARD_COORDS = [
    (370, 470, 390, 495),
    (415, 470, 430, 495),
]

SHAPE_COLORS = {
    "hearts": (150, 33, 24),
    "diamonds": (29, 70, 149),
    "spades": (19, 19, 19),
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
    w, h = card_img.size
    box = (w-10, 0, w, 10)
    region = card_img.crop(box)
    region = region.convert("RGB")
    np_region = np.array(region)
    diffs = np.abs(np_region - 255)
    contrast = diffs.sum(axis=2)
    idx = np.unravel_index(np.argmin(contrast, axis=None), contrast.shape)
    color = tuple(int(x) for x in np_region[idx[0], idx[1]])
    return color

def preprocess_card(card_img, out_size=(100, 100)):
    card_img = card_img.convert("RGBA")
    card_img = ImageOps.contain(card_img, (out_size[0] - 10, out_size[1] - 10))
    background = Image.new("RGBA", out_size, (255, 255, 255, 255))
    offset = ((out_size[0] - card_img.width) // 2, (out_size[1] - card_img.height) // 2)
    background.paste(card_img, offset, card_img)
    return background.convert("L")

for image_file in os.listdir(IMAGES_DIR):
    if not image_file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
        continue
    image_path = os.path.join(IMAGES_DIR, image_file)
    try:
        img = Image.open(image_path)
        card_strs = []
        for idx, coords in enumerate(CARD_COORDS):
            card_crop = img.crop(coords)
            shape_color = sample_shape_color(card_crop)
            shape = closest_shape(shape_color)
            processed_img = preprocess_card(card_crop)
            text = pytesseract.image_to_string(processed_img, config='--psm 10').strip().upper()
            text = CARD_REPLACEMENTS.get(text, text)
            suit_initial = SUIT_INITIALS.get(shape, '?')
            card_strs.append(f"{text}-{suit_initial}")
        print(f"({','.join(card_strs)})")
    except Exception:
        pass