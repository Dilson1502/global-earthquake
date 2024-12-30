import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def check_dotenv():
    # Define the name of the .env file
    dotenv_file = '.env'

    # Check if the .env file exists in the current directory
    return os.path.isfile(dotenv_file)


if __name__ == "__main__":
    if check_dotenv():
        logging.info(".env is present, running program with variables present in .env file...")
    else:
        logging.info("Looking for GitHub environment presence...")
