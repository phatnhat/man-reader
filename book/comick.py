import requests
from tqdm import tqdm
import os
import concurrent.futures
import time
import urllib.request
import json
import glob

class ComicK():
    def __init__(self, url):
        self.base_url = "https://api.comick.fun"
        self.img_url = "https://meo.comick.pictures"

        self.url = url
        self.manga = self.search()

    def _request(self, url, data=None):
        MAX_RETRY = 5

        for tries in range(MAX_RETRY):
            try:
                req = urllib.request.Request(url, data)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0')
                req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8')
                req.add_header('Accept-Language', 'en-US,en;q=0.5')

                r = urllib.request.urlopen(req, timeout=30).read().decode('utf-8')

                return r
            except Exception as e:
                if tries < (MAX_RETRY - 1):
                    continue
                return None


    def search(self):
        url_parts = self.url.split("/")
        slug = url_parts[-1]

        r = self._request(
            f"{self.base_url}/comic/{slug}"
        )

        return json.loads(r)
    
    
    def info(self):
        return self.manga
    
    
    def get_list_chapter(self, limit=9999999, lang='en'):
        r = self._request(f"{self.base_url}/comic/{self.manga['comic']['hid']}/chapters?chapter-order=1&limit={limit}&lang={lang}")
        return [chapter for chapter in json.loads(r)["chapters"] if chapter['chap'] is not None]
    
    
    def get_chapter(self, chapter, lang='en'):
        r = self._request(f"{self.base_url}/comic/{self.manga['comic']['hid']}/chapters?limit=1&page=1&chap-order=1&lang={lang}&chap={chapter}")
        return json.loads(r)["chapters"][0]
    
    def get_thumbs(self, chapter, lang='en'):
        chapter = self.get_chapter(chapter, lang)
        r = self._request(f"{self.base_url}/chapter/{chapter['hid']}/")
        r_json = json.loads(r)['chapter']['md_images']

        return [f"{self.img_url}/{md_image['b2key']}" for md_image in r_json]
