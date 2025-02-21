import os
import sys

from src.g_sheets_ops import all_worksheets, worksheet_name_validator
from src.logger import logger
from src.util import url_validator


def user_input_for_exported_file() -> str:
    """
    Function to get user input for exporting worksheet.

    Returns:
        str: The name of the worksheet to export.
    """
    while True:
        all_worksheets()
        filename = input("Enter worksheet name or type 'quit' and press enter to exit: ")
        if filename == 'quit':
            print('Exiting program')
            sys.exit(0)
        if not filename.strip():
            print('Worksheet name cannot be empty\n')
            continue
        if not worksheet_name_validator(filename):
            print(f'{filename} does not exist in spreadsheet\n')
            continue
        return filename


def user_input_for_scraping():
    """
    Function to get user input for scraping parameters.

    Returns:
        tuple: A tuple containing the base URL, the number of pages to scrape, and the worksheet name.
    """
    while True:
        base_url = input('Enter base url (e.g https://www.davidjones.com/men/shoes) or type "quit" and press enter to exit: ')
        if base_url.lower().strip() == 'quit':
            logger.info('Quit')
            sys.exit(0)
        if not base_url:
            print('Base URL cannot be empty')
            continue
        if url_validator(base_url):
            break
        print('Invalid URL')

    while True:
        url_cout = input('Enter amount of page to scrape or press enter for default amount(1) or type "quit" and press enter to exit: ')
        if url_cout.lower() == 'quit':
            logger.info('Quit')
            sys.exit(0)
        if not url_cout.strip():
            url_cout = 1
            break
        if url_cout.isdigit():
            url_cout = int(url_cout)
            break
        print('Only accept number')

    while True:
        sheet_name = input("Enter worksheet name or type 'quit' and press enter to exit: ")
        if sheet_name.lower().strip() == 'quit':
            logger.info('Quit')
            sys.exit(0)
        if not sheet_name:
            print('Worksheet name cannot be empty!')
            continue
        if worksheet_name_validator(sheet_name):
            while True:
                new_ws = input(f'Worksheet with name {sheet_name} already exist would you like to create a new worksheet (y/n): ').lower()
                if not new_ws.strip():
                    print('Option cannot be empty')
                    continue
                if new_ws == 'y':
                    break
                if new_ws == 'n':
                    return base_url, url_cout, sheet_name
                logger.error('Invalid input')
            continue
        return base_url, url_cout, sheet_name


def user_input_for_sheet_del():
    """
    Function to get user input for deleting a worksheet.

    Returns:
        str: The name of the worksheet to delete.
    """
    while True:
        all_worksheets()
        to_del = input('\nEnter sheet name to delete or type "quit" and press enter to exit: ')
        if to_del == 'quit':
            sys.exit(0)
        if not to_del:
            print('\nSheet name cannot be empty')
            continue
        if worksheet_name_validator(to_del):
            return to_del
        print('\nSheet name not found')


def user_input_for_display_sheet():
    """
    Function to get user input for displaying a worksheet.

    Returns:
        str: The name of the worksheet to display.
    """
    while True:
        all_worksheets()

        ws = input("\nEnter worksheet name or type 'quit' and press enter to exit the program: ")
        if ws.lower() == 'quit':
            sys.exit(0)
        if not ws.strip():
            print('\nWorksheet name cannot be empty')
            continue
        if not worksheet_name_validator(ws):
            print(f"{ws} does not exist in spreadsheet\n")
            continue
        return ws


def destination_to_go(action_name):
    """
       Function to get user input for the next action.

       Args:
           action_name (str): The name of the current action.

       Returns:
           int: The option chosen by the user.
       """
    while True:
        option = input(f"""
1. Continue {action_name}
2. Go to Main Menu
3. Exit Program

Choose option: """)

        if not option.strip():
            print('Option cannot be empty')
            continue
        if not option.isdigit():
            print('Accept numbers only')
            continue
        if int(option) not in range(1, 4):
            print('Invalid option')
            continue
        return int(option)


def user_input_main_menu():
    """
    Function to get user input for the main menu.

    Returns:
        int: The option chosen by the user.
    """
    while True:
        options = input("""
        
1. Scrape Website
2. View Worksheet
3. Export Worksheet
4. Delete Worksheet

Choose Number from the option above or type 'quit' and press enter to exit the program: """).strip()

        if options.lower() == 'quit':
            logger.info('Exit the program')
            sys.exit(0)
        if not options.isdigit():
            print('\nChoose available number!')
            continue
        if not options:
            print('Option cannot be empty\n')
            continue
        if int(options) not in range(1, 5):
            print('\nChoose avalilable number only!')
            continue
        return int(options)

