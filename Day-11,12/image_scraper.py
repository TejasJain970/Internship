from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests
import time
import os

directory = 'path_where_images_will_be_saved'
chromedriver_path = "path_where_chromedriver.exe_is_stored"
i = 1
j = 0

input1 = str(input('\nWhat do you want to search for ?\n'))
    
Start = time.perf_counter()

input_new = '-'.join(input1.split(' '))
url = f'https://pixabay.com/images/search/{input_new}/?pagi=1'

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

time.sleep(3)
height = driver.execute_script("return document.body.scrollHeight")
height_new = round(height/50)

for _ in range(height_new):
    driver.execute_script("window.scrollBy(0, 50)")
    time.sleep(0.02)

html = driver.page_source
sauce = BeautifulSoup(html, "html.parser")

images = sauce.select('div.container--MwyXl > a > img')
if len(images) == 0:
    print(f'\nNo matches were found for "{input1}"')

for image in images:
    try:
        img_url = image['srcset']
        if img_url:
            source = img_url.split(', ')[-1]
            source = source.strip(' 2x')

        else:
            source = image['src']    

    except:
        source = image['src']

    filename = f'image{i}.jpg'
    try:
        img = requests.get(source)

    except:
        print(f'Error Saving {filename}')
        i += 1
        continue

    path = os.path.join(directory, filename)
    with open(path, 'wb') as f:
        save = f.write(img.content)
        print(f'Saved {filename}')
    
    i += 1
    j += 1    

driver.quit()
print(f'\nSaved {j} images for "{input1}"')

Finish = time.perf_counter()
total_time = round((Finish-Start)/60, 3)