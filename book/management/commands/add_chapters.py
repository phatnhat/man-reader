import os
from django.core.management.base import BaseCommand 
from book.models import Chapter
import urllib.request
import json
from urllib.parse import urlsplit
from book.models import *
from accounts.models import User
from django.contrib import messages, auth
from book.comick import ComicK
from tqdm import tqdm
from collections import defaultdict

class Command(BaseCommand):   
    def add_arguments(self, parser):
        parser.add_argument('--slug', type=str, required=True)

    def handle(self, *args, **kwargs):
        slug = kwargs['slug']

        comick = ComicK(slug)
        title = comick.info()['comic']['title']
        book = Book.objects.get(name=title)

        if book is None:
            print('Not found book')
            return
        
        chapters = list({ 
                each['chap'] : each for each in comick.get_list_chapter()[::-1]
            }.values()) 

        if book.chapters.all():
            index = [i for i, element in enumerate(chapters, start=1) if element['chap'] == f'{book.last_chapter:g}'][0]
            for chap in tqdm(chapters[index:]):
                chapter = Chapter(title=chap['title'], book=book, chap=float(chap['chap']))
                chapter.save()
        else:
            for chap in tqdm(chapters):
                chapter = Chapter(title=chap['title'], book=book, chap=float(chap['chap']))
                chapter.save()
        print('Finished.')

