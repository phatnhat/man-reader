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
from django.conf import settings

class Command(BaseCommand):   
    def handle(self, *args, **kwargs): 
        project_name = settings.SETTINGS_MODULE.split('.')[0]
        print(project_name)
