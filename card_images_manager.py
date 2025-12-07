"""
Card image manager - downloads and provides access to playing card images.

Uses open-source card images for visual display.
"""

import os
import urllib.request
from pathlib import Path
from PIL import Image, ImageTk


class CardImageManager:
    """Manages card images for GUI display."""

    def __init__(self, image_dir="card_images"):
        self.image_dir = Path(image_dir)
        self.image_dir.mkdir(exist_ok=True)
        self.card_cache = {}

        # Base URL for card images (using deckofcardsapi.com free images)
        self.base_url = "https://deckofcardsapi.com/static/img"

    def _download_card_image(self, card_code):
        """Download a single card image."""
        url = f"{self.base_url}/{card_code}.png"
        filepath = self.image_dir / f"{card_code}.png"

        if not filepath.exists():
            try:
                print(f"Downloading card image: {card_code}")
                urllib.request.urlretrieve(url, filepath)
            except Exception as e:
                print(f"Error downloading {card_code}: {e}")
                return None

        return str(filepath)

    def get_card_image(self, card_str, size=(80, 120)):
        """
        Get PIL Image for a card.

        Args:
            card_str: Card string like "AS", "10H", "KD"
            size: Tuple of (width, height) for resizing

        Returns:
            PIL Image object
        """
        if not card_str or card_str == "--":
            # Return card back image
            card_code = "back"
        else:
            # Convert card string to deck of cards API format
            # e.g., "AS" -> "AS", "10H" -> "0H", etc.
            card_code = self._convert_to_api_code(card_str)

        # Check cache
        cache_key = f"{card_code}_{size}"
        if cache_key in self.card_cache:
            return self.card_cache[cache_key]

        # Download if needed
        filepath = self._download_card_image(card_code)
        if not filepath or not os.path.exists(filepath):
            # Return a blank/error image
            return None

        # Load and resize image
        img = Image.open(filepath)
        img = img.resize(size, Image.LANCZOS)

        # Cache it
        self.card_cache[cache_key] = img

        return img

    def get_tk_image(self, card_str, size=(80, 120)):
        """
        Get tkinter PhotoImage for a card.

        Args:
            card_str: Card string like "AS", "10H", "KD"
            size: Tuple of (width, height) for resizing

        Returns:
            tkinter PhotoImage object
        """
        img = self.get_card_image(card_str, size)
        if img is None:
            return None

        return ImageTk.PhotoImage(img)

    def _convert_to_api_code(self, card_str):
        """
        Convert our card format to deckofcardsapi.com format.

        Args:
            card_str: "AS", "10H", "KD", "2C", etc.

        Returns:
            API code like "AS", "0H", "KD", "2C"
        """
        card_str = card_str.strip().upper()

        if not card_str:
            return "back"

        # Extract rank and suit
        if card_str.startswith("10"):
            rank = "0"  # API uses 0 for 10
            suit = card_str[2] if len(card_str) > 2 else ""
        else:
            rank = card_str[0]
            suit = card_str[1] if len(card_str) > 1 else ""

        # API uses lowercase suit except for special cards
        return f"{rank}{suit}"

    def preload_common_cards(self):
        """Preload common card images for faster display."""
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
                print(f"Error preloading {card}: {e}")
