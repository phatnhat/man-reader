import base64
import json
import os
from urllib.parse import urlsplit
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
import requests
from django.utils.html import format_html

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        
        if not name:
            raise ValueError('User must have an name')
        
        user = self.model(
            email = self.normalize_email(email),
            name = name,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, name, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(name, email, password, **extra_fields)
    
    
class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def check_vote(self, book):
        return self.votes.filter(book=book)
    
    def get_vote(self, book):
        if self.check_vote(book):
            return self.votes.get(book=book)
        return None
    
    def check_userreading(self, book):
        return self.users_reading.filter(book=book)
    
    def get_userreading(self, book):
        if self.check_userreading(book):
            return self.users_reading.get(book=book)
        return None

    def __str__(self):
        return self.email
    

class AvatarHashtag(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Avatar(models.Model):
    HOST_UPLOAD = 'https://api.imgbb.com/1/upload'

    hashtag = models.ForeignKey(AvatarHashtag, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(blank=True, null=True)

    def image_tag(self):
        return format_html('<img src="https://i.ibb.co/{}" width=100/>', self.image)
    image_tag.short_description = 'Picture'
    image_tag.allow_tags = True

    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Avatar.objects.get(pk=self.pk)
            
        if self.pk is None or (self.pk is not None and orig.image != self.image):
            if self.image:
                encodedString = base64.b64encode(self.image.file.read())
                data = {"key": os.getenv("IMGBB_API"), "image": encodedString.decode("utf-8")}
                uploadedImageInfo = requests.post(self.HOST_UPLOAD, data=data)
                jsonResponse = json.loads(uploadedImageInfo.text)
                url = jsonResponse["data"]["display_url"]
                filename = urlsplit(url).path.lstrip('/')
                self.image.save(str(filename), '', save=False)
        super(Avatar, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.hashtag}'

    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='profile')
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE, blank=True, null=True, default=1, related_name='profiles')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name
    

class UserReading(models.Model):
    reading_list = models.ForeignKey('book.ReadingList', blank=True, null=True, on_delete=models.CASCADE, related_name="user_reading_lists")
    book = models.ForeignKey('book.Book', on_delete=models.CASCADE, related_name='books_reading')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='users_reading')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'book'], name='unique_readingist')
        ]

    def __str__(self):
        return f'{self.user} - {self.book} | {self.reading_list}'
    

class ContinueReading(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='users_continue_reading')
    book = models.ForeignKey('book.Book', null=True, blank=True, on_delete=models.CASCADE, related_name='books_continue_reading')
    chapter = models.ForeignKey('book.Chapter', null=True, blank=True, on_delete=models.CASCADE, related_name='chapters_continue_reading')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'chapter'], name='unique_continuereading')
        ]

    def __str__(self):
        return f'{self.user} | {self.chapter}'
    

class Notification(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='user_notifications')
    chapter = models.ForeignKey('book.Chapter', null=True, blank=True, on_delete=models.CASCADE, related_name='chapter_notifications')
    mark = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'chapter'], name='unique_notification')
        ]

    def __str__(self):
        return f'{self.user} | {self.chapter}'
