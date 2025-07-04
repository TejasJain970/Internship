from bs4 import BeautifulSoup
import requests
import os

directory = 'path_where_images_will_be_saved'

url = "https://en.wikipedia.org/wiki/List_of_national_flags_of_sovereign_states"

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
           "AppleWebKit/537.36 (KHTML, like GEcko) Chrome/117.0.2311.135 Safari/537.36 Edge/12.246"}

r = requests.get(url=url, headers=headers)
sauce = BeautifulSoup(r.content, 'html.parser')

caption = sauce.find('caption')
table = caption.parent

rows = table.find_all('tr')

for row in rows:
    tds = row.find_all('td')
    for td in tds:
        figures = td.find_all('figure')
        for figure in figures:
            aa = figure.find_all('a')
            for a in aa:
                imgs = a.find_all('img')
                for img in imgs:
                    src = img['src']
                    part1 = src.split('.svg')[0]
                    part2 = part1.replace('thumb/', '')
                    part3 = part2.strip('//')
                    image = f'https://{part3}.svg'
                    filename = image.split('/')[-1]
                    path = os.path.join(directory, filename)
                    flag = requests.get(image, headers=headers)
                    
                    if flag.status_code != 200:
                        print(f'Error getting {filename}')
                    
                    else:
                        with open(path, 'wb') as f:
                            save = f.write(flag.content)
                            print(f'Saved {filename}')


                
