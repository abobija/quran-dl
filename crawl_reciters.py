import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

def extract_links(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    anchor_elements = soup.select('a[href^="/quran/"]')

    links = [anchor_element['href'] for anchor_element in anchor_elements]

    return links

def extract_download_link(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    download_element = soup.select_one('.list-group-item a[href*=download]')

    if download_element:
        download_link = download_element['href']
        return download_link

    return None

def crawl_reciters():
    main_url = 'https://quranicaudio.com'
    links = extract_links(main_url)
    reciter_slugs = []

    with tqdm(total=len(links), ncols=80, unit="link") as pbar:
        for link in links:
            absolute_link = f"{main_url}{link}"
            download_link = extract_download_link(absolute_link)

            if download_link:
                reciter_slug = download_link.split("/")[4]
                reciter_slugs.append(reciter_slug)

            time.sleep(0.25)  # Delay of 0.25 seconds between each request
            pbar.update(1)

    with open("reciters.py", "w") as file:
        file.write("reciters = [\n")
        for slug in reciter_slugs:
            file.write(f"    '{slug}',\n")
        file.write("]\n")

if __name__ == "__main__":
    crawl_reciters()
