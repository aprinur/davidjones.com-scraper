import logging
from logging import Logger

LOG_FILE = 'app.log'

logging.basicConfig(
    level=logging.INFO,
    format='\n%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(LOG_FILE),
              logging.StreamHandler()
              ]
)


def log() -> Logger:
    return logging.getLogger(__name__)


logger = log()
