import requests
from bs4 import BeautifulSoup
import pandas as pd

# Scrape product details from the product listing page
def scrape_product_listing(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = []

    # Extract product details from the HTML structure
    listings = soup.find_all('div', {'data-component-type': 's-search-result'})
    for listing in listings:
        product_url = 'https://www.amazon.in' + listing.find('a', {'class': 'a-link-normal'})['href']
        product_name = listing.find('span', {'class': 'a-size-medium'}).text.strip()
        product_price = listing.find('span', {'class': 'a-offscreen'}).text.strip()
        product_rating = listing.find('span', {'class': 'a-icon-alt'}).text.strip().split()[0]
        product_reviews = listing.find('span', {'class': 'a-size-base'}).text.strip().replace(',', '')

        products.append({
            'Product URL': product_url,
            'Product Name': product_name,
            'Product Price': product_price,
            'Rating': product_rating,
            'Number of Reviews': product_reviews
        })

    return products

# Scrape additional details from each product's URL
def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_description_element = soup.find('div', {'id': 'productDescription'})
    product_description = product_description_element.text.strip() if product_description_element else ''
    
    asin_element = soup.find('th', text='ASIN')
    asin = asin_element.find_next_sibling('td').text.strip() if asin_element else ''
    
    manufacturer_element = soup.find('th', text='Manufacturer')
    manufacturer = manufacturer_element.find_next_sibling('td').text.strip() if manufacturer_element else ''

    return {
        'Description': product_description,
        'ASIN': asin,
        'Product Description': product_description,
        'Manufacturer': manufacturer
    }


# Scrape product listing pages and fetch additional details for each product
# Scrape product listing pages and fetch additional details for each product
def scrape_amazon_products():
    all_products = []

    # Scrape product details from 20 pages of the product listing
    for page in range(1, 21):
        url = f'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{page}'
        products = scrape_product_listing(url)
        all_products.extend(products)

    # Scrape additional details for each product
    for product in all_products[:200]:
        url = product['Product URL']
        additional_details = scrape_product_details(url)
        product.update(additional_details)

    # Export data to CSV
    df = pd.DataFrame(all_products)
    df.to_csv('amazon_products.csv', index=False)
    print("Data exported successfully.")

# Run the scraping function
scrape_amazon_products()
