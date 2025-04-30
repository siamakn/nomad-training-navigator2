# utils/logger.py

import logging
from config.settings import settings
from pathlib import Path

log_dir = Path(settings.LOG_DIR)
log_dir.mkdir(parents=True, exist_ok=True)

log_file = log_dir / "app.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(settings.APP_NAME)
