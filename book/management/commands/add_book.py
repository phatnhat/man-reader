import os
from django.core.management.base import BaseCommand 
from book.models import Genre
import urllib.request
import json
from urllib.parse import urlsplit
from book.models import *
from django.core.files import File
from book.comick import ComicK

class Command(BaseCommand):   
    def add_arguments(self, parser):
        parser.add_argument('--slug', type=str, required=True)

    def handle(self, *args, **kwargs):
        slug = kwargs['slug']

        print("Loading...") 

        comick = ComicK(slug)
        title = comick.info()['comic']['title']
        book = Book.objects.filter(name=title)

        if book:
            print("Book is existed")
            return
        
        name = comick.info()['comic']['title']
        country = comick.info()['comic']['country']
        type = Type.objects.filter(pk=1 if country == 'jp' else 2 if country == 'kr' else 3).first() or None
        iso = comick.info()['comic']['iso639_1']
        origin_name = [name['title'] for name in comick.info()['comic']['md_titles'] if name['lang'] == iso][0]
        desc = comick.info()['comic']['desc']
        genres = [genre['md_genres']['name'] for genre in comick.info()['comic']['md_comic_md_genres']]
        demographic = Demographic.objects.filter(pk=comick.info()['comic']['demographic']).first() or None
        status = Status.objects.filter(pk=comick.info()['comic']['status']).first() or None
        author = Author.objects.filter(name=comick.info()['authors'][0]['name'])
        artist = Artist.objects.filter(name=comick.info()['artists'][0]['name'])
        published = comick.info()['comic']['year']
        cover_photo = f"https://meo.comick.pictures/{comick.info()['comic']['md_covers'][0]['b2key']}"

        print('Adding book...')

        if not author:
            author = Author(name=comick.info()['authors'][0]['name'])
            author.save()
        else: author = author.first()

        if not artist:
            artist = Artist(name=comick.info()['artists'][0]['name'])
            artist.save()
        else: artist = artist.first()

        book = Book(name=name, origin_name=origin_name, description=desc, type=type, 
                    demographic=demographic, status=status, author=author, artist=artist, 
                    published=published)
        
        print("Uploading cover photo...")

        opener  = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'),
                            ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'),
                            ('Accept-Language', 'en-US,en;q=0.5')]
        urllib.request.install_opener(opener)
        req = urllib.request.urlretrieve(cover_photo)
        book.cover_photo = File(open(req[0], 'rb'))
        book.save()
        book.genres.add(*[Genre.objects.get(name=genre) for genre in genres])

        print('Finished.')




        
    # def handle(self, *args, **kwargs): 
    #     slug = '01-komi-san-wa-komyushou-desu'
    #     url = f'https://api.comick.app/comic/{slug}'
        
    #     req = urllib.request.Request(url)
    #     req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0')
    #     req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8')
    #     req.add_header('Accept-Language', 'en-US,en;q=0.5')

    #     r = urllib.request.urlopen(req).read().decode('utf-8')
    #     responseJson = json.loads(r)

    #     name = responseJson['comic']['title']
    #     country = responseJson['comic']['country']
    #     type = Type.objects.get(pk=1 if country == 'jp' else 2 if country == 'kr' else 3)
    #     iso = responseJson['comic']['iso639_1']
    #     origin_name = [name['title'] for name in responseJson['comic']['md_titles'] if name['lang'] == iso][0]
    #     desc = responseJson['comic']['desc']
    #     genres = [genre['name'] for genre in responseJson['genres']]
    #     demographic = Demographic.objects.get(pk=responseJson['comic']['demographic'])
    #     status = Status.objects.get(pk=responseJson['comic']['status'])
    #     author = Author.objects.filter(name=responseJson['authors'][0]['name'])
    #     artist = Artist.objects.filter(name=responseJson['artists'][0]['name'])
    #     published = responseJson['comic']['year']
    #     cover_photo = f"https://meo.comick.pictures/{responseJson['comic']['md_covers'][0]['b2key']}"

    #     if not author:
    #         author = Author(name=responseJson['authors'][0]['name'])
    #         author.save()
    #     else: author = author.first()

    #     if not artist:
    #         artist = Artist(name=responseJson['artists'][0]['name'])
    #         artist.save()
    #     else: artist = artist.first()

    #     book = Book(name=name, origin_name=origin_name, description=desc, type=type, 
    #                 demographic=demographic, status=status, author=author, artist=artist, 
    #                 published=published)
    #     opener  = urllib.request.build_opener()
    #     opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'),
    #                         ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'),
    #                         ('Accept-Language', 'en-US,en;q=0.5')]
    #     urllib.request.install_opener(opener)
    #     req = urllib.request.urlretrieve(cover_photo)
    #     book.cover_photo = File(open(req[0], 'rb'))
    #     book.save()
    #     book.genres.add(*[Genre.objects.get(name=genre) for genre in genres])


        # result = {
        #     'name': name,
        #     'country': country,
        #     'type': type,
        #     'origin_name': origin_name,
        #     'desc': desc,
        #     'genres': genres,
        #     'demographic': demographic,
        #     'status': status,
        #     'author': author,
        #     'artist': artist,
        #     'published': published,
        #     'cover_photo': cover_photo,
        # }