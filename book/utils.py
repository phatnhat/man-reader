from django.db.models import Count,  Avg, OuterRef, Subquery
from .models import Chapter

def sort_by(books, sort='default'):
    if sort == 'latest-updated':
        books = books.annotate(
            latest_chapter_date=Subquery(
                Chapter.objects.filter(book=OuterRef('pk')).order_by('-updated_at').values('updated_at')[:1]
        )).order_by('-latest_chapter_date')
    elif sort == 'rating':
        books = books.annotate(
            rating=Avg('rates__mark')
        ).order_by('-rating')
    elif sort == 'name-az':
        books = books.order_by('name')
    elif sort == 'release-date':
        books = books.order_by('-published')
    elif sort == 'most-viewed':
        books = books.annotate(
            view=Count('views')
        ).order_by('-view')
    else:
        books = books.order_by('-created_at')
    return books

def sort_list():
    return [
        {'slug': 'default', 'name': "Default"},
        {'slug': 'latest-updated', 'name': 'Latest Updated'},
        {'slug': 'rating', 'name': 'Rating'},
        {'slug': 'name-az', 'name': 'Name A-Z'},
        {'slug': 'release-date', 'name': 'Release Date'},
        {'slug': 'most-viewed', 'name': 'Most Viewed'}
    ]