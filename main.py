from src.util import get_html_content, get_string_json, string_to_json, export_to_file, save_to_gspread
from src.parser import json_parser
from src import URL


def scrape(page_amount: int = 1):
    final_data = []
    for i in range(0, 90 * page_amount, 90):
        url = URL.format(page_number=i)
        html_content = get_html_content(url)
        string_json = get_string_json(html_content)
        json_data = string_to_json(string_json)
        parsed_data = json_parser(json_data)
        print(type(parsed_data))
        for data in parsed_data:
            final_data.append(data)
    dataframe = export_to_file(final_data)
    save_to_gspread(dataframe)


if __name__ == '__main__':
    scrape(2)


