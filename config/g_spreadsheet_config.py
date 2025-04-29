import os

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from gspread.exceptions import SpreadsheetNotFound

def connect_to_spreadsheet():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

    load_dotenv()
    spreadsheet_name = os.getenv('G_SPREADSHEET_NAME')
    current_spreadsheet_name = spreadsheet_name
    creds_file = os.getenv('GOOGLE_SHEET_CREDENTIALS_FILE')

    if not creds_file or not os.path.exists(os.path.abspath(creds_file)):
        raise FileNotFoundError('Google Sheets API credentials file not found')

    creds = Credentials.from_service_account_file(creds_file, scopes=scope)
    client = gspread.authorize(creds)

    while True:
        try:
            spreadsheets = client.open(current_spreadsheet_name)
            print(f'Successfully connected to spreadsheet {current_spreadsheet_name}')
            return spreadsheets

        except SpreadsheetNotFound:
            print(f'Spreadsheet with name {current_spreadsheet_name} not found.')
            new_spreadsheet_name = input('Enter spreadsheet name: ').strip()
            if new_spreadsheet_name:

                if new_spreadsheet_name != current_spreadsheet_name:
                    with open('.env', 'r+') as file:
                        lines = file.readlines()
                        file.seek(0)
                        for line in lines:
                            if line.startswith('G_SPREADSHEET_NAME='):
                                file.write(f'G_SPREADSHEET_NAME={new_spreadsheet_name}\n')
                            else:
                                file.write(line)
                        file.truncate()
                        load_dotenv(override=True)
                    print(f'.env updated with new spreadsheet name: {new_spreadsheet_name}')
                current_spreadsheet_name = new_spreadsheet_name






"""
problem when rewriting G_SPREADSHEET_NAME
"""

