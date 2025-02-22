from dataclasses import asdict

import gspread.exceptions
import pandas as pd
from tabulate import tabulate

from config.g_spreadsheet_config import spreadsheets
from config.scraping_config import HEADERS
from src.logger import logger


def worksheet_name_validator(worksheet_name):
    """
    Validates if a worksheet with the given name exists.

    Args:
        worksheet_name (str): The name of the worksheet to validate.

    Returns:
        bool: True if the worksheet exists, False otherwise.
    """
    try:
        spreadsheets.worksheet(worksheet_name)
        return True
    except gspread.exceptions.WorksheetNotFound:
        return False


def to_g_worksheet(sheetname, data):
    """
    Saves data to a Google Sheets worksheet. If the worksheet exists, it appends new rows.
    If the worksheet does not exist, it creates a new one and saves the data.

    Args:
        sheetname (str): The name of the worksheet.
        data (list[DataRequirements]): The data to save.

    Returns:
        None
    """
    try:
        data_row = [[d.Brand, d.ID, d.Name, d.Price, d.PriceRrp, d.Discount, d.Product_URL, d.Image_URL] for d in data]
        if sheetname in {ws.title for ws in spreadsheets.worksheets()}:
            worksheet_value = spreadsheets.worksheet(sheetname)
            existing_data = set(tuple(row) for row in worksheet_value.get_all_values())
            new_rows = [row for row in data_row if tuple(row) not in existing_data]
            if new_rows:
                spreadsheets.worksheet(sheetname).append_rows(new_rows)
                print(f'\nResult added to worksheet {sheetname}')
        else:
            new_data = [HEADERS] + data_row
            new_sheet = create_new_sheet(sheetname)
            new_sheet.update('A1', new_data)
            print(f'\nData saved in worksheet {sheetname} ')

    except Exception as e:
        print(f'Error saving to worksheet {sheetname}: {e}')


def create_new_sheet(sheet_name):
    """
    Creates a new worksheet with the given name.

    Args:
        sheet_name (str): The name of the new worksheet.

    Returns:
        gspread.models.Worksheet: The created worksheet.
    """
    new_sheet = spreadsheets.add_worksheet(sheet_name, rows=100, cols=26)
    print(f'Worksheet {sheet_name} has created')
    return new_sheet


def all_worksheets():
    """
    Prints the titles of all worksheets in the spreadsheet.

    Returns:
        None
    """
    for key, value in enumerate([ws.title for ws in spreadsheets.worksheets()]):
        print(f'{key+1}. {value}')


def worksheet_values(workshet_name):
    """
    Prints the values of the specified worksheet in a tabulated format.

    Args:
        workshet_name (str): The name of the worksheet.

    Returns:
        None
    """
    sh = spreadsheets.worksheet(workshet_name)
    df = pd.DataFrame(sh.get_all_values())
    print(f"\n{tabulate(df, headers="firstrow", tablefmt="simple_grid")}")


def del_sheet(worksheet_name):
    """
    Deletes the specified worksheet.

    Args:
        worksheet_name (str): The name of the worksheet to delete.

    Returns:
        None
    """
    try:
        worksheet = spreadsheets.worksheet(worksheet_name)
        spreadsheets.del_worksheet(worksheet)
        print(f'Worksheet {worksheet_name} has been deleted.')

    except Exception as e:
        logger.info(f'Worksheet deletion error: {e}')

