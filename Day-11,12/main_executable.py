import image_scraper
import shutil
import time
import cv2
import os

i = 1
j = 1
k = 1
v = 1

Start = time.perf_counter()

while i <= image_scraper.j:
    new_directory = f"path_where_directories_will_be_stored\\image{i}"
    try:
        os.makedirs(new_directory)
        i += 1

    except FileExistsError:
        print(f"Directory '{new_directory}' already exists.")
        break
    
    except Exception as e:
        print(f"ERROR: {e}")
        break    

print(f'\nCreated {image_scraper.j} directories for copies of {image_scraper.j} images')
print('Copying the saved images from source path to the newly created directories.....')

while k <= image_scraper.j:
    image_directory = f'path_where_images_were_saved\\image{k}.jpg'
    while j <= image_scraper.j:
        new_directory = f'path_where_directories_are_stored\\image{k}\\{k}.{j}.jpg'
        shutil.copy(os.path.join(image_directory), new_directory)
        j += 1
    j = 1
    k += 1
print(f'\nCopied {image_scraper.j*image_scraper.j} images in {image_scraper.j} folders with {image_scraper.j} copies in each folder respectively')
print(f'Creating videos for all images in all the folders.....')

while v <= 100:
    image_folder = f'path_where_directories_are_stored\\image{v}'
    video_file = f'path_where_videos_will_be_stored\\image{v}.mp4'
    video_name = f'image{v}.mp4'
    fps = 1

    images = [img for img in os.listdir(image_folder)]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    size = (width, height)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_file, fourcc, fps, size)

    for image_name in images:
        img_path = os.path.join(image_folder, image_name)
        img = cv2.imread(img_path)
        video.write(img)

    video.release()
    v += 1

print(f'Created {image_scraper.j} videos for all images in the {image_scraper.j} folders respectively')
Finish = time.perf_counter()
total_time = round((Finish-Start)/60, 3)

print(f'\nExecuted in {round(image_scraper.total_time + total_time, 3)} minutes...')


