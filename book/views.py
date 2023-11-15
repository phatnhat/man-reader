import string
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pytz
from .models import Book, Genre, Type, Chapter, ChapterImage, Vote, View, Status, Demographic
from accounts.models import Notification
from django.http import Http404, HttpResponse
import json
import time
from django.template.loader import render_to_string
from django.db.models import Count, Q, Avg, Min, F, OuterRef, Subquery, Sum
from django.views.decorators.csrf import csrf_exempt
from ipware import get_client_ip
from django.utils import timezone
from datetime import timedelta, datetime
from functools import reduce
from operator import and_, or_
from .utils import sort_by, sort_list
# Create your views here.


def type(request, slug):
    sort = request.GET.get('sort', 'default')

    sort_name = [s['name'] for s in sort_list() if s['slug'] == sort][0]

    type = get_object_or_404(Type, slug=slug)
    books = type.type_books.all()
    type_books = sort_by(books, sort)

    paginator = Paginator(type_books, 16)
    page_number = request.GET.get("page", 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'type': slug,
        'sort': sort,
        'sort_list': sort_list(),
        'sort_name': sort_name,
        'page_obj': page_obj,
    }

    return render(request, 'book/type_book-list.html', context)


def genre(request, slug):
    sort = request.GET.get('sort', 'default')

    sort_name = [s['name'] for s in sort_list() if s['slug'] == sort][0]

    genre = get_object_or_404(Genre, slug=slug)
    books = genre.books.all()
    genre_books = sort_by(books, sort)

    paginator = Paginator(genre_books, 16)
    page_number = request.GET.get("page", 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'genre': slug,
        'sort': sort,
        'sort_list': sort_list(),
        'sort_name': sort_name,
        'page_obj': page_obj,
    }

    return render(request, 'book/genre_book-list.html', context)


def hot_cate(request, slug):
    if slug == 'latest-updated':
        books = sort_by(Book.objects.all(), 'latest-updated') #Book.objects.all().order_by('-updated_at')
    elif slug == 'new-release':
        books = sort_by(Book.objects.all(), 'release-date') #Book.objects.all().order_by('-published')
    elif slug == 'most-viewed':
        books = sort_by(Book.objects.all(), 'most-viewed') #Book.objects.all().order_by('created_at')
    elif slug == 'completed':
        sort = request.GET.get('sort', 'default')

        sort_name = [s['name'] for s in sort_list() if s['slug'] == sort][0]

        books = sort_by(Book.objects.filter(status=2), sort) #Book.objects.filter(status=2).order_by(sort_order)
        
        paginator = Paginator(books, 16)
        page_number = request.GET.get("page", 1)

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {
            'cate': slug.replace('-', ' '),
            'slug': slug,
            'sort': sort,
            'sort_list': sort_list(),
            'sort_name': sort_name,
            'page_obj': page_obj,
        }

        return render(request, 'book/hot_cate-list.html', context)
    else:
        raise Http404("The requested resource was not found.")

    paginator = Paginator(books, 16)
    page_number = request.GET.get("page", 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'cate': slug.replace('-', ' '),
        'slug': slug,
        'page_obj': page_obj,
    }

    return render(request, 'book/hot_cate-list.html', context)


def search(request):
    keyword = request.GET.get('keyword')

    books = Book.objects.filter(name__icontains=keyword)

    paginator = Paginator(books, 16)
    page_number = request.GET.get("page", 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'keyword': keyword,
        'page_obj': page_obj,
    }

    return render(request, 'book/search-list.html', context)


def suggest(request):
    keyword = request.GET.get('keyword')
    books = Book.objects.filter(name__icontains=keyword)
    html = render_to_string('includes/search-results.html', {'books': books, 'keyword': keyword})

    return HttpResponse(html)


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    realtime = Book.objects.filter(genres__in=book.genres.all()).exclude(pk=book.pk).annotate(dcount=Count('pk')).order_by()[:5]

    context = {
        'book': book,
        'realtime': realtime,
    }

    return render(request, 'book/detail.html', context)


def read_book(request, slug, chap=None):
    n_id = request.GET.get('n_id')
    if n_id and request.user.is_authenticated: 
        try:
            notification = Notification.objects.get(pk=n_id)
            notification.mark = True
            notification.save()
        except:pass

    book = get_object_or_404(Book, slug=slug)
    if chap is None: chap = book.first_chapter.chap if book.first_chapter else None
    chapter = get_object_or_404(Chapter, book=book, chap=chap)
    chapter_image = ChapterImage.objects.filter(chapter=chapter)

    book_chapters = book.chapters.all()
    next_chapter = book_chapters.order_by('chap').filter(chap__gt=chap).first()
    prev_chapter = book_chapters.order_by('-chap').filter(chap__lt=chap).first()

    context = {
        'book': book,
        'chapter': chapter,
        'chapter_image': chapter_image,
        'prev_chapter': prev_chapter,
        'next_chapter': next_chapter,
    }

    return render(request, 'book/read.html', context)


def random(request):
    book = Book.objects.all().order_by('?').first()
    return redirect('book-detail', slug=book.slug)


def vote(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            book_id = request.POST.get('book_id')
            mark = request.POST.get('mark')

            user = request.user
            book = Book.objects.get(pk=book_id)

            if user.check_vote(book):
                vote = Vote.objects.get(user=request.user, book=book)
                vote.mark = mark
            else:
                vote = Vote(user=request.user, book=book, mark=mark)
            vote.save()

            vote_count = book.rates.count()
            vote_star = book.rates.aggregate(Avg('mark'))['mark__avg']

            return HttpResponse(json.dumps({'status': True, 
                                            'message': 'Thanks for the vote.',
                                            'vote_count': vote_count,
                                            'vote_star': vote_star}), content_type="application/json")
        except Exception as e:
            return HttpResponse(json.dumps({'status': False, 'message': 'Something went wrong. Please try again!'}), content_type="application/json")
    return redirect('home')


@csrf_exempt
def count_view(request, pk):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            client_ip, is_routable = get_client_ip(request)
            book = Book.objects.get(pk=pk)
            view = View(book=book, ip_address=client_ip)
            view.save()
            return HttpResponse(json.dumps({'status': True, 'message': 'Success'}), content_type="applicatino/json")
        except Exception as e:
            return HttpResponse(json.dumps({'status': False, 'message': e}), content_type="applicatino/json")
    return redirect('home')


def filter(request):
    type = request.GET.get('type', '')
    status = request.GET.get('status', '')
    demographic = request.GET.get('demographic', '')
    create_at = int(request.GET.get('create_at', 0) or 0) 
    end_date = timezone.now()
    start_date = end_date - timedelta(days=create_at) 
    min_chap = 0 if request.GET.get('min_chap', 0) == '' else int(request.GET.get('min_chap', 0))
    sy = int(request.GET.get('sy', 0) or 0)
    ey = int(request.GET.get('ey', 0) or 0)
    sort = request.GET.get('sort', 'default')
    genres = request.GET.get('genres') or ''

    typies = Type.objects.all()
    statues = Status.objects.all()
    demographics = Demographic.objects.all()
    published_choices = Book.published.field.choices

    filter_kwargs = {}
    filter_kwargs['type__id__icontains'] = type
    filter_kwargs['status__id__icontains'] = status
    filter_kwargs['demographic__id__icontains'] = demographic
    if create_at != 0: filter_kwargs['created_at__range'] = [start_date, end_date]
    if sy != 0 and ey == 0: filter_kwargs['published__gte'] = sy
    elif sy == 0 and ey != 0: filter_kwargs['published__lte'] = ey
    elif sy != 0 and ey != 0: filter_kwargs['published__range'] = [sy, ey]
    
    books = Book.objects.annotate(chapter_count=Count('chapters')).filter(**filter_kwargs)

    if genres:
        genres = list(genres.split(','))
        for genre in genres: books = books.filter(genres__id=genre)

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

    if min_chap != 0: books = [book for book in books if float(getattr(book.last_chapter, 'chap', '-1')) >= min_chap]

    paginator = Paginator(books, 16)
    page_number = request.GET.get("page", 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'type_selected': type,
        'status_selected': status,
        'create_at_selected': create_at,
        'min_chap_selected': min_chap,
        'demographic_selected': demographic,
        'min_chap_value': min_chap,
        'sort': sort,
        'sy': sy,
        'ey': ey,
        'genres_selected': ",".join(genres),
        'typies': typies,
        'statues': statues,
        'demographics': demographics,
        'published_choices': published_choices,
        'page_obj': page_obj,
        'page_number': page_number,
    }
    return render(request, 'book/filter.html', context)


def az_list(request, alpha=None):
    alpha_list = [('All', None), ('#', 'other'), ('0-9', '0-9')] + [(alpha, alpha) for alpha in list(string.ascii_uppercase)]

    if alpha == None:
        books = Book.objects.all().order_by('name')
    elif alpha == "other":
        books = Book.objects.exclude(Q(name__regex=r'^[A-Za-z]')).all()
    elif alpha == '0-9':
        books = Book.objects.filter(Q(name__regex=r'^[0-9]')).all()
    else:
        books = Book.objects.filter(Q(name__istartswith=alpha)).all()

    #desired_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    now = datetime.now(pytz.utc).astimezone()
    today = now.date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    month_start = today.replace(day=1)
    next_month_start = month_start + timedelta(days=32)
    month_end = next_month_start.replace(day=1) - timedelta(days=1)
    most_viewed_today = Book.objects.filter(views__date=today).annotate(view_count=Count('views')).order_by('-view_count')
    most_viewed_week = Book.objects.filter(views__date__range=[week_start, week_end]).annotate(view_count=Count('views')).order_by('-view_count')
    most_viewed_month = Book.objects.filter(views__date__range=[month_start, month_end]).annotate(view_count=Count('views')).order_by('-view_count')

    paginator = Paginator(books, 16)
    page_number = request.GET.get("page", 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    context = {
        'books': books,
        'page_obj': page_obj,
        'alpha_list': alpha_list,
        'alpha_selected': alpha,
        'chart_today': most_viewed_today,
        'chart_week': most_viewed_week,
        'chart_month': most_viewed_month,
    }
    return render(request, 'book/az-list.html', context)

