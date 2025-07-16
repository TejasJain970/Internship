import scraper_threading
import concurrent.futures
import shutil
import time
import cv2
import os

def copier(k):
    image_directory = f'path_where_images_were_downloaded\\image{k}.jpg'
    for j in range(1, scraper_threading.image_count + 1):
        new_directory = f'path_where_images_will_be_copied\\image{k}\\{k}.{j}.jpg'
        shutil.copy(image_directory, new_directory)

def video(v):
    image_folder = f'path_where_images_were_copied\\image{v}'
    video_file = f'path_where_video_will_be_saved\\image{v}.mp4'
    fps = 1

    images = [img for img in os.listdir(image_folder)]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, _ = frame.shape
    size = (width, height)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_file, fourcc, fps, size)

    for image_name in images:
        img_path = os.path.join(image_folder, image_name)
        img = cv2.imread(img_path)
        video.write(img)

    video.release()

Start = time.perf_counter()

for i in range(1, scraper_threading.image_count + 1):
    new_directory = f"path_where_images_will_be_copied\\image{i}"
    try:
        os.makedirs(new_directory)

    except FileExistsError:
        print(f"Directory '{new_directory}' already exists.")
        break
    
    except Exception as e:
        print(f"ERROR: {e}")
        break    

print(f'\nCreated {scraper_threading.image_count} directories for copies of {scraper_threading.image_count} images')
print('Copying the saved images from source path to the newly created directories.....')

with concurrent.futures.ThreadPoolExecutor(24) as executor:
    executor.map(copier, range(1, scraper_threading.image_count + 1))

print(f'\nCopied {scraper_threading.image_count*scraper_threading.image_count} images in {scraper_threading.image_count} folders with {scraper_threading.image_count} copies in each folder respectively')
print(f'Creating videos for all images in all the folders.....')

with concurrent.futures.ThreadPoolExecutor(24) as executor:
    executor.map(video, range(1, scraper_threading.image_count + 1))

print(f'Created {scraper_threading.image_count} videos for all images in the {scraper_threading.image_count} folders respectively')
Finish = time.perf_counter()
total_time = round((Finish-Start)/60, 3)

print(f'\nExecuted in {round(scraper_threading.total_time + total_time, 3)} minutes...')


