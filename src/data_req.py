from dataclasses import dataclass


@dataclass
class DataRequirements:

    Brand: str
    ID: str
    Name: str
    Price: float
    PriceRrp: float
    Discount: float
    Product_URL: str
    Image_URL: str
