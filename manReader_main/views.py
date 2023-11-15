from django.shortcuts import render
from book.models import Book, Chapter, View
from django.http import HttpResponse
from accounts.forms import LoginForm, RegisterForm, ForgotForm
from django.db.models import F, Subquery, OuterRef, Count, ExpressionWrapper, FloatField, Avg, Sum
from django.utils import timezone
from django.db.models.functions import ExtractMonth
import pytz
import datetime
from datetime import timedelta

def home(request):
    deslides = Book.objects.all().order_by('?')[:5]
    trends = Book.objects.annotate(
        latest_chapter_date=Subquery(Chapter.objects.filter(book=OuterRef('pk')).order_by('-updated_at').values('updated_at')[:1]),
        trending_metric=ExpressionWrapper(F('latest_chapter_date') + Avg('rates__mark') + Count('views'), output_field=FloatField())
    ).order_by('-trending_metric')[:10]
    recommends = Book.objects.annotate(
        recommendation_metric=Sum('rates__mark')
    ).order_by('-recommendation_metric')[:20]
    lastest_chaps = Book.objects.annotate(
        latest_chapter_date=Subquery(
            Chapter.objects.filter(book=OuterRef('pk')).order_by('-updated_at').values('updated_at')[:1]
    )).order_by('-latest_chapter_date')[:10]
    completed = Book.objects.filter(status__name='Completed')[:20]

    #desired_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    now = datetime.datetime.now(pytz.utc).astimezone()
    today = now.date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    month_start = today.replace(day=1)
    next_month_start = month_start + timedelta(days=32)
    month_end = next_month_start.replace(day=1) - timedelta(days=1)
    most_viewed_today = Book.objects.filter(views__date=today).annotate(view_count=Count('views')).order_by('-view_count')
    most_viewed_week = Book.objects.filter(views__date__range=[week_start, week_end]).annotate(view_count=Count('views')).order_by('-view_count')
    most_viewed_month = Book.objects.filter(views__date__range=[month_start, month_end]).annotate(view_count=Count('views')).order_by('-view_count')
    
    context = {
        'deslides': deslides,
        'trends': trends,
        'recommends': recommends,
        'lastest_chaps': lastest_chaps,
        'chart_today': most_viewed_today,
        'chart_week': most_viewed_week,
        'chart_month': most_viewed_month,
        'completed': completed,
    }

    return render(request, "home.html", context)


def test(request):
    return render(request, 'test.html')
