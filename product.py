import os
import requests
import json

class Product:
    def __init__(self, product_data, image_dir):
        self.id = product_data['id']
        self.name = product_data['name']
        self.final_price = product_data['final_price']
        self.unit_of_weight = product_data['metaData'].get('Unit Of Weight') if 'metaData' in product_data else None
        self.discounted_price = self.get_discounted_price(product_data)
        self.image_paths = self.download_images(product_data.get('images', []), image_dir)
        
    def get_discounted_price(self, product_data):
        discounted_price = self.final_price
        if 'offers' in product_data and product_data['offers']:
            for offer in product_data['offers']:
                offer_price = offer.get('price')
                if offer_price is not None and offer_price < discounted_price:
                    discounted_price = offer_price
        return discounted_price

    def download_images(self, image_urls, image_dir):
        image_paths = []
        for image_url in image_urls:
            image_name = f"{self.id}_{os.path.basename(image_url)}"
            image_path = os.path.join(image_dir, image_name)
            if not os.path.exists(image_path):
                response = requests.get(image_url)
                if response.status_code == 200:
                    with open(image_path, 'wb') as f:
                        f.write(response.content)
            image_paths.append(image_path)
        return image_paths

    def to_dict(self):
        return {
            "name": self.name,
            "unit_of_weight": self.unit_of_weight,
            "final_price": self.final_price,
            "discounted_price": self.discounted_price,
            "image_paths": self.image_paths
        }
