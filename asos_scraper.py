import requests
from bs4 import BeautifulSoup
import os
import time

url = "https://www.asos.com/women/dresses/cat/?cid=8799&_gl=1*pqrypr*_up*MQ..&gclid=e2751bd4baec1a0c6efa7c2995f34d3a&gclsrc=3p.ds"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': url  
}

retries = 3
response = None  # Initialize the response variable outside the loop

for attempt in range(retries):
    try:
        response = requests.get(url, headers=headers, timeout=5) 
        print(f"Attempt {attempt + 1}: Status Code: {response.status_code}")

        if response.status_code == 403:
            print("Access Forbidden. The server blocked the request.")
            break          
        if response.status_code != 200:
            print("Failed to fetch the page.")
            if attempt < retries - 1:
                print("Retrying...")
                time.sleep(2 ** attempt) 
            else:
                print("Failed after multiple attempts.")
            continue
        else:
            print("Page fetched successfully.")
            break
    except requests.exceptions.RequestException as e:
        print(f"Error on attempt {attempt + 1}: {e}")
        if attempt < retries - 1:
            print("Retrying...")
            time.sleep(2 ** attempt)  # Exponential backoff (2, 4, 8 seconds)
        else:
            print("Failed after multiple attempts.")

if response and response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all('article', role='group', aria_label='product')

    os.makedirs('images', exist_ok=True)

    for product in products:
        product_name = product.find('h2', class_='productDescription_sryaw').get_text(strip=True) if product.find('h2', class_='productDescription_sryaw') else 'No Name'
        product_url = product.find('a', class_='productLink_KM4PI')['href'] if product.find('a', class_='productLink_KM4PI') else 'No URL'
        price_tag = product.find('p', class_='container_s8SSI')
        price = price_tag.find('span', class_='price__B9LP').get_text(strip=True) if price_tag else 'N/A'        
        img_tag = product.find('img')
        image_url = 'https:' + img_tag['src'] if img_tag and 'src' in img_tag.attrs else None
        if image_url:
            img_name = image_url.split('/')[-1]
            img_path = os.path.join('images', img_name)

            img_data = requests.get(image_url).content
            with open(img_path, 'wb') as f:
                f.write(img_data)
                print(f"Product: {product_name}")
                print(f"URL: {product_url}")
                print(f"Price: {price}")
                print(f"Image URL: {image_url}")
                print('-' * 30)
else:
    print("No successful response was received. Exiting.")
