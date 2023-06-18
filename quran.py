import os
import sys
import requests
import time
from tqdm import tqdm
from surahs import surahs
import argparse
from crawl_reciters import crawl_reciters
from colorama import Fore, Style

def format_speed(speed):
    if speed >= 1024 * 1024:
        return f"{speed / (1024 * 1024):.2f} mB/s"
    elif speed >= 1024:
        return f"{speed / 1024:.2f} kB/s"
    else:
        return f"{speed:.2f} B/s"


def download_surahs(reciter_slug):
    reciter_folder = f"downloads/{reciter_slug}"
    os.makedirs(reciter_folder, exist_ok=True)

    total_size = 0
    total_time = 0
    not_found_surahs = []

    with tqdm(total=len(surahs), ncols=80) as pbar:
        for index, surah_name in enumerate(surahs, start=1):
            filename = f"{index:03d} {surah_name} - {reciter_slug}.mp3"
            file_path = os.path.join(reciter_folder, filename)
            url = f"https://download.quranicaudio.com/quran/{reciter_slug}/{index:03d}.mp3"

            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            if os.path.isfile(file_path):
                pbar.update(1)
                continue

            start_time = time.time()

            response = requests.get(url, stream=True)
            if response.status_code == 200:
                try:
                    with open(file_path, "wb") as file:
                        with tqdm(
                            desc=f"Downloading {index}/{len(surahs)} {surah_name}",
                            total=int(response.headers.get("Content-Length", 0)),
                            unit="B",
                            unit_scale=True,
                            unit_divisor=1024,
                            ncols=80
                        ) as inner_pbar:
                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:
                                    file.write(chunk)
                                    inner_pbar.update(len(chunk))
                except FileNotFoundError:
                    not_found_surahs.append(f"{index:03d} {surah_name}")
            else:
                not_found_surahs.append(f"{index:03d} {surah_name}")

            end_time = time.time()
            elapsed_time = end_time - start_time

            try:
                file_size = os.path.getsize(file_path)
                total_size += file_size
            except FileNotFoundError:
                pass

            total_time += elapsed_time

            pbar.update(1)

    average_speed = total_size / total_time
    total_size_gb = total_size / (1024 * 1024 * 1024)
    total_time_minutes = total_time / 60

    formatted_speed = format_speed(average_speed)

    print("\nAll surahs downloaded successfully!")
    print(f"Total size: {total_size_gb:.2f} GB")
    print(f"Total time taken: {total_time_minutes:.2f} minutes")
    print(f"Average download speed: {formatted_speed}")

    if not_found_surahs:
        print("\nSurahs not found:")
        for surah in not_found_surahs:
            print(f"{Fore.YELLOW}{surah}{Style.RESET_ALL}")

def display_reciters():
    from reciters import reciters

    print("Available Reciters:")
    for reciter in reciters:
        print(reciter)

def main():
    parser = argparse.ArgumentParser(description="Quran Downloader")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Help Command
    help_parser = subparsers.add_parser('help', help='Show usage information')

    # Crawl Reciters Command
    crawl_reciters_parser = subparsers.add_parser('crawl-reciters', help='Crawls all reciters and updates reciters.py')

    # Reciters Command
    reciters_parser = subparsers.add_parser('reciters', help='Display all available reciters')

    # Download Command
    download_parser = subparsers.add_parser('download', help='Download surahs by reciter slug')
    download_parser.add_argument('reciter', type=str, help='Reciter slug')

    args = parser.parse_args()

    if args.command == 'crawl-reciters':
        crawl_reciters()
    elif args.command == 'reciters':
        display_reciters()
    elif args.command == 'download':
        reciter_slug = args.reciter
        download_surahs(reciter_slug)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
