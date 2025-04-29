# utils/logger.py

import logging
from pathlib import Path
from config.settings import settings

# Make sure log directory exists
Path(settings.LOG_DIR).mkdir(parents=True, exist_ok=True)

# Configure logger
logger = logging.getLogger("nomad_training_navigator")
logger.setLevel(logging.DEBUG)

# File handler
file_handler = logging.FileHandler(settings.LOG_DIR / "app.log")
file_handler.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)
