from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import matplotlib.pyplot as plt
import concurrent.futures
import requests
import shutil
import psutil
import time
import cv2
import os

p = psutil.Process(os.getpid())
p.nice(psutil.ABOVE_NORMAL_PRIORITY_CLASS)

class ImageTaskLog:
    '''This class contains functions for all the tasks that are
    performed on all images and also the functions to log and graph
    the CPU and Memory load.'''
    def __init__(self, url, number, 
                 download_directory, 
                 image_directory, 
                 video_directory,
                 start_time,
                 log_directory):
        '''Initialize class variables'''
        self.url = url
        self.number = number
        self.download_directory = download_directory
        self.image_directory = image_directory
        self.video_directory = video_directory
        self.start_time = start_time
        self.log_directory = log_directory

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
        video = cv2.VideoWriter(video_path, fourcc, 1, size)
        for image_name in images:
            img_path = os.path.join(self.copy_folder, image_name)
            img_read = cv2.imread(img_path)
            video.write(img_read)
        video.release()

    def log(self):
        '''This function logs CPU and memory usage during processing of each
        image into a .txt file.'''
        elapsed = time.perf_counter() - self.start_time
        elapsed_str = time.strftime("%M:%S", time.gmtime(elapsed))
        cpu = round(psutil.cpu_percent()*12, 1)
        memory = psutil.virtual_memory().percent
        log_text = (f"[{elapsed_str}]\timage{self.number}.jpg Completed\tCPU: {cpu}%\tRAM: {memory}%\n")
        with open(self.log_directory, "a") as f:
            f.write(log_text)    

    def task(self):
        '''This function runs all four (download, copy, video, log).'''
        self.download()
        self.copy()
        self.video()
        self.log()
        print(f'Task Completed Successfully for image{self.number}.jpg')

    def graph(log_directory):
        '''This function plots the graph for CPU and memory usage
        during processing of each image.'''
        elapsed_time = []
        cpu_usage = []
        memory_usage = []

        with open(log_directory, 'r') as f:
            for line in f:
                if "image" in line:
                    image_time = line.split(']')[0].strip('[')
                    minutes, seconds = map(int, image_time.split(':'))
                    total_seconds = minutes*60 + seconds
                    elapsed_time.append(total_seconds)
                    cpu_str = line.split("CPU:")[1].split('%')[0].strip()
                    ram_str = line.split("RAM:")[1].split('%')[0].strip()
                    cpu_usage.append(float(cpu_str))
                    memory_usage.append(float(ram_str))

        plt.figure(figsize=(12, 6))
        plt.plot(elapsed_time, cpu_usage, label='CPU Usage (%)', color='red')
        plt.plot(elapsed_time, memory_usage, label='RAM Usage (%)', color='blue')
        plt.xlabel('Elapsed Time (seconds)')
        plt.ylabel('Usage (%)')
        plt.title('CPU and Memory Usage Over Time')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


class ImageScrape:
    '''This class contains functions to setup chrome webdriver and scrape
    images.'''
    def __init__(self, chromedriver_path):
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
            soup = BeautifulSoup(html, "html.parser")
            all_images = soup.select('div.H8Rx8c > g-img > img')[30:]
            for img in all_images:
                if img.get('src'):
                    urls.append(img['src'])
                    if len(urls) >= max:
                        break
        self.driver.quit()
        return urls[:max]


def main():
    '''The main function initializes all paths, executes the
    ProcessPoolExecutor and calculates the total time taken.'''
    Start = time.perf_counter()

    chromedriver_path = "path_where_chromedriver_is_stored\\chromedriver.exe"
    download_directory = "path_where_images_will_be_saved"
    image_directory = "path_where_copies_will_be_saved"
    video_directory = "path_where_videos_will_be_saved"
    log_directory = "path_where_.txt_file_is_stored\\system_usage_log.txt"

    scraper = ImageScrape(chromedriver_path=chromedriver_path)
    image_urls = scraper.scroll_extract()

    Initial = time.perf_counter()
    with open(log_directory, "w") as f:
        f.write("### CPU & RAM Log Start ###\n\n")
        f.write(f'{round(Initial - Start)} seconds(s) were taken by Chrome web driver to start and load the webpage till the end\n\n')

    with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        for i, url in enumerate(image_urls, start=1):
            tasks = ImageTaskLog(url, i, download_directory,
                              image_directory, video_directory,
                              Start,log_directory)
            executor.submit(tasks.task)

    Finish = time.perf_counter()
    total_time = round((Finish - Start) / 60, 3)
    with open(log_directory, "a") as f:
        f.write(f"\nTotal time taken: {total_time} minutes\n")
    print(f'Executed in {total_time} Minutes...')

    ImageTaskLog.graph(log_directory)

if __name__ == '__main__':
    main()
