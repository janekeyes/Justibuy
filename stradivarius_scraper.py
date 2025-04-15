import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Setup Selenium driver
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

#options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the Stradivarius product page
url = "https://www.stradivarius.com/ie/woman/clothing/view-all-c1750029.html"
driver.get(url)
time.sleep(5)

# Scroll multiple times to load dynamic content
SCROLL_PAUSE_TIME = 3
last_height = driver.execute_script("return document.body.scrollHeight")

for i in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

    
with open("page_dump.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

print("📄 Dumped page source to page_dump.html")

# Try finding product elements
product_elements = driver.find_elements(By.CSS_SELECTOR, '[id^="ProductGridItem_"]')
if not product_elements:
    product_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-cy="grid-product"]')

print(f"Found {len(product_elements)} product elements.")

results = []

for product in product_elements:
    try:
        title = product.find_element(By.CSS_SELECTOR, '[data-cy="grid-product-title"]').text
        price = product.find_element(By.CSS_SELECTOR, '[data-cy="grid-product-price"]').text
        img = product.find_element(By.CSS_SELECTOR, 'img[data-cy="grid-item-image"]').get_attribute("src")

        results.append({
            "title": title,
            "price": price,
            "image_url": img
        })
    except Exception as e:
        print("Error parsing a product:", e)

# Save to CSV
csv_filename = "stradivarius_products.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["title", "price", "image_url"])
    writer.writeheader()
    writer.writerows(results)

print(f"✅ Saved {len(results)} items to {csv_filename}")
driver.quit()
