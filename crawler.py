import os
import random
import time

import cloudscraper
import requests

HTTP_Headers = {'User-Agent':'Mozilla/5.0'}
MyAnimeList_URL = 'https://myanimelist.net/topanime.php'
AnimePlanet_URL = 'https://www.anime-planet.com/anime/all'

def crawl(dir_name, base_url, page_count, mode='page', offset=0, scraper=False):
    print(f"Crawling {base_url}...")
    os.makedirs(f"data/{dir_name}/", exist_ok=True)
    for page in range(1, page_count + 1):
        if mode == 'offset':
            index = (page - 1) * 50
            file_num = page
        else:
            index = page
            file_num = page

        target_url = f"{base_url}?limit={index}" if mode == 'offset' else f"{base_url}?page={index}"
        print(f'Downloading {target_url} page {page}...')

        try:
            if scraper:
                raw = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}).get(target_url, timeout=15)
            else:
                raw  = requests.get(target_url, headers=HTTP_Headers, timeout=10)

            if raw.status_code == 200:
                with open(f"data/{dir_name}/{file_num}.html", "w", encoding="utf-8") as f:
                    f.write(raw.text)
            else :
                print(f"Error: {raw.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Exception: {e}")

        time.sleep(random.randint(5, 10))

if __name__ == "__main__":
    crawl("mal", MyAnimeList_URL, 22, mode='offset')
    crawl("ap", AnimePlanet_URL, 35, mode='page', scraper=True)
