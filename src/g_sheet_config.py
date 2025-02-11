import gspread
from google.oauth2.service_account import Credentials
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]


creds = Credentials.from_service_account_file(GOOGLE_SHEET_CREDENTIALS_FILE, scopes=scope)
client = gspread.authorize(creds)
sheets = client.open(G_SHEETNAME).sheet1