from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
import time
import os

directory = 'path_where_images_will_be_saved'
page_number = 1

input1 = str(input('\nWhat do you want to search for ?\n'))
    
input_new = '-'.join(input1.split(' '))
url = f'https://pixabay.com/images/search/{input_new}/?pagi=1'

chromedriver_path = "path_where_chromedriver.exe_is_saved"

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument("--log-level=3")
options.add_argument("--enable-javascript")
options.add_experimental_option("prefs", {"profile.cookie_controls_mode": 0})

service = Service(executable_path=chromedriver_path)

driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

driver.get(url)

heading = driver.find_element(by=By.CLASS_NAME, value='indicator--Nf9Sc')
pages = heading.text
total_pages = pages.split('of ')[-1]
int_total_pages = int(total_pages)
time.sleep(5)
print(f'\nTotal {total_pages} pages found for "{input1}"')

while True:
    input2 = input(f'\nHow many pages do you want to download ? (Maximum 100 images per page) (Maximum {total_pages} pages)\n')
    try:
        input2 = int(input2)
        if input2 > int_total_pages:
            print('\nPlease enter a valid integer !')
            continue
        break

    except:
        print('\nPlease enter a valid integer !')
        continue   

Start = time.perf_counter()

while page_number <= input2:
    url = f'https://pixabay.com/images/search/{input_new}/?pagi={page_number}'
    driver.get(url)
    time.sleep(2)

    height = driver.execute_script("return document.body.scrollHeight")
    height_new = round(height/50)

    for _ in range(height_new):
        driver.execute_script("window.scrollBy(0, 50)")
        time.sleep(0.015)

    html = driver.page_source
    sauce = BeautifulSoup(html, "lxml")

    images = sauce.select('div.container--MwyXl > a > img')

    for image in images:
        source = image['src']
        filename = source.split('/')[-1]
        img = requests.get(source)
        path = os.path.join(directory, filename)
        with open(path, 'wb') as f:
            save = f.write(img.content)
            print(f'Saved {filename}')

    page_number += 1   

Finish = time.perf_counter()
print(f'\nExecuted in {round(Finish-Start, 3)} seconds...')
                
