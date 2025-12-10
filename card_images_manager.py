"""Downloads and manages playing card images from deckofcardsapi.com for GUI display."""
import os
import urllib.request
from pathlib import Path
from PIL import Image, ImageTk
from src.logging_config import get_logger

logger = get_logger('card_images')

class CardImageManager:
    def __init__(self, image_dir="card_images"):
        self.image_dir = Path(image_dir)
        self.image_dir.mkdir(exist_ok=True)
        self.card_cache = {}
        self.base_url = "https://deckofcardsapi.com/static/img"

    def _download_card_image(self, card_code):
        url = f"{self.base_url}/{card_code}.png"
        filepath = self.image_dir / f"{card_code}.png"
        if not filepath.exists():
            try:
                logger.info(f"Downloading card image: {card_code}")
                urllib.request.urlretrieve(url, filepath)
            except Exception as e:
                logger.error(f"Error downloading {card_code}: {e}")
                return None
        return str(filepath)

    def get_card_image(self, card_str, size=(80, 120)):
        if not card_str or card_str == "--":
            card_code = "back"
        else:
            card_code = self._convert_to_api_code(card_str)
        cache_key = f"{card_code}_{size}"
        if cache_key in self.card_cache:
            return self.card_cache[cache_key]
        filepath = self._download_card_image(card_code)
        if not filepath or not os.path.exists(filepath):
            return None
        img = Image.open(filepath)
        img = img.resize(size, Image.LANCZOS)
        self.card_cache[cache_key] = img
        return img

    def get_tk_image(self, card_str, size=(80, 120)):
        img = self.get_card_image(card_str, size)
        if img is None:
            return None
        return ImageTk.PhotoImage(img)

    def _convert_to_api_code(self, card_str):
        card_str = card_str.strip().upper()
        if not card_str:
            return "back"
        if card_str.startswith("10"):
            rank = "0"
            suit = card_str[2] if len(card_str) > 2 else ""
        else:
            rank = card_str[0]
            suit = card_str[1] if len(card_str) > 1 else ""
        return f"{rank}{suit}"

    def preload_common_cards(self):
        common_cards = [
            "AS", "KS", "QS", "JS", "10S",
            "AH", "KH", "QH", "JH", "10H",
            "AD", "KD", "QD", "JD", "10D",
            "AC", "KC", "QC", "JC", "10C",
            "back"
        ]
        for card in common_cards:
            try:
                self.get_card_image(card)
            except Exception as e:
                logger.error(f"Error preloading {card}: {e}")
