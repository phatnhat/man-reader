from django.db import models
from django.utils.text import slugify
import datetime
import base64
import requests
import os
import json
from urllib.parse import urlsplit
from dotenv import load_dotenv
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.utils.html import format_html
from django.utils.html import escape
from django.db.models import *
from django.http import HttpRequest
from ipware import get_client_ip



# Create your models here.
load_dotenv('./manReader_main/.env')

class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'type'
        verbose_name_plural = 'typies'

    def save(self):
        self.slug = slugify(self.name)
        super().save()

    def __str__(self):
        return self.name
    

class Demographic(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'demographic'
        verbose_name_plural = 'demographics'

    def save(self):
        self.slug = slugify(self.name)
        super().save()

    def __str__(self):
        return self.name
    

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def save(self):
        self.slug = slugify(self.name)
        super().save()

    def __str__(self):
        return self.name
    

class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'status'
        verbose_name_plural = 'statues'

    def save(self):
        self.slug = slugify(self.name)
        super().save()

    def __str__(self):
        return self.name
    

class Author(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'author'
        verbose_name_plural = 'authors'

    def save(self):
        self.slug = slugify(self.name)
        super().save()

    def __str__(self):
        return self.name
    

class Artist(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'artist'
        verbose_name_plural = 'artists'

    def save(self):
        self.slug = slugify(self.name)
        super().save()

    def __str__(self):
        return self.name


class Book(models.Model):
    YEAR_CHOICES = [(r, r) for r in range(1990, datetime.date.today().year+1)]
    CURRENT_YEAR = datetime.date.today().year
    HOST_UPLOAD = 'https://api.imgbb.com/1/upload'

    name = models.CharField(max_length=200, unique=True)
    origin_name = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=1024, blank=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True, related_name='type_books')
    genres = models.ManyToManyField(Genre, related_name='books')
    demographic = models.ForeignKey(Demographic, on_delete=models.CASCADE, null=True, blank=True, related_name='demographic_books')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True, related_name='status_books')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True, related_name='author_books')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True, blank=True, related_name='artist_books')
    published = models.IntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR)
    cover_photo = models.ImageField(blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def poster_tag(self):
        return format_html('<img src="https://i.ibb.co/{}" width=100/>', self.cover_photo)
    poster_tag.short_description = 'Poster'
    poster_tag.allow_tags = True

    @property
    def first_chapter(self):
        smallest_chap = self.chapters.aggregate(smallest=Min('chap'))
        return self.chapters.filter(chap=smallest_chap['smallest']).first()
    
    @property
    def last_chapter(self):
        maxest_chap = self.chapters.aggregate(maxest=Max('chap'))
        return self.chapters.filter(chap=maxest_chap['maxest']).first()
    
    @property
    def list_chapters(self):
        return self.chapters.all().order_by('-chap')
    
    @property
    def vote_count(self):
        return self.rates.count()
    
    @property
    def vote_star(self):
        return self.rates.aggregate(Avg('mark'))['mark__avg'] or 0.0

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        if self.pk is not None:
            orig = Book.objects.get(pk=self.pk)
            
        if self.pk is None or (self.pk is not None and orig.cover_photo != self.cover_photo):
            if self.cover_photo:
                encodedString = base64.b64encode(self.cover_photo.file.read())
                data = {"key": os.getenv("IMGBB_API"), "image": encodedString.decode("utf-8")}
                uploadedImageInfo = requests.post(self.HOST_UPLOAD, data=data)
                jsonResponse = json.loads(uploadedImageInfo.text)
                url = jsonResponse["data"]["display_url"]
                filename = urlsplit(url).path.lstrip('/')
                self.cover_photo.save(str(filename), '', save=False)
        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.id}'
    

class Chapter(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    chap = models.FloatField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def tit(self):
        return self.title if self.title is not None else ''

    def __str__(self):
        return f'{self.book.name} - Chap {self.chap}'
    

class ChapterImage(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='images')
    url = models.URLField(blank=True, null=True)
    page = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])

    def image_tag(self):
        return format_html('<img src="{}" width=100/>', self.url)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __str__(self):
        return f'Page {self.page}'
    

class Vote(models.Model):
    MARK_CHOICES = [(1, "BAD"), (2, "NORMAL"), (10, "GOOD")]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='rates')
    user = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='votes')
    mark = models.IntegerField(choices=MARK_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'book'], name='unique_vote')
        ]

    def __str__(self):
        return f'{self.user} | {self.book}: {self.mark}'
    

class View(models.Model):
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='views')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.ip_address} | {self.book}'
    

class ReadingList(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


