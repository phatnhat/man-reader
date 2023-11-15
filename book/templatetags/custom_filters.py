from django import template
from django.db.models import Avg

register = template.Library()

@register.filter
def pair_items(items):
    return [items[i:i+2] for i in range(0, len(items), 2)]

@register.filter
def check_vote(user, book):
    return user.check_vote(book)

@register.filter
def get_vote(user, book):
    return user.get_vote(book).mark

@register.filter
def check_readinglist(user, book):
    return user.check_userreading(book)

@register.filter
def get_readinglist(user, book):
    return user.get_userreading(book)
