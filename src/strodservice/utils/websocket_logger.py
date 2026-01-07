from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
import logging
from datetime import datetime

logger = logging.getLogger('websocket_logger')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('websocket.log')
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_websocket_event(username, event_type, data):
    logger.info(f"User: {username}, Event: {event_type}, Data: {data}")