import os
from django.core.management.base import BaseCommand 
from book.models import Chapter, ChapterImage
import urllib.request
import json
from urllib.parse import urlsplit
from book.models import *
from django.contrib import messages, auth
from book.comick import ComicK
from django.utils.text import slugify
from tqdm import tqdm

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--chaps', nargs=2, type=str, required=False)
        parser.add_argument('--slug', type=str, required=True)
    
    def handle(self, *args, **kwargs): 
        slug = kwargs['slug']
        chaps = kwargs['chaps']

        comick = ComicK(slug)
        title = comick.info()['comic']['title']
        book = Book.objects.get(name=title)

        if book is None:
            print('Not found book')
            return
        
        if not book.chapters.all():
            print("Not found chapter")
            return
        
        chapters = book.chapters.all()

        from_chap = int([float(c.chap) for c in chapters].index(float(chaps[0]))) if chaps else None
        to_chap = int([float(c.chap) for c in chapters].index(float(chaps[1]))) if chaps else None

        for chap in tqdm(chapters[from_chap:to_chap]):
            thumbs = comick.get_thumbs(f"{float(chap.chap):g}")
            chapter = Chapter.objects.get(book=book, chap=float(chap.chap))
            list_models = [ChapterImage(chapter=chapter, url=thumb, page=index) for index, thumb in enumerate(thumbs)]
            ChapterImage.objects.bulk_create(list_models)
        print('Finished.')