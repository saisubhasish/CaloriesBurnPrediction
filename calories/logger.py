import os
import logging
from datetime import datetime


def create_logs():
    """
    Create logs for the application.

    This function sets up the logging configuration for the application. It creates a logger object and configures it to write logs to both a local log file and AWS CloudWatch. The logs are stored in a directory named after the current date, and the log file is named after the current time. The log file path is returned.
    """
    logger = logging.getLogger(__name__)
    now = datetime.now()

    LOG_FILE_FOLDER = now.strftime('%m_%d_%Y')
    LOG_FILE = now.strftime('%H-%M-%S') + ".log"

    logs_path = os.path.join(os.getcwd(), 'logs', LOG_FILE_FOLDER)
    os.makedirs(logs_path, exist_ok=True)

    LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

    logging.basicConfig(filename=LOG_FILE_PATH,
                        format="[%(asctime)s] %(lineno)d - %(filename)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s", level=logging.INFO)

    # Set the log level
    logger.setLevel(logging.INFO)

    return logger

logger = create_logs()
