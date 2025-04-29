import os

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials


scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

load_dotenv()
G_SPREADSHEET_NAME = os.getenv('G_SPREADSHEET_NAME')
GOOGLE_SHEET_CREDENTIALS_FILE = os.getenv('GOOGLE_SHEET_CREDENTIALS_FILE')

if not GOOGLE_SHEET_CREDENTIALS_FILE or not os.path.exists(os.path.abspath(GOOGLE_SHEET_CREDENTIALS_FILE)):
    raise FileNotFoundError('Google Sheets API credentials file not found')

creds = Credentials.from_service_account_file(GOOGLE_SHEET_CREDENTIALS_FILE, scopes=scope)
client = gspread.authorize(creds)
spreadsheets = client.open(G_SPREADSHEET_NAME)
