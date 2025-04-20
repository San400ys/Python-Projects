import os
import threading
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from pathlib import Path
from urllib.parse import urlparse
import argparse
import time

class ImageFetcher:
    def __init__(self, max_workers=5, output_dir="downloads"):
        self.max_workers = max_workers
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.lock = threading.Lock()
        self.successful = []
        self.failed = []
        self.sizes = {}

    def download_image(self, url):
        try:
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()
            
            filename = os.path.basename(urlparse(url).path)
            if not filename:
                filename = f"image_{int(time.time())}.jpg"
                
            save_path = self.output_dir / filename
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            size = os.path.getsize(save_path)
            
            with self.lock:
                self.successful.append(url)
                self.sizes[save_path] = size
            
            return True, url, size
        except Exception as e:
            with self.lock:
                self.failed.append(url)
            return False, url, str(e)

    def get_top_largest(self, top_n=5):
        return sorted(self.sizes.items(), key=lambda x: x[1], reverse=True)[:top_n]

    def fetch_images(self, urls):
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self.download_image, url) for url in urls]
            
            for future in tqdm(as_completed(futures), total=len(urls), desc="Скачивание"):
                pass
        
        total_time = time.time() - start_time
        total_size = sum(self.sizes.values()) / (1024 * 1024) 
        avg_speed = total_size / total_time if total_time > 0 else 0
        
        print(f"\nУспешно скачано {len(self.successful)}/{len(urls)} изображений")
        print(f"Общий размер: {total_size:.2f} MB")
        print(f"Средняя скорость: {avg_speed:.2f} MB/сек")
        print(f"Затраченное время: {total_time:.2f} секунд")
        
        if self.failed:
            print(f"\nНе удалось скачать {len(self.failed)} изображений:")
            for url in self.failed[:5]: 
                print(f"- {url}")

        if self.sizes:
            print("\nСамые большие изображения:")
            for path, size in self.get_top_largest():
                print(f"- {path.name}: {size/1024:.2f} KB")

def read_urls_from_file(file_path):
    with open(file_path) as f:
        return [line.strip() for line in f if line.strip()]

def main():
    parser = argparse.ArgumentParser(description="ImageFetcher Pro - параллельный загрузчик изображений")
    parser.add_argument("urls", nargs="*", help="URL-адреса изображений для скачивания")
    parser.add_argument("--file", help="Файл с URL-адресами (по одному на строку)")
    parser.add_argument("--workers", type=int, default=5, help="Количество потоков")
    parser.add_argument("--output", default="downloads", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    urls = args.urls
    if args.file:
        urls.extend(read_urls_from_file(args.file))
    
    if not urls:
        print("Не указаны URL-адреса.")
        return
    
    fetcher = ImageFetcher(max_workers=args.workers, output_dir=args.output)
    fetcher.fetch_images(urls)

if __name__ == "__main__":
    main()
