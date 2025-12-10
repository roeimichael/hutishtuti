"""Configuration loader from config.yaml or config.local.yaml."""
import yaml
from pathlib import Path
from typing import Dict, Tuple, Any

class Config:
    def __init__(self, config_path: str = None):
        self._config = self._load_config(config_path)

    def _load_config(self, config_path: str = None) -> Dict[str, Any]:
        if config_path is None:
            project_root = Path(__file__).parent.parent
            config_files = [
                project_root / "config.local.yaml",
                project_root / "config.yaml",
            ]
            for config_file in config_files:
                if config_file.exists():
                    config_path = str(config_file)
                    break
            else:
                raise FileNotFoundError("No configuration file found")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config

    @property
    def tesseract_path(self) -> str:
        return self._config.get('tesseract', {}).get('path', 'tesseract')

    @property
    def card_locations(self) -> Dict[str, Tuple[int, int, int, int]]:
        locations = self._config.get('card_locations', {})
        return {k: tuple(v) for k, v in locations.items()}

    @property
    def suit_colors(self) -> Dict[str, Tuple[int, int, int]]:
        colors = self._config.get('suit_colors', {})
        return {k: tuple(v) for k, v in colors.items()}

    @property
    def suit_initials(self) -> Dict[str, str]:
        return self._config.get('suit_initials', {})

    @property
    def ocr_threshold(self) -> int:
        return self._config.get('ocr', {}).get('threshold', 180)

    @property
    def ocr_padding(self) -> int:
        return self._config.get('ocr', {}).get('padding', 30)

    @property
    def ocr_output_size(self) -> Tuple[int, int]:
        size = self._config.get('ocr', {}).get('output_size', [100, 100])
        return tuple(size)

    @property
    def ocr_psm_mode(self) -> int:
        return self._config.get('ocr', {}).get('psm_mode', 10)

    @property
    def crop_directory(self) -> str:
        return self._config.get('ocr', {}).get('crop_directory', 'card_crops')

    @property
    def card_replacements(self) -> Dict[str, str]:
        return self._config.get('card_replacements', {})

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

_config_instance = None

def get_config(config_path: str = None) -> Config:
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_path)
    return _config_instance

def reload_config(config_path: str = None):
    global _config_instance
    _config_instance = Config(config_path)
