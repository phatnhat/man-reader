from django.db import models
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from .models import Type, Genre, Author, Artist, Book, Status, Demographic, Chapter, ChapterImage, Vote, View, ReadingList
import requests
from django.contrib.admin import widgets

# Register your models here.
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    ordering = ('id',)
    prepopulated_fields = {'slug': ('name',)}

class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    ordering = ('id',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    ordering = ('id',)
    prepopulated_fields = {'slug': ('name',)}

class DemographicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    ordering = ('id',)
    prepopulated_fields = {'slug': ('name',)}


class BookChapterImageInline(admin.StackedInline):
    model = ChapterImage
    extra = 0
    fields = ('image_tag', 'url')
    readonly_fields = ['image_tag']

class BookChapterAdmin(admin.ModelAdmin):
    inlines = [BookChapterImageInline]
    search_fields = ['book__name', 'chap']
    raw_id_fields = ('book',)

class BookChapterInline(admin.TabularInline):
    model = Chapter
    extra = 0
    ordering = ('-chap',)

class BookAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/admin/style.css',)
        }
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    inlines = [BookChapterInline]
    list_display = ('name', 'type', 'author', 'artist', 'status')
    fields = ('poster_tag', 'name', 'origin_name', 'description', 'type', 'demographic', 'status', 
            'genres', 'author', 'artist', 'published', 'cover_photo', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    readonly_fields = ['poster_tag']


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    ordering = ('id',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['id', 'name']

class ArtistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    ordering = ('id',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['id', 'name']

class VoteAdmin(admin.ModelAdmin):
    raw_id_fields = ('book', 'user')

class ViewAdmin(admin.ModelAdmin):
    readonly_fields = ('date',) 

admin.site.register(Type, TypeAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Artist, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Demographic, DemographicAdmin)
admin.site.register(Chapter, BookChapterAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(View, ViewAdmin)
admin.site.register(ReadingList)