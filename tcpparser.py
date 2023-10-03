import requests
from bs4 import BeautifulSoup
import json

base_url = 'http://127.0.0.1:8080'

# Function to fetch and parse a page
def fetch_and_parse_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Failed to fetch page: {url}")
        return None

# Function to extract product details from a product page
def extract_product_details(product_url):
    product_page = fetch_and_parse_page(product_url)
    if product_page:
        values = [value.strip().split(' : ')[-1] for value in product_page.find('h2').stripped_strings]

        book_info = {
            "name": values[0],
            "author": values[1],
            "price": float(values[2]),
            "description": values[3]
        }

# Convert the dictionary to a JSON object
        json_object = json.dumps(book_info, indent=4)
        return json_object
    return None

# Function to find product links on the products listing page
def find_product_links(products_listing_url):
    products_listing_page = fetch_and_parse_page(products_listing_url)
    if products_listing_page:
        product_links = []
        for product_link in products_listing_page.find_all('a'):
            product_links.append(product_link['href'])
        return product_links
    return []

# Main function to start parsing
def main():
    # Fetch the product listing page URL
    products_listing_url = base_url + '/books'

    # Get product links from the product listing page
    product_links = find_product_links(products_listing_url)

    # Iterate through product links and extract product details
    for product_link in product_links:
        product_url = base_url + product_link
        product_details = extract_product_details(product_url)
        if product_details:
            print("Product Details:")
            print(product_details)
            print("\n")

if __name__ == '__main__':
    main()