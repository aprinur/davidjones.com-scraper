from curl_cffi import requests
from src import sheets
import pandas as pd
import openpyxl
import json
import re
import os


def get_string_json(html_content: str):
    try:
        json_pattern = r'var trackingObj = (\{.*?\})\)\(window\);'
        json_data = re.search(json_pattern, html_content, re.DOTALL)

        if not json_data:
            print('No json data')

        json_data = json_data.group(1).replace("'", '"')
        data = re.sub(r'(?<!")(\b[a-zA-Z_][a-zA-Z0-9_]*\b)(?=\s*:)', r'"\1"', json_data)
        new_data = re.sub(r',"fhSourceId":\s*"[^"]*"[\s\S]*?push\(trackingObj\)[\s\S]*?}', '', data)
        new_json_data = re.sub(r',(\s*})', r'\1', new_data)
        return new_json_data
    except Exception as e:
        print(f'get_string_json error: {e}')
        return False


def string_to_json(data_string: dict):
    try:
        loaded_data = json.loads(data_string)
        return loaded_data
    except Exception as e:
        print(f'string_to_json error: {e}')


def get_html_content(URL):
    try:
        response = requests.get(URL, impersonate='chrome')
        html_content = response.text
        if response.status_code != 200:
            print(f'error {response.status_code}')
        return html_content
    except TimeoutError as e:
        print(f'get_html_content: error {e}')
        return False


def export_to_file(data, filename: str):
    try:
        if data:
            save_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
            excel_path = os.path.join(save_dir, f'{filename}.xlsx')

            df = pd.DataFrame(data)
            df['Product_URL'].apply(lambda x: f'=HYPERLINK("{x}", "{x}"')
            df['Image_URL'].apply(lambda x: f'=HYPERLINK("{x}", "{x}"')
            df.to_excel(excel_path, engine='openpyxl', index=False)
            print(f'Data exported as {filename} in {save_dir}')
            return df

    except Exception as e:
        print(f'Save to file error : {e}')


def save_to_gspread(dataframe):
    try:
        sheets.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())
    except Exception as e:
        print(f'error save to gspread: {e}')