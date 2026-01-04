import yaml
import os
from dataclasses import dataclass, asdict
from typing import Dict, Any

CONFIG_FILE = "config.yaml"

@dataclass
class Settings:
    model_name: str = "orca-mini-3b-gguf2-q4_0.gguf"
    model_path: str = "models/"
    max_tokens: int = 200
    temperature: float = 0.7
    top_k: int = 40
    persona: str = "default"

class ConfigManager:
    def __init__(self, config_path: str = CONFIG_FILE):
        self.config_path = config_path
        self.settings = Settings()
        self.load()

    def load(self):
        """Load settings from the config file."""
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                data = yaml.safe_load(f) or {}
                # Update settings with loaded data
                for key, value in data.items():
                    if hasattr(self.settings, key):
                        setattr(self.settings, key, value)
    
    def save(self):
        """Save current settings to the config file."""
        with open(self.config_path, "w") as f:
            yaml.dump(asdict(self.settings), f)

    def update(self, **kwargs):
        """Update specific settings and save."""
        for key, value in kwargs.items():
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)
            else:
                raise KeyError(f"Invalid setting: {key}")
        self.save()

    def get(self, key: str) -> Any:
        return getattr(self.settings, key, None)
