from src.data_req import DataRequirements


def json_parser(json_object: dict) -> list[DataRequirements]:
    """
    Parse data based on DataRequirement

    :param json_object: json data to parse
    :return: list[DataRequirement]
    """
    try:
        if json_object:
            all_data = []
            for json in json_object.get('products', {}).get('catalogue', []):
                all_data.append(DataRequirements(
                    Brand=json.get('brand', ''),
                    ID=json.get('id', ''),
                    Name=json.get('name', ''),
                    Price=json.get('price', 0.00),
                    PriceRrp=json.get('priceRrp', 0.00),
                    Discount=json.get('discountValue', 0.00),
                    Product_URL=json.get('productURL', ''),
                    Image_URL=json.get('productImageURL', '')))
            return all_data
        else:
            return []
    except Exception as e:
        print(f'Error parsing json: {e}')