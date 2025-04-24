import yaml
import threading
from pathlib import Path

def get_project_root() -> Path:
    """Get the project root directory"""
    return Path(__file__).resolve().parent.parent.parent

PROJECT_ROOT = get_project_root()

class Config:
    _lock = threading.Lock()
    _initialized = False

    def __init__(self):
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self._config = None
                    self._load_initial_config()
                    self._initialized = True

    def _load_initial_config(self):
        config_path =  self._get_config_path()

        with config_path.open("rb") as f:
            self._config = yaml.safe_load(f)

    def _get_config_path(self) -> Path:
        root = PROJECT_ROOT
        config_path = root / "config" / "config.yml"

        if config_path.exists():
            return config_path
        
        raise FileNotFoundError("No configuration file found in config directory.")
    
    def get(self, key, default = None):
        return self._config.get(key, default)
