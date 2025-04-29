import json
import os
import re

import pandas as pd
from curl_cffi import requests
from ratelimit import limits, sleep_and_retry

from config.g_spreadsheet_config import spreadsheets
from config.scraping_config import MAX_CALLS, PERIOD, HEADERS
from src.data_req import DataRequirements
from src.logger import logger
from src.parser import json_parser


# Page handling
def url_validator(url: str) -> bool:
    """
    Check if the given url is active

    :param url: str
    :return: bool
    """
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestsError:
        return False


@sleep_and_retry
@limits(calls=MAX_CALLS, period=PERIOD)
def get_html_content(url: str) -> str | bool:
    """
    Fetch HTML from the website

    :param url: url of the site
    :return: HTML data structure
    """
    try:
        response = requests.get(url, impersonate='chrome')
        return response.text

    except TimeoutError as e:
        print()
        logger.error(f'get_html_content error : {e}')
        return False


def get_string_json(html_content: str) -> str | bool:
    """
    Get json data from given html

    :param html_content: html data structure
    :return: string json from html content
    """
    try:
        json_pattern = r'var trackingObj = (\{.*?\})\)\(window\);'
        json_data = re.search(json_pattern, html_content, re.DOTALL)

        if not json_data:
            print()
            logger.info(f'No json data available')

        json_data = json_data.group(1).replace("'", '"')
        data = re.sub(r'(?<!")(\b[a-zA-Z_][a-zA-Z0-9_]*\b)(?=\s*:)', r'"\1"', json_data)
        new_data = re.sub(r',"fhSourceId":\s*"[^"]*"[\s\S]*?push\(trackingObj\)[\s\S]*?}', '', data)
        new_json_data = re.sub(r',(\s*})', r'\1', new_data)
        return new_json_data
    except Exception as e:
        print()
        logger.error(f'Getting json from html content failed: {e}')
        return False


def string_to_json(data_string: str) -> any:
    """
    Load string data as a JSON so it could be parsed as a dictionary

    :param data_string: string JSON to convert
    :return: loaded string as data JSON
    """
    try:
        loaded_data = json.loads(data_string)
        return loaded_data
    except Exception as e:
        print()
        logger.error(f'loads string to json error : {e}')


def page_process(url: str) -> list[DataRequirements] | None:
    """
    Process given URL into list[DataRequirement]

    :param url: base url of page to scrape
    :return: a list of DataRequirement object
    """
    html_content = get_html_content(url)
    if not html_content:
        return None

    string_json = get_string_json(html_content)
    json_data = string_to_json(string_json)
    return json_parser(json_data)


# File Handling
def to_file(data: list[DataRequirements] | str, filename: str) -> bool | None:
    """
    Export given data into .xlsx or .csv

    :param data: list of DataRequirement object | worksheet name
    :param filename: exported filename
    :return: .xlsx and .csv file
    """
    try:
        save_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
        excel_path = os.path.join(save_dir, f'{filename}.xlsx')
        csv_path = os.path.join(save_dir, f'{filename}.csv')

        if isinstance(data, list):
            rows = [[d.Brand, d.ID, d.Name, d.Price, d.PriceRrp, d.Discount, d.Product_URL, d.Image_URL] for d in data]
            df = pd.DataFrame(rows, columns=HEADERS)
            df['Product URL'] = df['Product URL'].apply(lambda x: f'=HYPERLINK("{x}", "{x}")')
            df['Image URL'] = df['Image URL'].apply(lambda x: f'=HYPERLINK("{x}", "{x}")')
            df.to_excel(excel_path, index=False)
            df.to_csv(csv_path, index=False, encoding="utf-8-sig")
            print(f'Data exported successfully as {filename}.xlsx and {filename}.csv in {save_dir}')

        else:
            to_export = spreadsheets.worksheet(data)
            data_values = to_export.get_all_values()
            df = pd.DataFrame(data_values[1:], columns=data_values[0])
            df['Product URL'] = df['Product URL'].apply(lambda x: f'=HYPERLINK("{x}", "{x}")')
            df['Image URL'] = df['Image URL'].apply(lambda x: f'=HYPERLINK("{x}", "{x}")')
            df.to_excel(excel_path, index=False)
            df.to_csv(csv_path, index=False, encoding="utf-8-sig")
            print(f'Data exported successfully as {filename}.xlsx and {filename}.csv in {save_dir}')

    except Exception as e:
        print()
        print(f'Exporting data error: {e}')
        return False


# Removal Verifiction
def sheet_removal_verif() -> bool | None:
    """
    Verification to remove worksheet from spreadsheet

    :return: y for True, n for False
    """
    while True:
        verif = input('Confirm delete y/n: ').lower()
        if not verif.strip():
            print('Confirmation cannot be empty')
            continue
        if verif == 'y':
            return True
        elif verif == 'n':
            return False
        logger.info('Invalid input')
