from dataclasses import dataclass


@dataclass
class DataRequirements:
    Name: str
    ID: str
    Price: float
    Brand: str
    Product_URL: str
    Image_URL: str
