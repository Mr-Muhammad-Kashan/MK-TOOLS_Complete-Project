import logging
import os
from datetime import datetime
from .paths import resource_path

def setup_logger():
    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'logs'))
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except Exception:
            log_dir = "."
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_dir, f"mk-tools_{timestamp}.log")
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler(log_file), logging.StreamHandler()])
    return logging.getLogger(__name__)

logger = setup_logger()
