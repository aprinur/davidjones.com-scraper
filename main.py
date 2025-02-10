from src.util import get_html_content, get_string_json, string_to_json, export_to_file, save_to_gspread
from src.parser import json_parser
from config.config import get_full_url, PAGE_SIZE
import logging
from src import URL

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(messege)s'
)

logger = logging.getLogger(__name__)


def scrape(page_amount: int = 1):
    try:
        final_data = []
        for page_num in range(page_amount):
            offset = page_num * PAGE_SIZE
            url = get_full_url(offset)

            data = page_process(url)
            if data:
                final_data.extend(data)
        if final_data:
            df = export_to_file(final_data)
            return save_to_gspread(df)
        return None
    except Exception as e:
        logger.error(f'Scraping failed {e}')
        return None


def page_process(url):
    html_content = get_html_content(url)
    if not html_content:
        return None

    string_json = get_string_json(html_content)
    json_data = string_to_json(string_json)
    return json_parser(json_data)


if __name__ == '__main__':
    scrape(2)


