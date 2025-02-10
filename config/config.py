PAGE_SIZE = 90
BASE_URL = "https://www.davidjones.com/men/shoes"


def get_full_url(page_amount: int) -> str:
    return f'{BASE_URL}?src=fh&size={PAGE_SIZE}&offset={page_amount}'

