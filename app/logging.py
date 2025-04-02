import configparser
import logging
import logging.config
import os
from logging.handlers import RotatingFileHandler

# Define the path to the logging configuration file
LOGGING_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "../logging.conf")
LOG_FOLDER = os.path.join(os.path.dirname(__file__), "../logs")


def setup_logging():
    """Sets up logging configuration from the logging.conf file."""
    # Ensure the logs folder exists
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)

    # Configure logging programmatically to ensure proper paths
    if os.path.exists(LOGGING_CONFIG_FILE):
        # Use ConfigParser to manipulate the config before loading
        config = configparser.ConfigParser()
        config.read(LOGGING_CONFIG_FILE)

        # Update file handler path to use logs directory
        log_file = os.path.join(LOG_FOLDER, "app.log")
        config.set("handler_fileHandler", "args", f"('{log_file}', 'a', 5242880, 5)")

        # Apply the updated config
        logging.config.fileConfig(config)
    else:
        # Fallback to programmatically setting up logging with rolling file handler
        logging.basicConfig(level=logging.DEBUG)
        log_file = os.path.join(LOG_FOLDER, "app.log")
        handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)


# Initialize logging when the module is imported
setup_logging()

# Example logger for this module
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.debug("Logging module initialized successfully.")
