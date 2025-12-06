"""
Configuration loader for Hutishtuti OCR.

This module loads configuration from config.yaml or config.local.yaml
and provides easy access to configuration values.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Any


class Config:
    """Configuration manager for OCR settings."""

    def __init__(self, config_path: str = None):
        """
        Initialize configuration.

        Args:
            config_path: Optional path to config file. If not provided,
                        searches for config.local.yaml, then config.yaml
        """
        self._config = self._load_config(config_path)

    def _load_config(self, config_path: str = None) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if config_path is None:
            # Search for config files in order of preference
            project_root = Path(__file__).parent.parent
            config_files = [
                project_root / "config.local.yaml",  # User's local config (gitignored)
                project_root / "config.yaml",         # Default config
            ]

            for config_file in config_files:
                if config_file.exists():
                    config_path = str(config_file)
                    break
            else:
                raise FileNotFoundError(
                    "No configuration file found. Please create config.yaml or config.local.yaml"
                )

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        return config

    @property
    def tesseract_path(self) -> str:
        """Get Tesseract executable path."""
        return self._config.get('tesseract', {}).get('path', 'tesseract')

    @property
    def card_locations(self) -> Dict[str, Tuple[int, int, int, int]]:
        """Get card location coordinates."""
        locations = self._config.get('card_locations', {})
        # Convert lists to tuples
        return {k: tuple(v) for k, v in locations.items()}

    @property
    def suit_colors(self) -> Dict[str, Tuple[int, int, int]]:
        """Get RGB color values for suits."""
        colors = self._config.get('suit_colors', {})
        return {k: tuple(v) for k, v in colors.items()}

    @property
    def suit_initials(self) -> Dict[str, str]:
        """Get suit abbreviations."""
        return self._config.get('suit_initials', {})

    @property
    def ocr_threshold(self) -> int:
        """Get OCR binarization threshold."""
        return self._config.get('ocr', {}).get('threshold', 180)

    @property
    def ocr_padding(self) -> int:
        """Get OCR image padding."""
        return self._config.get('ocr', {}).get('padding', 30)

    @property
    def ocr_output_size(self) -> Tuple[int, int]:
        """Get OCR output image size."""
        size = self._config.get('ocr', {}).get('output_size', [100, 100])
        return tuple(size)

    @property
    def ocr_psm_mode(self) -> int:
        """Get Tesseract PSM mode."""
        return self._config.get('ocr', {}).get('psm_mode', 10)

    @property
    def crop_directory(self) -> str:
        """Get directory for card crops."""
        return self._config.get('ocr', {}).get('crop_directory', 'card_crops')

    @property
    def card_replacements(self) -> Dict[str, str]:
        """Get card text replacements for OCR corrections."""
        return self._config.get('card_replacements', {})

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key."""
        return self._config.get(key, default)


# Global config instance
_config_instance = None


def get_config(config_path: str = None) -> Config:
    """
    Get the global configuration instance.

    Args:
        config_path: Optional path to config file

    Returns:
        Config instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_path)
    return _config_instance


def reload_config(config_path: str = None):
    """
    Reload configuration from file.

    Args:
        config_path: Optional path to config file
    """
    global _config_instance
    _config_instance = Config(config_path)
