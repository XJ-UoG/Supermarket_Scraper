import os
import requests
import json
from product import Product

# Function to get product data from a single page
def get_product_data(page):
    url = "https://website-api.omni.fairprice.com.sg/api/product/v2"
    params = {
        "algopers": "prm-ppb-1,prm-ep-1,t-epds-1,t-ppb-0,t-ep-0",
        "category": "fresh-milk",
        "experiments": "searchVariant-B,timerVariant-Z,substitutionBSVariant-B,gv-A,shelflife-B,ds-A,SDND_delivery_reason-C,ls_comsl-B,ls_deltime-ogA,ls_deltime-feA,cartfiller-a,catnav-hide,catbubog-B,sbanner-A,count-b,cam-a,priceperpiece-b,ls_deltime-sortA,promobanner-c,algopers-b,dlv_pref_mf-B,delivery_pref_ffs-A,delivery_pref_pfc-B,crtalc-B,rec-wtyl-ds,rec-fbt-ds",
        "includeTagDetails": "true",
        "metaData": "[object Object]",
        "orderType": "DELIVERY",
        "page": page,
        "pageType": "category",
        "slug": "fresh-milk",
        "storeId": "165",
        "url": "fresh-milk"
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data

# Directory to save images
image_dir = "fairprice_images"
os.makedirs(image_dir, exist_ok=True)

# Get the initial page to determine the total number of pages
initial_data = get_product_data(1)
total_pages = initial_data['data']['pagination']['total_pages']

# Collect data from all pages
all_products = []
for page in range(1, total_pages + 1):
    page_data = get_product_data(page)
    for product_data in page_data['data']['product']:
        product = Product(product_data, image_dir)
        all_products.append(product.to_dict())

# Save to JSON
with open('fairprice_milk.json', 'w') as f:
    json.dump(all_products, f, indent=4)
