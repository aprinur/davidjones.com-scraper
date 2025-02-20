PAGE_SIZE = 90
MAX_CALLS = 60
PERIOD = 60
HEADERS = ['Brand', 'ID', 'Name', 'Price (AUD)', 'Price Rrp', 'Discount', 'Product URL', 'Image URL']


def get_full_url(page_amount: int, base_url: str) -> str:
    """
    Constructs the full URL for pagination.

    :param page_amount: amount of page to scrape
    :param base_url: base url of the page
    :return: full URl as a string
    """
    return f'{base_url}?src=fh&size={PAGE_SIZE}&offset={page_amount}'
