import os
from django.core.management.base import BaseCommand 
from book.models import Genre
import urllib.request
import json
from urllib.parse import urlsplit
from book.models import *
from accounts.models import User, UserReading
from django.contrib import messages, auth
from book.comick import ComicK
from django.db.models import Avg
from book.utils import sort_by

class Command(BaseCommand):   
    def handle(self, *args, **kwargs): 
        user = User.objects.get(email='nhatphay7@gmail.com')
        chapter = Chapter.objects.all()[0]
        user_reading = UserReading.objects.filter(book=chapter.book).all()
        users = User.objects.filter(users_reading__in=user_reading)
        print(users)
