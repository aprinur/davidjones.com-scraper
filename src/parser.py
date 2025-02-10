from src.data_req import DataRequirements


def json_parser(json_object: dict):
    try:
        if json_object:
            all_data = []
            for json in json_object.get('products', {}).get('catalogue', []):
                data = {
                    "name": json.get('name', ''),
                    "id_": json.get('id', ''),
                    "price": json.get('price', 0.00),
                    "brand": json.get('brand', ''),
                    "product_url": json.get('productURL', ''),
                    "image_url": json.get('productImageURL', ''),
                }
                all_data.append(data)

            return [DataRequirements(
                Name=item['name'],
                ID=item['id_'],
                Price=item['price'],
                Brand=item['brand'],
                Product_URL=item['product_url'],
                Image_URL=item['image_url']
            ) for item in all_data]
        else:
            return False
    except Exception as e:
        print(f'Error parsing json: {e}')