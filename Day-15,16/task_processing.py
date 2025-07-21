from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import concurrent.futures
import requests
import shutil
import psutil
import time
import cv2
import os

class ImageTask:
    '''This class contains functions for all the tasks that are
    performed on all images.'''
    def __init__(self, url, number, 
                 download_directory, 
                 image_directory, 
                 video_directory):
        '''Initialize class variables'''
        self.url = url
        self.number = number
        self.download_directory = download_directory
        self.image_directory = image_directory
        self.video_directory = video_directory

    def download(self):
        '''This function downloads the images that were scraped from
        google.'''
        filename = f'image{self.number}.jpg'
        img_url = requests.get(self.url)
        self.image_path = os.path.join(self.download_directory, filename)
        with open(self.image_path, 'wb') as f:
            f.write(img_url.content)    

    def copy(self):
        '''This function creates a new directory for each image and
        makes 1000 copies for each image.'''
        folder = os.path.join(self.image_directory, f'image{self.number}')
        os.makedirs(folder, exist_ok=True)
        for j in range(1, 1001):
            destination = os.path.join(folder, f'{self.number}.{j}.jpg')
            shutil.copy(self.image_path, destination)
        self.copy_folder = folder

    def video(self):
        '''This function creates a slideshow video for all image copies
        in each created directory.'''
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
        '''This function runs all three (download, copy, video).'''
        self.download()
        self.copy()
        self.video()
        print(f'Task Completed Successfully for image{self.number}.jpg')

class ImageScrape:
    '''This class contains functions to setup chrome webdriver and scrape
    images.'''
    def __init__(self, chromedriver_path ):
        '''Initialize class variables'''
        self.url = "https://google.com/search?q=nature&udm=2"
        self.chromedriver_path = chromedriver_path
        self.driver = self.driver_setup()
        
    def driver_setup(self):
        '''This function initializes options and services for the chrome
        webdriver.'''
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument("--log-level=3")
        service = Service(executable_path=self.chromedriver_path)
        return webdriver.Chrome(service=service, options=options)

    def scroll_extract(self, max=1000):
        '''This function scrolls the webpage to the end and then makes a
        list for all the extracted image urls.'''
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
    '''The main function initializes all paths, executes the
    ThreadPoolExecutor and calculates the total time taken.'''
    Start = time.perf_counter()

    chromedriver_path = "path_where_chromedriver_is_stored\\chromedriver.exe"
    download_directory = "path_where_images_will_be_saved"
    image_directory = "path_where_copies_will_be_saved"
    video_directory = "path_where_videos_will_be_saved"

    p = psutil.Process(os.getpid())
    p.nice(psutil.HIGH_PRIORITY_CLASS)

    scraper = ImageScrape(chromedriver_path=chromedriver_path)
    image_urls = scraper.scroll_extract()

    with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        for i, url in enumerate(image_urls, start=1):
            tasks = ImageTask(url, i, download_directory,
                              image_directory, video_directory)
            executor.submit(tasks.task)

    Finish = time.perf_counter()
    print(f'Executed in {round((Finish-Start)/60, 3)} Minutes...')

if __name__ == '__main__':
    main()