from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import concurrent.futures
import requests
import time
import os

directory = 'path_where_images_will_be_downloaded'
chromedriver_path = "path_where_chromedriver_is_stored\\chromedriver.exe"

i = 1
image_count = 0

def scraper(image, number):
    source = image['src']
    filename = f'image{number}.jpg'
    img = requests.get(source)

    path = os.path.join(directory, filename)

    with open(path, 'wb') as f:
        f.write(img.content)
        print(f'Saved {filename}') 
    
Start = time.perf_counter()
  
url = f'https://www.google.com/search?q=nature&sxsrf=AE3TifONYbl6Nk5o9M9hflMV0W-vnl5hvw:1752482949620&udm=2'

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument("--log-level=3")
options.add_argument("--enable-javascript")
options.add_experimental_option("prefs", {"profile.cookie_controls_mode": 0})

service = Service(executable_path=chromedriver_path)

driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

for _ in range(1,3):
    driver.get(url)   

    time.sleep(1)
    for _ in range(5000):
        driver.execute_script("window.scrollBy(0, 100)")

    html = driver.page_source
    sauce = BeautifulSoup(html, "html.parser")

    all_images = sauce.select('div.H8Rx8c > g-img > img')
    refined_images = all_images[30:]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for image in refined_images:
            executor.submit(scraper, image, i)
            i += 1
            image_count += 1
            if image_count == 1000:
                break

print(f'\nSaved {image_count} images of nature')

Finish = time.perf_counter()
total_time = round((Finish-Start)/60, 3)
