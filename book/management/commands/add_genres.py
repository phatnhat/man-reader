from django.core.management.base import BaseCommand 
from book.models import Genre
import urllib.request
import json

class Command(BaseCommand):   
    def handle(self, *args, **kwargs): 
        url = 'https://api.comick.app/genre/'
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0')
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8')
        req.add_header('Accept-Language', 'en-US,en;q=0.5')

        r = urllib.request.urlopen(req).read().decode('utf-8')
        data = json.loads(r)

        for d in data:
            g = Genre(name=d['name'], slug=d['slug'])
            g.save()

        print("Finished")