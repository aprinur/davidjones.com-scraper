import os
import shutil
import sys
from dotenv import load_dotenv
from pathlib import Path

from src.logger import logger

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
credentials_dir = Path(project_dir) / 'credentials'


def check_cred_dir() -> None:
    """
    Check if the credentials directory exists. If not, create it and log the action.

    Returns:
        None
    """
    if not os.path.exists(credentials_dir):
        os.makedirs(credentials_dir)
        print(f'Credentials directoy has created in {project_dir}')


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
        api_dir = Path(project_dir) / api_key_filename

        shutil.move(api_dir, credentials_dir)
        logger.info(f'{api_key_filename} moved to {credentials_dir}')

        relative_cred_path = os.path.join('credentials', os.path.basename(api_key_filename))

        env_content = rf"""
G_SPREADSHEET_NAME='{g_sheetname}'
GOOGLE_SHEET_CREDENTIALS_FILE='{relative_cred_path}'
DEBUG=False
""".strip()

        with open(env_path, 'w') as env:
            env.write(env_content)
        load_dotenv(env_path)


def user_input_for_gsheet():
    """
    Function to get user input for Google Sheets credentials.

    Returns:
        tuple: A tuple containing the Google Sheets name and the API key filename.
    """
    while True:
        g_sheetname = input("Enter your google spreadsheet name or type 'quit' and press enter to exit: ").strip()
        if g_sheetname.lower() == 'quit':
            print('Closing program')
            sys.exit(0)
        if g_sheetname:
            break
        logger.warning('Sheet name cannot be empty')
    while True:
        api_key = input("Enter json API key name or type 'quit' and press enter to exit: ").strip()
        file_path = os.path.join(project_dir, api_key)
        if api_key.lower() == 'quit':
            print('Closing program')
            sys.exit(0)
        if os.path.exists(file_path):
            return g_sheetname, api_key
        logger.error(
            f'Error: "{api_key}" not found in working directory. Please move the file to the working directory and try again')


def creds() -> None:
    """
    Function to call check_cred_dir() and check_dotenv()

     Returns:
         None
        """
    check_cred_dir()
    check_dotenv()


creds()
