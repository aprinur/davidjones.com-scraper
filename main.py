import sys

from config.scraping_config import get_full_url, PAGE_SIZE
from src.g_sheets_ops import to_g_worksheet, worksheet_values, del_sheet
from src.logger import logger
from src.user_input import user_input_for_exported_file, user_input_for_sheet_del, user_input_for_scraping, \
    user_input_for_display_sheet, user_input_main_menu
from src.util import page_process, to_file, sheet_removal_verif


def scrape() -> None:
    """
    Function to scrape website and save the result as .xlsx and .csv

    :return: .xlsx and .csv file
    """
    try:
        while True:
            final_data = []
            base_url, amount, sheet_name = user_input_for_scraping()
            for page_num in range(amount):
                offset = page_num * PAGE_SIZE
                url = get_full_url(offset, base_url)

                data = page_process(url)
                if data:
                    final_data.extend(data)

            if final_data:
                to_g_worksheet(sheet_name, final_data)
                to_file(final_data, sheet_name)

            if handle_destination('Scraping'):
                continue

    except Exception as e:
        logger.error(f'Scraping failed {e}')
        return None


def display_worksheet() -> None:
    """
    Function to display a worksheet

    :return: none
    """
    while True:
        to_display = user_input_for_display_sheet()
        worksheet_values(to_display)
        if handle_destination('View Worksheet'):
            continue


def export_sheet() -> None:
    """
    Function to export google worksheet

    :return: .xlsx and .csv file
    """
    while True:
        to_export = user_input_for_exported_file()
        to_file(to_export, to_export)

        if handle_destination('Export Worksheet'):
            continue


def delete_sheet() -> None:
    """
    Function to remove worksheet from Google spreadsheet

    :return: none
    """
    while True:
        sheet_name = user_input_for_sheet_del()
        if not sheet_removal_verif():
            print('Deletion aborted')
            if handle_destination('Delete Worksheet'):
                continue
        else:
            del_sheet(sheet_name)
            if handle_destination('Delete Worksheet'):
                continue


def handle_destination(action_name) -> bool | None:
    """
    Function to mapping where to go next

    :param action_name: On what function this function in
    :return: none
    """
    from src.user_input import destination_to_go

    dest = destination_to_go(action_name)
    if dest == 1:
        return True
    if dest == 2:
        main_menu()
    if dest == 3:
        print('Exit the program')
        sys.exit(0)
    return False


def main_menu() -> None:
    """
    Function to navigate what to do

    :return: None
    """
    options = user_input_main_menu()

    if options == 1:
        scrape()
    if options == 2:
        display_worksheet()
    if options == 3:
        export_sheet()
    if options == 4:
        delete_sheet()
    if options == 'quit':
        sys.exit(0)


if __name__ == '__main__':
    main_menu()

"""
edit: tes all possibility

"""
