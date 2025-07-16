from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import concurrent.futures
import requests
import shutil
import time
import cv2
import os

class ImageTask:
    def __init__(self, url, number, download_directory, image_directory, video_directory):
        self.url = url
        self.number = number
        self.download_directory = download_directory
        self.image_directory = image_directory
        self.video_directory = video_directory

    def download(self):
        filename = f'image{self.number}.jpg'
        img_url = requests.get(self.url)
        self.image_path = os.path.join(self.download_directory, filename)
        with open(self.image_path, 'wb') as f:
            f.write(img_url.content)    

    def copy(self):
        folder = os.path.join(self.image_directory, f'image{self.number}')
        os.makedirs(folder, exist_ok=True)
        for j in range(1, 1001):
            destination = os.path.join(folder, f'{self.number}.{j}.jpg')
            shutil.copy(self.image_path, destination)
        self.copy_folder = folder

    def video(self):
        images = [img for img in os.listdir(self.copy_folder)]
        frame = cv2.imread(os.path.join(self.copy_folder, images[0]))
        height, width, _ = frame.shape
        size = (width, height)
        video_path = os.path.join(self.video_directory, f'video{self.number}.mp4')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(video_path, fourcc, 0.5, size)
        for image_name in images:
            img_path = os.path.join(self.copy_folder, image_name)
            img_read = cv2.imread(img_path)
            video.write(img_read)
        video.release()        

    def task(self):
        self.download()
        self.copy()
        self.video()
        print(f'Task Completed Successfully for image{self.number}.jpg')

class ImageScrape:
    def __init__(self, chromedriver_path ):
        self.url = "https://google.com/search?q=nature&udm=2"
        self.chromedriver_path = chromedriver_path
        self.driver = self.driver_setup()
        
    def driver_setup(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument("--log-level=3")
        service = Service(executable_path=self.chromedriver_path)
        return webdriver.Chrome(service=service, options=options)

    def scroll_extract(self, max=1000):
        urls = []
        while len(urls) < max:
            self.driver.get(self.url)   
            time.sleep(1)
            for _ in range(5000):
                self.driver.execute_script("window.scrollBy(0, 100)")
            html = self.driver.page_source
            sauce = BeautifulSoup(html, "html.parser")
            all_images = sauce.select('div.H8Rx8c > g-img > img')[30:]
            for img in all_images:
                urls.append(img['src'])
                if len(urls) >= max:
                    break    
        self.driver.quit()
        return urls[:max]

def main():
    Start = time.perf_counter()

    chromedriver_path = "F:\\Tejas\\RESOURCES\\Driver\\chromedriver.exe"
    download_directory = "F:\\Downloads"
    image_directory = "F:\\IMAGES"
    video_directory = "F:\\VIDEOS"

    scraper = ImageScrape(chromedriver_path=chromedriver_path)
    image_urls = scraper.scroll_extract()

    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        for i, url in enumerate(image_urls, start=1):
            tasks = ImageTask(url, i, download_directory, image_directory, video_directory)
            executor.submit(tasks.task)

    Finish = time.perf_counter()
    print(f'Executed in {round((Finish-Start)/60, 3)} Minutes...')

if __name__ == '__main__':
    main()    