import os
import shutil
from src.logger import logger
from dotenv import load_dotenv
from src.user_input import user_input_for_gsheet

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
credentials_dir = os.path.join(project_dir, 'credentials')


def check_cred_dir() -> None:
    """
    Check if the credentials directory exists. If not, create it and log the action.

    Returns:
        None
    """
    if not os.path.exists(credentials_dir):
        os.makedirs(credentials_dir)
        logger.info('Credentials directory has created')


def check_dotenv() -> None:
    """
    Check if the .env file exists in the project directory. If not, create one and ask for Google Sheets credentials.
    Move the provided API key file to the credentials directory and write the necessary environment variables to the .env file.

    Returns:
        None
    """
    env_path = os.path.join(project_dir, '.env')

    if not os.path.exists(env_path):
        g_sheetname, api_key_filename = user_input_for_gsheet()

        destination_path = os.path.join(credentials_dir, os.path.basename(api_key_filename))
        shutil.move(api_key_filename, destination_path)
        logger.info(f'{api_key_filename} moved to {destination_path}')

        relative_cred_path = os.path.join('credentials', os.path.basename(api_key_filename))

        env_content = f"""
        G_SPREADSHEET_NAME="{g_sheetname}"
        GOOGLE_SHEET_CREDENTIALS_FILE="{relative_cred_path}"
        DEBUG=True
        """.strip()

        with open(env_path, 'w') as env:
            env.write(env_content)
        load_dotenv(env_path)


check_cred_dir()
check_dotenv()