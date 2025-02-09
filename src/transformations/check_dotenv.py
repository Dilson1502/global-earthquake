import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def check_dotenv():
    """Validate if any .env file is present."""

    dotenv_file = '.env'
    return os.path.isfile(dotenv_file)


def check_dotenv_presence():
    if check_dotenv():
        logging.info(".env is present, running program with variables present in .env file...")
    else:
        logging.info("Looking for GitHub environment presence...")
